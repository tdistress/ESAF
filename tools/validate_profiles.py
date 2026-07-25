#!/usr/bin/env python3
"""Fail-closed validation of versioned ESAF profile packages."""

from __future__ import annotations

import argparse
import json
import re
import stat
import sys
from dataclasses import dataclass
from pathlib import Path, PurePosixPath
from typing import Sequence

import yaml
from jsonschema import Draft202012Validator, FormatChecker
from jsonschema.exceptions import SchemaError
from referencing.exceptions import Unresolvable

if __package__:
    from .crosswalks.io import parse_front_matter
    from .validate_assessment import (
        DIRECT_NEGATED_PROPOSITION,
        PROPOSITION_BOUNDARY,
        asserted_prohibited_phrases,
        quoted_occurrence_is_metalinguistic,
    )
else:
    from crosswalks.io import parse_front_matter
    from validate_assessment import (
        DIRECT_NEGATED_PROPOSITION,
        PROPOSITION_BOUNDARY,
        asserted_prohibited_phrases,
        quoted_occurrence_is_metalinguistic,
    )


ROOT = Path(__file__).resolve().parents[1]
PACKAGE_FILES = {
    "profile": "profile.json",
    "readme": "README.md",
    "control_selections": "control-selections.json",
    "risk_overlays": "risk-overlays.json",
    "evidence_expectations": "evidence-expectations.json",
    "external_references": "external-references.json",
}
DOCUMENT_SCHEMAS = {
    "profile": "profile.schema.json",
    "control_selections": "control-selections.schema.json",
    "risk_overlays": "risk-overlays.schema.json",
    "evidence_expectations": "evidence-expectations.schema.json",
    "external_references": "external-references.schema.json",
}
SEMVER_PATTERN = r"[0-9]+\.[0-9]+\.[0-9]+"
SEMVER = re.compile(rf"^{SEMVER_PATTERN}$")
PROFILE_DOMAIN = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
PROFILE_IDENTIFIER = re.compile(
    rf"^[a-z0-9]+(?:-[a-z0-9]+)*--"
    rf"[a-z0-9]+(?:-[a-z0-9]+)*--(?P<version>{SEMVER_PATTERN})$"
)
PROFILE_ROOT_FILES = frozenset({"ESAF-1800.md", "README.md"})
PROFILE_PROPOSITION_BOUNDARY = re.compile(
    rf"(?:{PROPOSITION_BOUNDARY.pattern})|"
    r"\b(?:even\s+though|while|whereas|though)\b|[\r\n]",
    PROPOSITION_BOUNDARY.flags,
)
UK_PILOT_PROFILE_ID = "uk--jurisdiction-profile--0.1.0"
UK_PILOT_REGISTRY_PATHS = {
    (
        "uk-ncsc--cyber-essentials-requirements-for-it-infrastructure--3.3"
        "--esaf-0.4-alpha--0.1.0"
    ): (
        "crosswalks/registry/"
        "uk-ncsc--cyber-essentials-requirements-for-it-infrastructure--3.3"
        "--esaf-0.4-alpha--0.1.0.md"
    ),
    (
        "uk-ncsc--cyber-essentials-plus-test-specification--3.2"
        "--esaf-0.4-alpha--0.1.0"
    ): (
        "crosswalks/registry/"
        "uk-ncsc--cyber-essentials-plus-test-specification--3.2"
        "--esaf-0.4-alpha--0.1.0.md"
    ),
    (
        "uk-ncsc--cyber-essentials-plus-test-specification--3.2"
        "--esaf-0.4-alpha--0.2.0"
    ): (
        "crosswalks/registry/"
        "uk-ncsc--cyber-essentials-plus-test-specification--3.2"
        "--esaf-0.4-alpha--0.2.0.md"
    ),
}
UK_PILOT_MAPPING_REFERENCES = frozenset(UK_PILOT_REGISTRY_PATHS)
MAPPING_LIFECYCLE_STATES = ("approved", "published", "deprecated", "retired")
EXTERNAL_IMPORT_FIELDS = frozenset(
    {
        "relationship",
        "relationships",
        "disposition",
        "dispositions",
        "supported-outcome",
        "supported-outcomes",
        "equivalence",
        "evidence-import",
        "evidence-imports",
    }
)
LOCAL_MATURITY_FIELDS = frozenset(
    {
        "local-maturity-scale",
        "maturity-levels",
        "maturity-model",
        "maturity-scale",
    }
)
NON_IMPORT_STATEMENT = (
    "Relationships, external outcomes, and evidence are not imported."
)
BOUNDED_PREDICATE_MODIFIERS = (
    r"(?:(?:not|never|by\s+no\s+means)\s+)?"
    r"(?:(?!(?:not|never)\b)[A-Za-z]+ly\s+)?"
)
ASPECT_VOICE_AUXILIARY_MATRIX = {
    "active_do": r"(?:does|did)\s+(?:not\s+)?",
    "active_perfect": r"(?:has|had)\s+(?:(?:not|never)\s+)?",
    "active_progressive": r"(?:is|was)\s+(?:(?:not|never)\s+)?",
    "active_perfect_progressive": (
        r"(?:has|had)\s+(?:(?:not|never)\s+)?been\s+"
    ),
    "passive_simple": (
        r"(?:is|are|was|were)\s+(?:(?:not|never)\s+)?"
    ),
    "passive_perfect": (
        r"(?:has|have|had)\s+(?:(?:not|never)\s+)?been\s+"
    ),
    "passive_progressive": (
        r"(?:is|are|was|were)\s+(?:(?:not|never)\s+)?being\s+"
    ),
}


def bounded_aspect_voice_patterns(
    *,
    active_subject: str,
    active_object: str,
    passive_subject: str,
    passive_agent: str,
    base: str,
    present: str,
    past: str,
    participle: str,
    progressive: str,
) -> tuple[re.Pattern[str], ...]:
    """Compile the bounded active/passive auxiliary matrix for one verb."""
    matrix = ASPECT_VOICE_AUXILIARY_MATRIX
    active_rows = (
        rf"(?P<outcome>(?:{present}|{past})\s+{active_object})",
        rf"{matrix['active_do']}"
        rf"(?P<outcome>{base}\s+{active_object})",
        rf"{matrix['active_perfect']}"
        rf"(?P<outcome>{participle}\s+{active_object})",
        rf"{matrix['active_progressive']}"
        rf"(?P<outcome>{progressive}\s+{active_object})",
        rf"{matrix['active_perfect_progressive']}"
        rf"(?P<outcome>{progressive}\s+{active_object})",
    )
    passive_rows = (
        rf"{matrix['passive_simple']}"
        rf"(?P<outcome>{participle}\s+{passive_agent})",
        rf"{matrix['passive_perfect']}"
        rf"(?P<outcome>{participle}\s+{passive_agent})",
        rf"{matrix['passive_progressive']}"
        rf"(?P<outcome>{participle}\s+{passive_agent})",
    )
    return tuple(
        re.compile(
            rf"\b{active_subject}\s+{row}\b",
            re.IGNORECASE,
        )
        for row in active_rows
    ) + tuple(
        re.compile(
            rf"\b{passive_subject}\s+{row}\b",
            re.IGNORECASE,
        )
        for row in passive_rows
    )


PROFILE_ASSERTION_PATTERNS = (
    (
        "legal sufficiency",
        re.compile(
            r"\bestablish(?:es|ed|ing)?\s+(?:no\s+)?"
            r"(?P<outcome>legal sufficiency)\b",
            re.IGNORECASE,
        ),
    ),
    (
        "external approval",
        re.compile(
            r"\bestablish(?:es|ed|ing)?\s+(?:no\s+)?"
            r"(?P<outcome>external approval)\b",
            re.IGNORECASE,
        ),
    ),
    (
        "production readiness",
        re.compile(
            r"\bestablish(?:es|ed|ing)?\s+(?:no\s+)?"
            r"(?P<outcome>production readiness)\b",
            re.IGNORECASE,
        ),
    ),
    (
        "legal sufficiency",
        re.compile(
            r"\b(?:is|are|was|were)\s+(?:not\s+)?"
            r"(?P<outcome>legally sufficient)\b",
            re.IGNORECASE,
        ),
    ),
    (
        "legal sufficiency",
        re.compile(
            r"\b(?:provides?|demonstrates?)\s+(?:no\s+)?"
            r"(?P<outcome>legal sufficiency)\b",
            re.IGNORECASE,
        ),
    ),
    (
        "external approval",
        re.compile(
            r"\b(?:has|have|had)\s+(?:no\s+)?"
            r"(?P<outcome>external approval)\b",
            re.IGNORECASE,
        ),
    ),
    (
        "external approval",
        re.compile(
            r"\b(?:is|are|was|were)\s+(?:not\s+)?"
            r"(?P<outcome>externally approved)\b",
            re.IGNORECASE,
        ),
    ),
    (
        "production readiness",
        re.compile(
            r"\b(?:is|are|was|were)\s+(?:not\s+)?"
            r"(?P<outcome>production[- ]ready|ready for production)\b",
            re.IGNORECASE,
        ),
    ),
    (
        "production readiness",
        re.compile(
            r"\b(?:demonstrates?|provides?)\s+(?:no\s+)?"
            r"(?P<outcome>production readiness)\b",
            re.IGNORECASE,
        ),
    ),
    (
        "compliance",
        re.compile(
            r"\bcertif(?:y|ies|ied)\s+(?:no\s+)?"
            r"(?P<outcome>compliance)\b",
            re.IGNORECASE,
        ),
    ),
    (
        "compliance",
        re.compile(
            r"\b(?:is|are|was|were)\s+(?:not\s+)?"
            r"(?P<outcome>compliant)\b",
            re.IGNORECASE,
        ),
    ),
    (
        "certification",
        re.compile(
            r"\b(?:is|are|was|were)\s+(?:not\s+)?"
            r"(?P<outcome>certified)\b",
            re.IGNORECASE,
        ),
    ),
    (
        "equivalence",
        re.compile(
            r"\b(?:is|are|was|were)\s+(?:not\s+)?"
            r"(?P<outcome>equivalent)\b",
            re.IGNORECASE,
        ),
    ),
    (
        "endorsement",
        re.compile(
            r"\b(?:is|are|was|were)\s+(?:not\s+)?"
            r"(?P<outcome>endorsed)\b",
            re.IGNORECASE,
        ),
    ),
    (
        "scheme satisfaction",
        re.compile(
            r"\b(?:Cyber Essentials|external scheme)\s+requirements?\s+"
            r"(?:is|are|was|were)\s+(?:not\s+)?"
            r"(?P<outcome>satisfied)\b"
            r"|\b(?:satisf(?:y|ies|ied|ying))\s+"
            r"(?P<active_outcome>(?:Cyber Essentials|external scheme)\s+"
            r"requirements?)\b",
            re.IGNORECASE,
        ),
    ),
    (
        "scheme satisfaction",
        re.compile(
            r"\b(?:meet(?:s|ing)?|met)\s+"
            r"(?P<outcome>(?:Cyber Essentials|external scheme)\s+"
            r"requirements?)\b",
            re.IGNORECASE,
        ),
    ),
    (
        "compliance",
        re.compile(
            r"\b(?:ensur(?:e|es|ed|ing))\s+"
            r"(?P<outcome>legal compliance)\b"
            r"|\blegal compliance\s+(?:is|was)\s+(?:not\s+)?"
            r"(?P<passive_outcome>ensured)\b",
            re.IGNORECASE,
        ),
    ),
    (
        "compliance",
        re.compile(
            r"\b(?:compl(?:y|ies|ied|ying))\s+with\s+"
            r"(?P<outcome>Cyber Essentials|an?\s+external scheme)\b",
            re.IGNORECASE,
        ),
    ),
    (
        "certification eligibility",
        re.compile(
            r"\b(?:confer(?:s|red|ring)?)\s+"
            r"(?P<outcome>certification eligibility)\b"
            r"|\bcertification eligibility\s+(?:is|was)\s+(?:not\s+)?"
            r"(?P<passive_outcome>conferred)\b",
            re.IGNORECASE,
        ),
    ),
    (
        "certification eligibility",
        re.compile(
            r"\b(?:qualif(?:y|ies|ied|ying))\s+"
            r"(?P<outcome>(?:the\s+)?organization\s+for\s+certification)\b",
            re.IGNORECASE,
        ),
    ),
    (
        "named-authority approval",
        re.compile(
            r"\b(?:has|have|had)\s+(?:no\s+)?"
            r"(?P<outcome>NCSC approval)\b"
            r"|\bNCSC approval\s+(?:is|was)\s+(?:not\s+)?"
            r"(?P<passive_outcome>held)\b",
            re.IGNORECASE,
        ),
    ),
    (
        "named-authority approval",
        re.compile(
            r"\b(?:this|the)\s+profile\s+(?:is|was)\s+(?:not\s+)?"
            r"(?P<outcome>approved\s+by\s+NCSC)\b"
            r"|\bNCSC\s+(?:does\s+(?:not\s+)?)?"
            r"(?P<active_outcome>approves?\s+(?:this|the)\s+profile)\b",
            re.IGNORECASE,
        ),
    ),
    (
        "imported mapping relationship",
        re.compile(
            r"\b(?:Cyber Essentials|NCSC|external scheme)\s+"
            r"(?:provision|requirement|control)\s+[A-Za-z0-9.-]+\s+"
            r"(?:does\s+(?:not\s+)?)?"
            r"(?P<outcome>maps?\s+to\s+"
            r"[A-Z][A-Z0-9]{1,15}-[0-9]{3})\b"
            r"|\b[A-Z][A-Z0-9]{1,15}-[0-9]{3}\s+"
            r"(?:is|was)\s+(?:not\s+)?"
            r"(?P<passive_outcome>mapped\s+from)\s+"
            r"(?:Cyber Essentials|NCSC|external scheme)\s+"
            r"(?:provision|requirement|control)\b",
            re.IGNORECASE,
        ),
    ),
    (
        "imported mapping relationship",
        re.compile(
            r"\b(?:Cyber Essentials|NCSC|external scheme)\s+"
            r"(?:provision|requirement|control)\s+[A-Za-z0-9.-]+\s+"
            r"(?:does\s+(?:not\s+)?)?"
            r"(?P<outcome>(?:supports?|satisf(?:y|ies))"
            r"(?:\s+or\s+(?:support|satisfy))?)\s+"
            r"[A-Z][A-Z0-9]{1,15}-[0-9]{3}\b"
            r"|\b[A-Z][A-Z0-9]{1,15}-[0-9]{3}\s+"
            r"(?:is|was)\s+(?:not\s+)?"
            r"(?P<passive_outcome>(?:supported|satisfied)"
            r"(?:\s+or\s+(?:supported|satisfied))?)\s+by\s+"
            r"(?:Cyber Essentials|NCSC|external scheme)\s+"
            r"(?:provision|requirement|control)\s+[A-Za-z0-9.-]+\b",
            re.IGNORECASE,
        ),
    ),
    (
        "imported mapping relationship",
        re.compile(
            r"\b[A-Z][A-Z0-9]{1,15}-[0-9]{3}\s+"
            r"(?:does\s+(?:not\s+)?)?"
            r"(?P<outcome>(?:supports?|satisf(?:y|ies))"
            r"(?:\s+or\s+(?:support|satisfy))?)\s+"
            r"(?:Cyber Essentials|NCSC|external scheme)\s+"
            r"(?:provision|requirement|control)\s+[A-Za-z0-9.-]+\b"
            r"|\b(?:Cyber Essentials|NCSC|external scheme)\s+"
            r"(?:provision|requirement|control)\s+[A-Za-z0-9.-]+\s+"
            r"(?:is|was)\s+(?:not\s+)?"
            r"(?P<passive_outcome>(?:supported|satisfied)"
            r"(?:\s+or\s+(?:supported|satisfied))?)\s+by\s+"
            r"[A-Z][A-Z0-9]{1,15}-[0-9]{3}\b",
            re.IGNORECASE,
        ),
    ),
    (
        "external outcome import",
        re.compile(
            r"\b(?:suppl(?:y|ies|ied)|import(?:s|ed|ing)?"
            r"|incorporat(?:e|es|ed|ing)|transfer(?:s|red|ring)?)\s+"
            r"(?P<outcome>(?:its|the|an?)\s+external outcomes?)\b"
            r"|\bexternal outcomes?(?:\s+and\s+evidence)?\s+"
            r"(?:is|are|was|were)\s+(?:not\s+)?"
            r"(?P<passive_outcome>imported|supplied|incorporated|transferred)\b",
            re.IGNORECASE,
        ),
    ),
    (
        "compliance",
        re.compile(
            r"\bguarantee(?:s|d|ing)?\s+"
            r"(?P<outcome>legal compliance)\b",
            re.IGNORECASE,
        ),
    ),
    (
        "certification eligibility",
        re.compile(
            r"\bmake(?:s|d|ing)?\s+"
            r"(?P<outcome>(?:the\s+)?organization\s+eligible\s+for\s+"
            r"certification)\b",
            re.IGNORECASE,
        ),
    ),
    (
        "certification",
        re.compile(
            r"\bcertif(?:y|ies|ied|ying)\s+"
            r"(?P<outcome>(?:the\s+)?organization)\b",
            re.IGNORECASE,
        ),
    ),
    (
        "named-authority approval",
        re.compile(
            r"\b(?:this|the)\s+profile\s+has\s+(?:not\s+)?"
            r"(?P<outcome>received\s+NCSC approval)\b"
            r"|\bNCSC\s+has\s+(?:not\s+)?"
            r"(?P<active_outcome>approved\s+(?:this|the)\s+profile)\b",
            re.IGNORECASE,
        ),
    ),
    (
        "imported mapping relationship",
        re.compile(
            r"\b(?:requirement|provision|control)\s+[A-Za-z0-9.-]+\s+of\s+"
            r"(?:Cyber Essentials|NCSC|external scheme)\s+"
            r"(?:does\s+(?:not\s+)?)?"
            r"(?P<outcome>maps?\s+to\s+"
            r"[A-Z][A-Z0-9]{1,15}-[0-9]{3})\b"
            r"|\b(?:Cyber Essentials|NCSC|external scheme)\s+"
            r"(?:provision|requirement|control)\s+[A-Za-z0-9.-]+\s+"
            r"has\s+(?:no\s+)?(?P<active_outcome>a\s+mapping\s+to\s+"
            r"[A-Z][A-Z0-9]{1,15}-[0-9]{3})\b",
            re.IGNORECASE,
        ),
    ),
)
PROFILE_ASSERTION_PATTERNS += (
    (
        "compliance",
        re.compile(
            r"\b(?:guarantee(?:s|d|ing)?|prov(?:e|es|ed|en|ing)|"
            r"ensur(?:e|es|ed|ing))\s+(?P<outcome>legal compliance)\b"
            r"|\blegal compliance\s+(?:is|was|has\s+been|had\s+been)\s+"
            r"(?P<passive_outcome>guaranteed|proved|proven|ensured)\b",
            re.IGNORECASE,
        ),
    ),
    (
        "certification",
        re.compile(
            r"\bcertif(?:y|ies|ied|ying)\s+"
            r"(?P<outcome>(?:the\s+)?organization)\b"
            r"|\b(?:the\s+)?organization\s+"
            r"(?:is|was|has\s+been|had\s+been)\s+"
            r"(?P<passive_outcome>certified)\b",
            re.IGNORECASE,
        ),
    ),
    (
        "certification eligibility",
        re.compile(
            r"\b(?:make|makes|made|making)\s+"
            r"(?P<outcome>(?:the\s+)?organization\s+eligible\s+for\s+"
            r"certification)\b"
            r"|\b(?:the\s+)?organization\s+"
            r"(?:is|was|has\s+been|had\s+been)\s+"
            r"(?P<passive_outcome>made\s+eligible\s+for\s+certification)\b",
            re.IGNORECASE,
        ),
    ),
    (
        "named-authority approval",
        re.compile(
            rf"\bNCSC\s+(?:(?:has|had)\s+)?"
            rf"{BOUNDED_PREDICATE_MODIFIERS}"
            r"(?:approves?|approved|approving)\s+"
            r"(?P<active_outcome>(?:this|the)\s+profile)\b"
            r"|\b(?:this|the)\s+profile\s+"
            rf"(?:(?:is|was)\s+{BOUNDED_PREDICATE_MODIFIERS}"
            rf"|(?:has|had)\s+{BOUNDED_PREDICATE_MODIFIERS}been\s+"
            rf"{BOUNDED_PREDICATE_MODIFIERS})"
            r"(?P<outcome>approved\s+by\s+NCSC)\b"
            r"|\b(?:this|the)\s+profile\s+"
            rf"(?:(?:has|had)\s+)?{BOUNDED_PREDICATE_MODIFIERS}"
            r"(?:receives?|received|receiving)\s+"
            r"(?P<passive_outcome>NCSC approval)\b",
            re.IGNORECASE,
        ),
    ),
    (
        "imported mapping relationship",
        re.compile(
            r"\b(?:Cyber Essentials|NCSC|external scheme)\s+"
            r"(?:provision|requirement|control)\s+[A-Za-z0-9.-]+\s+"
            r"(?:is\s+|was\s+|has\s+been\s+|had\s+been\s+)?"
            r"(?P<outcome>mapped\s+to)\s+"
            r"[A-Z][A-Z0-9]{1,15}-[0-9]{3}\b",
            re.IGNORECASE,
        ),
    ),
)
PROFILE_ASSERTION_PATTERNS += (
    (
        "compliance",
        re.compile(
            r"\bguarantee(?:s|d|ing)?\s+"
            r"(?P<outcome>Cyber Essentials compliance)\b",
            re.IGNORECASE,
        ),
    ),
    (
        "compliance",
        re.compile(
            r"\bCompliance\s+with\s+Cyber Essentials\s+"
            r"(?:(?:is|was)\s+(?:not\s+)?"
            r"|(?:has|had)\s+(?:not\s+)?been\s+)"
            r"(?P<outcome>guaranteed\s+by\s+(?:this|the)\s+profile)\b",
            re.IGNORECASE,
        ),
    ),
    (
        "production readiness",
        re.compile(
            r"\bProduction readiness\s+"
            r"(?:(?:is|was)\s+(?:not\s+)?"
            r"|(?:has|had)\s+(?:not\s+)?been\s+)"
            r"(?P<outcome>confirmed\s+by\s+(?:this|the)\s+profile)\b",
            re.IGNORECASE,
        ),
    ),
    (
        "imported mapping relationship",
        re.compile(
            r"\bEvidence\s+for\s+"
            r"(?P<control>[A-Z][A-Z0-9]{1,15}-[0-9]{3})\s+"
            r"(?:(?:is|was)\s+(?:not\s+)?"
            r"|(?:has|had)\s+(?:not\s+)?been\s+)"
            r"(?P<outcome>provided\s+by)\s+"
            r"(?:Cyber Essentials|NCSC|external scheme)\s+"
            r"(?:provision|requirement|control)\s+[A-Za-z0-9.-]+\b",
            re.IGNORECASE,
        ),
    ),
)
PROFILE_ASSERTION_PATTERNS += (
    (
        "imported mapping relationship",
        re.compile(
            r"\b[A-Z][A-Z0-9]{1,15}-[0-9]{3}\s+"
            rf"(?:(?:does|did|has|had)\s+)?"
            rf"{BOUNDED_PREDICATE_MODIFIERS}"
            r"(?P<outcome>maps?|mapped)\s+from\s+"
            r"(?:Cyber Essentials|NCSC|external scheme)\s+"
            r"(?:provision|requirement|control)\s+[A-Za-z0-9.-]+\b",
            re.IGNORECASE,
        ),
    ),
    (
        "imported mapping relationship",
        re.compile(
            r"\b(?:Cyber Essentials|NCSC|external scheme)\s+"
            r"(?:provision|requirement|control)\s+[A-Za-z0-9.-]+\s+"
            rf"(?:(?:has|had)\s+)?{BOUNDED_PREDICATE_MODIFIERS}"
            r"(?P<outcome>maps?|mapped)\s+to\s+"
            r"[A-Z][A-Z0-9]{1,15}-[0-9]{3}\b",
            re.IGNORECASE,
        ),
    ),
    (
        "imported mapping relationship",
        re.compile(
            r"\b(?:Cyber Essentials|NCSC|external scheme)\s+"
            r"(?:provision|requirement|control)\s+[A-Za-z0-9.-]+\s+"
            rf"(?:(?:is|was)\s+{BOUNDED_PREDICATE_MODIFIERS}"
            rf"|(?:has|had)\s+{BOUNDED_PREDICATE_MODIFIERS}been\s+"
            rf"{BOUNDED_PREDICATE_MODIFIERS})"
            r"(?P<outcome>mapped\s+to)\s+"
            r"[A-Z][A-Z0-9]{1,15}-[0-9]{3}\b",
            re.IGNORECASE,
        ),
    ),
    (
        "imported mapping relationship",
        re.compile(
            r"\b(?:Cyber Essentials|NCSC|external scheme)\s+"
            r"(?:provision|requirement|control)\s+[A-Za-z0-9.-]+\s+"
            r"(?:has|had)\s+(?:no\s+)?"
            r"(?P<outcome>a\s+mapping\s+to)\s+"
            r"[A-Z][A-Z0-9]{1,15}-[0-9]{3}\b",
            re.IGNORECASE,
        ),
    ),
    (
        "imported mapping relationship",
        re.compile(
            r"\b[A-Z][A-Z0-9]{1,15}-[0-9]{3}\s+"
            rf"(?:(?:is|was)\s+{BOUNDED_PREDICATE_MODIFIERS}"
            rf"|(?:has|had)\s+{BOUNDED_PREDICATE_MODIFIERS}been\s+"
            rf"{BOUNDED_PREDICATE_MODIFIERS})"
            r"(?P<outcome>mapped\s+from)\s+"
            r"(?:Cyber Essentials|NCSC|external scheme)\s+"
            r"(?:provision|requirement|control)\s+[A-Za-z0-9.-]+\b",
            re.IGNORECASE,
        ),
    ),
    (
        "imported mapping relationship",
        re.compile(
            r"\b[A-Z][A-Z0-9]{1,15}-[0-9]{3}\s+"
            r"(?:has|had)\s+(?:no\s+)?"
            r"(?P<outcome>a\s+mapping\s+from)\s+"
            r"(?:Cyber Essentials|NCSC|external scheme)\s+"
            r"(?:provision|requirement|control)\s+[A-Za-z0-9.-]+\b",
            re.IGNORECASE,
        ),
    ),
)
PROFILE_ASSERTION_PATTERNS += (
    (
        "compliance",
        re.compile(
            r"\bguarantee(?:s|d|ing)?\s+"
            r"(?P<outcome>compliance\s+with\s+Cyber Essentials)\b",
            re.IGNORECASE,
        ),
    ),
    (
        "endorsement",
        re.compile(
            r"\bNCSC\s+(?:does\s+(?:not\s+)?)?"
            r"(?P<outcome>endorse(?:s|d|ing)?\s+(?:this|the)\s+profile)\b",
            re.IGNORECASE,
        ),
    ),
    (
        "production readiness",
        re.compile(
            r"\bconfirm(?:s|ed|ing)?\s+(?:no\s+)?"
            r"(?P<outcome>production readiness)\b",
            re.IGNORECASE,
        ),
    ),
    (
        "certification eligibility",
        re.compile(
            r"\b(?:the\s+)?organization\s+(?:is|was)\s+(?:not\s+)?"
            r"(?P<outcome>eligible\s+for\s+certification"
            r"(?:\s+under\s+(?:this|the)\s+profile)?)\b",
            re.IGNORECASE,
        ),
    ),
    (
        "named-authority approval",
        re.compile(
            r"\b(?:this|the)\s+profile\s+(?:has|had)\s+(?:not\s+)?"
            r"(?P<outcome>obtained\s+NCSC approval)\b",
            re.IGNORECASE,
        ),
    ),
    (
        "imported mapping relationship",
        re.compile(
            r"\b(?:Cyber Essentials\s+(?:provision|requirement|control)\s+"
            r"[A-Za-z0-9.-]+|[A-Z][A-Z0-9]{1,15}-[0-9]{3})\s+"
            r"(?:does\s+(?:not\s+)?)?"
            r"(?P<outcome>correspond(?:s|ed)?\s+to|"
            r"provid(?:e|es|ed)\s+evidence\s+for)\s+"
            r"(?:Cyber Essentials\s+(?:provision|requirement|control)\s+"
            r"[A-Za-z0-9.-]+|[A-Z][A-Z0-9]{1,15}-[0-9]{3})\b",
            re.IGNORECASE,
        ),
    ),
)
for label, pattern_args in (
    (
        "compliance",
        {
            "active_subject": r"(?:this|the)\s+profile",
            "active_object": r"Cyber Essentials compliance",
            "passive_subject": r"Cyber Essentials compliance",
            "passive_agent": r"by\s+(?:this|the)\s+profile",
            "base": "guarantee",
            "present": "guarantees",
            "past": "guaranteed",
            "participle": "guaranteed",
            "progressive": "guaranteeing",
        },
    ),
    (
        "production readiness",
        {
            "active_subject": r"(?:this|the)\s+profile",
            "active_object": r"production readiness",
            "passive_subject": r"production readiness",
            "passive_agent": r"by\s+(?:this|the)\s+profile",
            "base": "confirm",
            "present": "confirms",
            "past": "confirmed",
            "participle": "confirmed",
            "progressive": "confirming",
        },
    ),
    (
        "imported mapping relationship",
        {
            "active_subject": (
                r"(?:Cyber Essentials|NCSC|external scheme)\s+"
                r"(?:provision|requirement|control)\s+[A-Za-z0-9.-]+"
            ),
            "active_object": (
                r"evidence\s+for\s+"
                r"[A-Z][A-Z0-9]{1,15}-[0-9]{3}"
            ),
            "passive_subject": (
                r"evidence\s+for\s+"
                r"[A-Z][A-Z0-9]{1,15}-[0-9]{3}"
            ),
            "passive_agent": (
                r"by\s+(?:Cyber Essentials|NCSC|external scheme)\s+"
                r"(?:provision|requirement|control)\s+[A-Za-z0-9.-]+"
            ),
            "base": "provide",
            "present": "provides",
            "past": "provided",
            "participle": "provided",
            "progressive": "providing",
        },
    ),
    (
        "imported mapping relationship",
        {
            "active_subject": r"(?:this|the)\s+profile",
            "active_object": (
                r"evidence\s+from\s+"
                r"(?:Cyber Essentials|NCSC|external scheme)\s+"
                r"(?:provision|requirement|control)\s+[A-Za-z0-9.-]+"
            ),
            "passive_subject": (
                r"evidence\s+from\s+"
                r"(?:Cyber Essentials|NCSC|external scheme)\s+"
                r"(?:provision|requirement|control)\s+[A-Za-z0-9.-]+"
            ),
            "passive_agent": r"by\s+(?:this|the)\s+profile",
            "base": "import",
            "present": "imports",
            "past": "imported",
            "participle": "imported",
            "progressive": "importing",
        },
    ),
):
    PROFILE_ASSERTION_PATTERNS += tuple(
        (label, pattern)
        for pattern in bounded_aspect_voice_patterns(**pattern_args)
    )
WEAKENING_PREDICATE = re.compile(
    r"\b(?:replace(?:s|d|ing)?|alter(?:s|ed|ing)?|relax(?:es|ed|ing)?"
    r"|waiv(?:e|es|ed|ing)|weaken(?:s|ed|ing)?|narrow(?:s|ed|ing)?"
    r"|mark(?:s|ed|ing)?|mak(?:e|es|ing)|supersed(?:e|es|ed|ing)"
    r"|lower(?:s|ed|ing)?|render(?:s|ed|ing)?|exempt(?:s|ed|ing)?"
    r"|inapplicable|need\s+not\s+(?:be\s+)?appl(?:y|ied)"
    r"|no\s+longer\s+appl(?:y|ies|ied)"
    r"|does\s+not\s+appl(?:y|ies|ied))\b",
    re.IGNORECASE,
)
PASSIVE_WEAKENING = re.compile(
    r"\b(?P<control>(?:(?:core\s+)?controls?(?:\s+requirements?)?"
    r"|[A-Z][A-Z0-9]{1,15}-[0-9]{3}))\s+"
    rf"(?:{ASPECT_VOICE_AUXILIARY_MATRIX['passive_simple']}"
    rf"|{ASPECT_VOICE_AUXILIARY_MATRIX['passive_perfect']}"
    rf"|{ASPECT_VOICE_AUXILIARY_MATRIX['passive_progressive']})"
    r"(?P<predicate>replaced|waived|made\s+optional|altered|relaxed|weakened|"
    r"narrowed|marked\s+inapplicable|superseded|lowered|rendered\s+optional|"
    r"omitted|skipped|reduced|inapplicable|discontinued)\b",
    re.IGNORECASE,
)
ASPECTUAL_WEAKENING = (
    re.compile(
        r"\b(?P<control>(?:(?:core\s+)?controls?(?:\s+requirements?)?"
        r"|[A-Z][A-Z0-9]{1,15}-[0-9]{3}))\s+"
        r"(?:has|have|had)\s+(?:(?:not|never)\s+)?"
        r"(?P<predicate>ceased\s+to\s+apply|discontinued\s+applying)\b",
        re.IGNORECASE,
    ),
    re.compile(
        r"\b(?P<control>(?:(?:core\s+)?controls?(?:\s+requirements?)?"
        r"|[A-Z][A-Z0-9]{1,15}-[0-9]{3}))\s+"
        r"(?:(?:is|are|was|were)\s+(?:(?:not|never)\s+)?"
        r"|(?:has|have|had)\s+(?:(?:not|never)\s+)?been\s+)"
        r"(?P<predicate>no\s+longer\s+mandatory)\b",
        re.IGNORECASE,
    ),
    re.compile(
        r"\b(?P<control>(?:(?:core\s+)?controls?(?:\s+requirements?)?"
        r"|[A-Z][A-Z0-9]{1,15}-[0-9]{3}))\s+"
        r"(?:has|have|had)\s+"
        r"(?P<predicate>no\s+longer\s+been\s+mandatory)\b",
        re.IGNORECASE,
    ),
)
ADJECTIVAL_WEAKENING = (
    re.compile(
        r"\b(?P<control>(?:(?:core\s+)?controls?(?:\s+requirements?)?"
        r"|[A-Z][A-Z0-9]{1,15}-[0-9]{3}))\s+"
        r"(?P<predicate>(?:(?:shall|must|need)\s+not\s+apply)"
        r"|no\s+longer\s+appl(?:y|ies)"
        r"|(?:is|are)\s+no\s+longer\s+required"
        r"|(?:shall|must|may)\s+be\s+(?:optional|inapplicable)"
        r"|(?:shall|must|may)\s+not\s+be\s+mandatory"
        r"|(?:may|can)\s+be\s+(?:omitted|skipped|reduced)"
        r"|(?:is|are)\s+"
        r"(?:optional|inapplicable|not\s+required|not\s+mandatory)"
        r"|(?:(?:shall|must|may)\s+)?"
        r"(?:cease(?:s)?\s+to\s+apply|discontinue(?:s)?\s+applying))\b",
        re.IGNORECASE,
    ),
    re.compile(
        r"\b(?P<control>(?:(?:core\s+)?controls?"
        r"|[A-Z][A-Z0-9]{1,15}-[0-9]{3}))\s+"
        r"(?:is|are)\s+(?P<predicate>optional|not\s+required)\b",
        re.IGNORECASE,
    ),
    re.compile(
        r"\b(?P<control>[A-Z][A-Z0-9]{1,15}-[0-9]{3})\s+"
        r"(?P<predicate>shall\s+not\s+apply)\b",
        re.IGNORECASE,
    ),
    re.compile(
        r"\bmake(?:s|d|ing)?\s+"
        r"(?P<control>[A-Z][A-Z0-9]{1,15}-[0-9]{3})\s+"
        r"(?P<predicate>not\s+required)\b",
        re.IGNORECASE,
    ),
    re.compile(
        r"\b(?P<predicate>optional)\s+controls?\s+include(?:s)?\s+"
        r"(?P<control>[A-Z][A-Z0-9]{1,15}-[0-9]{3})\b",
        re.IGNORECASE,
    ),
    re.compile(
        r"\b(?P<control>(?:(?:core\s+)?controls?"
        r"|[A-Z][A-Z0-9]{1,15}-[0-9]{3}))\s+"
        r"(?:has|have|had)\s+(?:not\s+)?"
        r"(?P<predicate>become\s+optional)\b",
        re.IGNORECASE,
    ),
    re.compile(
        r"\b(?P<control>(?:(?:core\s+)?controls?"
        r"|[A-Z][A-Z0-9]{1,15}-[0-9]{3}))\s+"
        r"(?:(?:does|do|did)\s+(?:not\s+)?)?"
        r"(?P<predicate>remains?\s+optional)\b",
        re.IGNORECASE,
    ),
)
CONTROL_LANGUAGE = re.compile(
    r"\b(?:(?:core\s+)?controls?(?:\s+requirements?)?"
    r"|[A-Z][A-Z0-9]{1,15}-[0-9]{3})\b",
    re.IGNORECASE,
)
DIRECT_CONTROL_WEAKENING = (
    re.compile(
        r"\b(?:this|the)\s+profile\s+"
        rf"(?:{ASPECT_VOICE_AUXILIARY_MATRIX['active_do']})?"
        r"(?P<predicate>omit(?:s|ted)?|skip(?:s|ped)?|reduc(?:e|es|ed))\s+"
        r"(?:the\s+)?"
        r"(?P<control>(?:(?:core\s+)?controls?"
        r"|[A-Z][A-Z0-9]{1,15}-[0-9]{3}))"
        r"(?:\s+control)?\b",
        re.IGNORECASE,
    ),
    re.compile(
        r"\b(?:this|the)\s+profile\s+"
        rf"{ASPECT_VOICE_AUXILIARY_MATRIX['active_perfect']}"
        r"(?P<predicate>omitted|skipped|reduced)\s+"
        r"(?:the\s+)?"
        r"(?P<control>(?:(?:core\s+)?controls?"
        r"|[A-Z][A-Z0-9]{1,15}-[0-9]{3}))"
        r"(?:\s+control)?\b",
        re.IGNORECASE,
    ),
    re.compile(
        r"\b(?:this|the)\s+profile\s+"
        rf"(?:{ASPECT_VOICE_AUXILIARY_MATRIX['active_progressive']}"
        rf"|{ASPECT_VOICE_AUXILIARY_MATRIX['active_perfect_progressive']})"
        r"(?P<predicate>omitting|skipping|reducing)\s+"
        r"(?:the\s+)?"
        r"(?P<control>(?:(?:core\s+)?controls?"
        r"|[A-Z][A-Z0-9]{1,15}-[0-9]{3}))"
        r"(?:\s+control)?\b",
        re.IGNORECASE,
    ),
)
SAFE_DIRECT_CONTROL_COMPLEMENT = re.compile(
    r"^(?:"
    r"(?:-related)?\s+implementation\s+risks?\s*,?\s+"
    r"while\s+preserving\s+"
    r"(?:every\s+requirement|all\s+requirements)"
    r"|\s+from\s+(?:this|an|the)\s+illustrative\s+list\s*,?\s+"
    r"while\s+retaining\s+it\s+in\s+the\s+complete\s+selection\s+ledger"
    r")\s*$",
    re.IGNORECASE,
)
SAFE_READINESS_DENIAL = re.compile(
    r"\bproduction readiness(?:"
    r"\s+gaps?\s+remain\s+unresolved"
    r"|\s+(?:is\s+(?:still\s+)?not\s+established"
    r"|(?:has|had)\s+(?:"
    r"(?:not|never)\s+been\s+established"
    r"|yet\s+to\s+be\s+established)"
    r"|(?:remains|is|remained)\s+unestablished)"
    r")\b",
    re.IGNORECASE,
)
PREDICATE_NEGATION = re.compile(
    r"\b(?:cannot|can['’]t|doesn['’]t|isn['’]t|must\s+not|never|not"
    r"|by\s+no\s+means|shall\s+not|wasn['’]t|weren['’]t)\b",
    re.IGNORECASE,
)
ASSERTION_SUBJECT = re.compile(
    r"\b(?:(?:this|the)\s+profile|NCSC|legal compliance"
    r"|certification eligibility|(?:the\s+)?organization"
    r"|(?:(?:core\s+)?controls?(?:\s+requirements?)?)"
    r"|[A-Z][A-Z0-9]{1,15}-[0-9]{3}"
    r"|(?:Cyber Essentials|external scheme)\s+"
    r"(?:provision|requirement|control)\s+[A-Za-z0-9.-]+)\b",
    re.IGNORECASE,
)
POST_PREDICATE_NEGATION = re.compile(
    r"\b(?:no|neither)\b",
    re.IGNORECASE,
)
METALINGUISTIC_REFERENCE = re.compile(
    r"\b(?:phrase|words?|text|statement|assertion|claim)\b",
    re.IGNORECASE,
)
METALINGUISTIC_DISCUSSION = re.compile(
    r"\b(?:discuss(?:ed|es|ing)?|quot(?:e|es|ed|ing)"
    r"|prohibit(?:ed|s|ing)?|reject(?:ed|s|ing)?|avoid(?:ed|s|ing)?"
    r"|den(?:y|ies|ied|ying)|false)\b",
    re.IGNORECASE,
)
ASSERTIVE_DISCUSSION = re.compile(
    r"\b(?:assert(?:s|ed|ing)?|affirm(?:s|ed|ing)?"
    r"|confirm(?:s|ed|ing)?|claim(?:s|ed|ing))\b",
    re.IGNORECASE,
)
SOURCE_AUTHORITY_PATTERNS = (
    re.compile(
        r"\b(?:this|the)\s+profile\s+"
        r"(?:is|was|has\s+been|had\s+been)\s+(?:not\s+)?"
        r"(?P<outcome>governed\s+by)\s+"
        r"(?P<source>UK GDPR|Cyber Essentials|NCSC)\b",
        re.IGNORECASE,
    ),
    re.compile(
        r"\b(?P<source>UK GDPR|Cyber Essentials|NCSC)\s+"
        r"(?:is|was)\s+(?:not\s+)?"
        r"(?P<outcome>the\s+authority\s+for\s+(?:this|the)\s+profile\s+"
        r"(?:selection|scope|requirement))\b",
        re.IGNORECASE,
    ),
    re.compile(
        r"\b(?:this|the)\s+profile\s+(?:selection|scope|requirement)\s+"
        r"(?:is|was)\s+(?:not\s+)?"
        r"(?P<outcome>governed\s+by)\s+"
        r"(?P<source>UK GDPR|Cyber Essentials|NCSC)\b",
        re.IGNORECASE,
    ),
    re.compile(
        r"\b(?P<source>UK GDPR|Cyber Essentials|NCSC)\s+"
        r"(?:(?:does|did)\s+(?:not\s+)?)?"
        r"(?P<outcome>govern(?:s|ed)?)\s+(?:this|the)\s+profile"
        r"(?:\s+(?:selection|scope|requirement))?\b",
        re.IGNORECASE,
    ),
    re.compile(
        r"\b(?P<source>it|that source)\s+"
        r"(?:is|was)\s+(?:not\s+)?"
        r"(?P<outcome>the\s+authority\s+for\s+(?:this|the)\s+profile\s+"
        r"(?:selection|scope|requirement))\b",
        re.IGNORECASE,
    ),
    re.compile(
        r"\b(?P<source>[A-Z][A-Za-z0-9&.-]+"
        r"(?:\s+[A-Z][A-Za-z0-9&.-]+){0,5})\s+"
        r"(?:is|was)\s+(?:not\s+)?"
        r"(?P<outcome>the\s+authority\s+for\s+(?:this|the)\s+profile\s+"
        r"(?:selection|scope|requirement))\b",
        re.IGNORECASE,
    ),
    re.compile(
        r"\b(?:this|the)\s+profile\s+(?:selection|scope|requirement)\s+"
        r"(?:is|was)\s+(?:not\s+)?"
        r"(?P<outcome>governed\s+by)\s+"
        r"(?P<source>[A-Z][A-Za-z0-9&.-]+"
        r"(?:\s+[A-Z][A-Za-z0-9&.-]+){0,5})\b",
        re.IGNORECASE,
    ),
    re.compile(
        r"\b(?P<source>[A-Z][A-Za-z0-9&.-]+"
        r"(?:\s+[A-Z][A-Za-z0-9&.-]+){0,5})\s+"
        r"(?:(?:does|did)\s+(?:not\s+)?)?"
        r"(?P<outcome>govern(?:s|ed)?\s+(?:this|the)\s+profile)\b",
        re.IGNORECASE,
    ),
)


@dataclass(frozen=True)
class ProfilePackage:
    """A schema-valid profile package ready for semantic validation."""

    directory: Path
    relative: str
    documents: dict[str, dict[str, object]]


class OperationalProfileError(RuntimeError):
    """A sanitized repository-relative operational validation failure."""


class ContentProfileError(ValueError):
    """A deterministic repository-content validation failure."""


def lstat_mode(path: Path, diagnostic: str) -> int | None:
    """Return an entry mode without suppressing operational stat failures."""
    try:
        return path.lstat().st_mode
    except FileNotFoundError:
        return None
    except OSError as exc:
        raise OperationalProfileError(diagnostic) from exc


def bounded_paths(path: Path, boundary: Path) -> tuple[Path, ...]:
    """Return ``path`` and lexical parents only through ``boundary``."""
    try:
        path.relative_to(boundary)
    except ValueError:
        return ()
    result: list[Path] = []
    current = path
    while True:
        result.append(current)
        if current == boundary:
            return tuple(result)
        current = current.parent


def entry_is_alias(
    path: Path, diagnostic: str, mode: int | None = None
) -> bool:
    """Inspect a path for aliasing while preserving operational failures."""
    observed_mode = mode if mode is not None else lstat_mode(path, diagnostic)
    if observed_mode is None:
        return False
    if stat.S_ISLNK(observed_mode):
        return True
    try:
        return path.is_junction()
    except OSError as exc:
        raise OperationalProfileError(diagnostic) from exc


def reject_duplicate_keys(pairs: list[tuple[str, object]]) -> dict[str, object]:
    """Build a JSON object while refusing duplicate keys."""
    document: dict[str, object] = {}
    for key, value in pairs:
        if key in document:
            raise ValueError(f"duplicate JSON key {key!r}")
        document[key] = value
    return document


def load_json(path: Path) -> object:
    """Load JSON without accepting a lossy duplicate-key overwrite."""
    with path.open(encoding="utf-8") as handle:
        return json.load(handle, object_pairs_hook=reject_duplicate_keys)


def schema_diagnostics(
    schema: dict[str, object], document: object, relative: str
) -> list[str]:
    """Return deterministic Draft 2020-12 diagnostics for one document."""
    try:
        Draft202012Validator.check_schema(schema)
        validator = Draft202012Validator(
            schema,
            format_checker=FormatChecker(),
        )
    except SchemaError as exc:
        return [f"{relative}: invalid validation schema: {exc.message}"]

    try:
        errors = sorted(
            validator.iter_errors(document),
            key=lambda item: (
                tuple(str(part) for part in item.path),
                item.message,
            ),
        )
    except Unresolvable as exc:
        raise OperationalProfileError(
            f"{relative}: cannot resolve validation schema"
        ) from exc

    diagnostics: list[str] = []
    for error in errors:
        location = ".".join(str(part) for part in error.path) or "document"
        diagnostics.append(f"{relative}: {location}: {error.message}")
    return diagnostics


def inventory_profile_packages(
    root: Path,
) -> tuple[tuple[Path, ...], list[str]]:
    """Inventory every profile-domain entry without silently skipping content."""
    profiles = root / "profiles"
    packages: list[Path] = []
    diagnostics: list[str] = []
    try:
        profiles_mode = lstat_mode(
            profiles, "profiles: cannot inspect profile root"
        )
        if profiles_mode is None:
            diagnostics.append("profiles: profile root is missing")
        elif entry_is_alias(
            profiles, "profiles: cannot inspect profile root", profiles_mode
        ):
            diagnostics.append(
                "profiles: profile root must not be a symlink or junction alias"
            )
        elif not stat.S_ISDIR(profiles_mode):
            diagnostics.append("profiles: profile root must be a directory")
        else:
            for domain in sorted(profiles.iterdir(), key=lambda item: item.name):
                relative = domain.relative_to(root).as_posix()
                domain_mode = lstat_mode(
                    domain, f"{relative}: cannot inspect profile inventory entry"
                )
                if domain_mode is None:
                    raise OperationalProfileError(
                        f"{relative}: profile inventory entry disappeared"
                    )
                if entry_is_alias(
                    domain,
                    f"{relative}: cannot inspect profile inventory entry",
                    domain_mode,
                ):
                    if domain.name == "schema":
                        diagnostics.append(
                            f"{relative}: schema root or file must not be a "
                            "symlink or junction alias"
                        )
                    else:
                        diagnostics.append(
                            f"{relative}: profile inventory entry must not be a "
                            "symlink or junction alias"
                        )
                    continue
                if domain.name in PROFILE_ROOT_FILES:
                    if not stat.S_ISREG(domain_mode):
                        diagnostics.append(
                            f"{relative}: profile index entry must be a file"
                        )
                    continue
                if domain.name == "schema":
                    if not stat.S_ISDIR(domain_mode):
                        diagnostics.append(
                            f"{relative}: schema entry must be a directory"
                        )
                    continue
                if not stat.S_ISDIR(domain_mode):
                    diagnostics.append(
                        f"{relative}: unexpected profile inventory entry"
                    )
                    continue
                if not PROFILE_DOMAIN.fullmatch(domain.name):
                    diagnostics.append(
                        f"{relative}: invalid profile domain directory"
                    )
                    continue

                version_entries = tuple(
                    sorted(domain.iterdir(), key=lambda item: item.name)
                )
                if not version_entries:
                    diagnostics.append(
                        f"{relative}: profile domain contains no version entries"
                    )
                for version in version_entries:
                    version_relative = version.relative_to(root).as_posix()
                    version_mode = lstat_mode(
                        version,
                        f"{version_relative}: cannot inspect profile version entry",
                    )
                    if version_mode is None:
                        raise OperationalProfileError(
                            f"{version_relative}: profile version entry disappeared"
                        )
                    if entry_is_alias(
                        version,
                        f"{version_relative}: cannot inspect profile version entry",
                        version_mode,
                    ):
                        diagnostics.append(
                            f"{version_relative}: profile version directory "
                            "must not be a symlink or junction alias"
                        )
                        continue
                    if not stat.S_ISDIR(version_mode):
                        diagnostics.append(
                            f"{version_relative}: unexpected profile version entry"
                        )
                        continue
                    if not SEMVER.fullmatch(version.name):
                        diagnostics.append(
                            f"{version_relative}: invalid profile version directory"
                        )
                        continue
                    manifest = version / PACKAGE_FILES["profile"]
                    manifest_relative = manifest.relative_to(root).as_posix()
                    manifest_mode = lstat_mode(
                        manifest,
                        f"{manifest_relative}: cannot inspect profile manifest",
                    )
                    if manifest_mode is None:
                        diagnostics.append(
                            f"{version_relative}: missing profile manifest "
                            f"{PACKAGE_FILES['profile']}"
                        )
                    elif entry_is_alias(
                        manifest,
                        f"{manifest_relative}: cannot inspect profile manifest",
                        manifest_mode,
                    ):
                        diagnostics.append(
                            f"{manifest_relative}: "
                            "profile manifest must not be a symlink or junction alias"
                        )
                    elif not stat.S_ISREG(manifest_mode):
                        diagnostics.append(
                            f"{manifest_relative}: profile manifest must be a "
                            "regular file"
                        )
                    packages.append(version)
    except OSError as exc:
        raise OperationalProfileError(
            "profiles: cannot inventory profile packages"
        ) from exc

    if not packages:
        diagnostics.append("profiles: no profile packages found")
    return tuple(sorted(packages)), sorted(set(diagnostics))


def discover_profile_packages(root: Path) -> tuple[Path, ...]:
    """Return conventional packages from the fail-closed inventory."""
    return inventory_profile_packages(root)[0]


def safe_component(package: Path, relative: str) -> Path | None:
    """Resolve a normalized POSIX component path only within its package."""
    pure = PurePosixPath(relative)
    if (
        not relative
        or pure.is_absolute()
        or ".." in pure.parts
        or "\\" in relative
        or ":" in relative
        or pure.as_posix() != relative
        or not pure.parts
    ):
        return None
    candidate = package.joinpath(*pure.parts)
    if any(
        entry_is_alias(
            part, "profile package: cannot inspect package component path"
        )
        for part in bounded_paths(candidate, package)
    ):
        return None
    candidate_mode = lstat_mode(
        candidate, "profile package: cannot inspect package component"
    )
    if candidate_mode is None or not stat.S_ISREG(candidate_mode):
        return None
    try:
        candidate.resolve(strict=True).relative_to(package.resolve(strict=True))
    except (FileNotFoundError, ValueError):
        return None
    except OSError as exc:
        raise OperationalProfileError(
            "profile package: cannot resolve package component"
        ) from exc
    return candidate


def package_relative(root: Path, path: Path) -> str:
    return path.relative_to(root).as_posix()


def safe_schema(root: Path, schema_name: str) -> Path | None:
    """Resolve a schema only when it is a real file under ``profiles/schema``."""
    schema_root = root / "profiles" / "schema"
    candidate = schema_root / schema_name
    if any(
        entry_is_alias(
            part, "profiles/schema: cannot inspect validation schema path"
        )
        for part in bounded_paths(candidate, root)
    ):
        return None
    candidate_mode = lstat_mode(
        candidate, "profiles/schema: cannot inspect validation schema"
    )
    if candidate_mode is None or not stat.S_ISREG(candidate_mode):
        return None
    try:
        root_resolved = root.resolve(strict=True)
        schema_root_resolved = schema_root.resolve(strict=True)
        schema_root_resolved.relative_to(root_resolved)
        candidate.resolve(strict=True).relative_to(schema_root_resolved)
    except (FileNotFoundError, ValueError):
        return None
    except OSError as exc:
        raise OperationalProfileError(
            "profiles/schema: cannot resolve validation schema"
        ) from exc
    return candidate


def safe_repository_file(
    root: Path, relative: str, *, expected_root: str
) -> Path:
    """Resolve one normalized regular file beneath a repository subdirectory."""
    pure = PurePosixPath(relative)
    expected = PurePosixPath(expected_root)
    reference_kind = (
        "registry"
        if expected_root == "crosswalks/registry"
        else "snapshot"
    )
    if (
        not relative
        or pure.is_absolute()
        or ".." in pure.parts
        or "\\" in relative
        or ":" in relative
        or pure.as_posix() != relative
        or pure.parts[: len(expected.parts)] != expected.parts
    ):
        raise ValueError(
            f"unsafe or missing {reference_kind} path {relative!r}"
        )
    candidate = root.joinpath(*pure.parts)
    if any(
        entry_is_alias(
            part, f"{expected_root}: cannot inspect repository reference path"
        )
        for part in bounded_paths(candidate, root)
    ):
        raise ValueError(
            f"unsafe or missing {reference_kind} path {relative!r}"
        )
    candidate_mode = lstat_mode(
        candidate, f"{expected_root}: cannot inspect repository reference"
    )
    if candidate_mode is None or not stat.S_ISREG(candidate_mode):
        raise ValueError(
            f"unsafe or missing {reference_kind} path {relative!r}"
        )
    try:
        expected_directory = root.joinpath(*expected.parts).resolve(strict=True)
        candidate.resolve(strict=True).relative_to(expected_directory)
    except (FileNotFoundError, ValueError) as exc:
        raise ValueError(
            f"unsafe or missing {reference_kind} path {relative!r}"
        ) from exc
    except OSError as exc:
        raise OperationalProfileError(
            f"{expected_root}: cannot resolve repository reference"
        ) from exc
    return candidate


def load_schema(root: Path, schema_name: str, diagnostics: list[str]) -> dict[str, object] | None:
    nominal_path = root / "profiles" / "schema" / schema_name
    relative = package_relative(root, nominal_path)
    path = safe_schema(root, schema_name)
    if path is None:
        diagnostics.append(
            f"{relative}: schema root or file is missing, symlinked, or outside profiles/schema"
        )
        return None
    try:
        schema = load_json(path)
    except OSError as exc:
        raise OperationalProfileError(
            f"{relative}: cannot read validation schema"
        ) from exc
    except (json.JSONDecodeError, ValueError) as exc:
        diagnostics.append(f"{relative}: cannot load schema: {exc}")
        return None
    if not isinstance(schema, dict):
        diagnostics.append(f"{relative}: schema root must be an object")
        return None
    return schema


def load_document(
    root: Path,
    package: Path,
    component: str,
    diagnostics: list[str],
) -> dict[str, object] | None:
    filename = PACKAGE_FILES[component]
    path = safe_component(package, filename)
    relative = package_relative(root, package / filename)
    if path is None:
        diagnostics.append(f"{relative}: unsafe or missing package component")
        return None
    try:
        document = load_json(path)
    except OSError as exc:
        raise OperationalProfileError(
            f"{relative}: cannot read package component"
        ) from exc
    except (json.JSONDecodeError, ValueError) as exc:
        diagnostics.append(f"{relative}: cannot load JSON: {exc}")
        return None
    if not isinstance(document, dict):
        diagnostics.append(f"{relative}: document root must be an object")
        return None
    schema = load_schema(root, DOCUMENT_SCHEMAS[component], diagnostics)
    if schema is None:
        return None
    diagnostics.extend(schema_diagnostics(schema, document, relative))
    if any(error.startswith(f"{relative}:") for error in diagnostics):
        return None
    return document


def load_package(
    root: Path, directory: Path, diagnostics: list[str]
) -> ProfilePackage | None:
    """Load one complete, schema-valid package without following aliases."""
    start = len(diagnostics)
    relative = package_relative(root, directory)
    if any(
        entry_is_alias(
            path, f"{relative}: cannot inspect package directory path"
        )
        for path in bounded_paths(directory, root)
    ):
        diagnostics.append(f"{relative}: package directory must not be a symlink")
        return None

    expected_files = set(PACKAGE_FILES.values())
    try:
        actual_entries = {
            path.name: path for path in directory.iterdir()
        }
    except OSError as exc:
        raise OperationalProfileError(
            f"{relative}: cannot inventory package contents"
        ) from exc
    for filename in sorted(expected_files):
        path = actual_entries.get(filename)
        component_relative = f"{relative}/{filename}"
        if path is None:
            diagnostics.append(f"{relative}: missing package file {filename}")
            continue
        mode = lstat_mode(
            path, f"{component_relative}: cannot inspect package component"
        )
        if mode is None:
            diagnostics.append(f"{relative}: missing package file {filename}")
        elif entry_is_alias(
            path,
            f"{component_relative}: cannot inspect package component",
            mode,
        ):
            diagnostics.append(
                f"{component_relative}: package component must not be a "
                "symlink or junction alias"
            )
        elif not stat.S_ISREG(mode):
            diagnostics.append(
                f"{component_relative}: package component must be a regular file"
            )
    for entry, path in sorted(actual_entries.items()):
        if entry in expected_files:
            continue
        entry_relative = f"{relative}/{entry}"
        mode = lstat_mode(
            path, f"{entry_relative}: cannot inspect unlisted package entry"
        )
        if mode is None:
            raise OperationalProfileError(
                f"{entry_relative}: unlisted package entry disappeared"
            )
        if entry_is_alias(
            path,
            f"{entry_relative}: cannot inspect unlisted package entry",
            mode,
        ):
            kind = "symlink or junction alias"
        elif stat.S_ISDIR(mode):
            kind = "entry"
        else:
            kind = "file"
        diagnostics.append(f"{relative}: unlisted package {kind} {entry}")

    documents: dict[str, dict[str, object]] = {}
    profile = load_document(root, directory, "profile", diagnostics)
    if profile is None:
        return None
    documents["profile"] = profile

    components = profile.get("components")
    if not isinstance(components, dict):
        diagnostics.append(f"{relative}/profile.json: components must be an object")
    else:
        for component, filename in PACKAGE_FILES.items():
            if component == "profile":
                continue
            declared = components.get(component)
            if declared != filename:
                diagnostics.append(
                    f"{relative}/profile.json: component {component!r} must be {filename!r}"
                )
            elif safe_component(directory, declared) is None:
                diagnostics.append(
                    f"{relative}/profile.json: unsafe component path {declared!r}"
                )

    for component in DOCUMENT_SCHEMAS:
        if component == "profile":
            continue
        document = load_document(root, directory, component, diagnostics)
        if document is not None:
            documents[component] = document

    if len(diagnostics) != start:
        return None
    return ProfilePackage(directory=directory, relative=relative, documents=documents)


def control_population(root: Path) -> set[str]:
    """Load the authoritative ESAF control identifiers."""
    try:
        catalog = load_json(root / "controls" / "catalog.json")
    except OSError as exc:
        raise OperationalProfileError(
            "controls/catalog.json: cannot read control catalog"
        ) from exc
    except (json.JSONDecodeError, ValueError) as exc:
        raise ContentProfileError(
            "controls/catalog.json: cannot load JSON"
        ) from exc
    if not isinstance(catalog, dict):
        raise ContentProfileError(
            "controls/catalog.json: root must be an object"
        )
    controls = catalog.get("controls")
    if not isinstance(controls, list):
        raise ContentProfileError(
            "controls/catalog.json: controls must be an array"
        )
    identifiers: list[str] = []
    for index, record in enumerate(controls):
        if not isinstance(record, dict) or not isinstance(record.get("id"), str):
            raise ContentProfileError(
                f"controls/catalog.json: controls[{index}] requires a string id"
            )
        identifiers.append(record["id"])
    if len(identifiers) != len(set(identifiers)):
        raise ContentProfileError(
            "controls/catalog.json: contains duplicate control ids"
        )
    return set(identifiers)


def mapping_reference_metadata(
    root: Path, mapping_set_id: str, registry_path: str
) -> dict[str, object]:
    """Resolve declared mapping metadata without conflating editorial state."""
    canonical_registry_path = (
        f"crosswalks/registry/{mapping_set_id}.md"
    )
    if registry_path != canonical_registry_path:
        raise ValueError(
            "registry path must be canonical "
            f"{canonical_registry_path!r}"
        )
    registry_file = safe_repository_file(
        root, registry_path, expected_root="crosswalks/registry"
    )
    try:
        registry, _ = parse_front_matter(registry_file)
    except yaml.YAMLError as exc:
        raise ValueError("cannot parse registry front matter") from exc
    except (UnicodeError, ValueError) as exc:
        raise ValueError(
            f"cannot load registry front matter: {exc}"
        ) from exc
    events = registry.get("events")
    if not isinstance(events, list):
        raise ValueError("registry lifecycle events must be an array")
    catalog = load_json(root / "crosswalks" / "catalog.json")
    if not isinstance(catalog, dict):
        raise ValueError("crosswalks/catalog.json root must be an object")
    mapping_sets = catalog.get("mapping_sets")
    if not isinstance(mapping_sets, list):
        raise ValueError(
            "crosswalks/catalog.json mapping_sets must be an array"
        )
    matches = [
        record
        for record in mapping_sets
        if isinstance(record, dict)
        and isinstance(record.get("metadata"), dict)
        and record["metadata"].get("mapping_set_id") == mapping_set_id
    ]
    if len(matches) != 1:
        raise ValueError(
            f"mapping set {mapping_set_id} does not resolve exactly once"
        )
    record = matches[0]
    metadata = record["metadata"]
    editorial_status = metadata.get("status")
    snapshot_path = record.get("path")
    if not isinstance(editorial_status, str):
        raise ValueError(
            f"mapping set {mapping_set_id} has no editorial status"
        )
    if not isinstance(snapshot_path, str):
        raise ValueError(f"mapping set {mapping_set_id} has no snapshot path")
    snapshot_file = safe_repository_file(
        root, snapshot_path, expected_root="crosswalks/mappings"
    )
    try:
        snapshot, _ = parse_front_matter(snapshot_file)
    except yaml.YAMLError as exc:
        raise ValueError("cannot parse snapshot front matter") from exc
    except (UnicodeError, ValueError) as exc:
        raise ValueError(
            f"cannot load snapshot front matter: {exc}"
        ) from exc
    if registry.get("mapping_set_id") != mapping_set_id:
        raise ValueError(
            f"registry mapping_set_id does not match {mapping_set_id}"
        )
    if snapshot.get("mapping_set_id") != mapping_set_id:
        raise ValueError(
            f"snapshot mapping_set_id does not match {mapping_set_id}"
        )
    snapshot_status = snapshot.get("status")
    if snapshot_status != editorial_status:
        raise ValueError(
            f"snapshot editorial status {snapshot_status} does not match "
            f"catalog {editorial_status}"
        )
    return {
        "mapping_set_id": mapping_set_id,
        "editorial_status": editorial_status,
        "snapshot_path": snapshot_path,
        "registry_events": events,
    }


def mapping_lifecycle_diagnostics(
    metadata: dict[str, object], expected_status: str
) -> list[str]:
    """Validate snapshot editorial state and governed lifecycle separately."""
    diagnostics: list[str] = []
    editorial_status = metadata.get("editorial_status")
    events = metadata.get("registry_events")
    if not isinstance(events, list):
        return ["registry lifecycle events must be an array"]

    expected_editorial = (
        expected_status
        if expected_status in {"draft", "reviewed", "approved"}
        else "approved"
    )
    if editorial_status != expected_editorial:
        diagnostics.append(
            f"expected editorial status {expected_editorial}; "
            f"found {editorial_status}"
        )

    states = [
        event.get("state") if isinstance(event, dict) else None
        for event in events
    ]
    if editorial_status in {"draft", "reviewed"}:
        if events:
            diagnostics.append(
                f"{editorial_status} mapping snapshot requires empty "
                "registry lifecycle events"
            )
        return diagnostics

    if editorial_status == "approved":
        if not events:
            diagnostics.append(
                "approved mapping snapshot requires governed registry "
                "lifecycle events"
            )
            return diagnostics
        if states != list(MAPPING_LIFECYCLE_STATES[: len(states)]):
            diagnostics.append("invalid governed registry lifecycle event prefix")
            return diagnostics
        observed_status = states[-1]
        if observed_status != expected_status:
            diagnostics.append(
                f"expected lifecycle status {expected_status}; "
                f"found {observed_status}"
            )
    return diagnostics


def objects(value: object) -> list[dict[str, object]]:
    """Return the object members of a schema-validated array."""
    if not isinstance(value, list):
        return []
    return [item for item in value if isinstance(item, dict)]


def strings(value: object) -> list[str]:
    """Return the string members of a schema-validated array."""
    if not isinstance(value, list):
        return []
    return [item for item in value if isinstance(item, str)]


def duplicate_identifiers(
    records: list[dict[str, object]], field: str
) -> set[str]:
    identifiers = [
        value
        for record in records
        if isinstance((value := record.get(field)), str)
    ]
    return {
        identifier
        for identifier in identifiers
        if identifiers.count(identifier) > 1
    }


def semantic_diagnostics(
    root: Path, package: ProfilePackage
) -> list[str]:
    """Validate catalog coverage, condition use, identity, and lifecycle pins."""
    diagnostics: list[str] = []
    profile = package.documents["profile"]
    selections_document = package.documents["control_selections"]
    risk_document = package.documents["risk_overlays"]
    evidence_document = package.documents["evidence_expectations"]
    reference_document = package.documents["external_references"]

    expected_profile_id = profile.get("profile_id")
    expected_profile_version = profile.get("profile_version")
    identifier_match = (
        PROFILE_IDENTIFIER.fullmatch(expected_profile_id)
        if isinstance(expected_profile_id, str)
        else None
    )
    if identifier_match is not None and isinstance(
        expected_profile_version, str
    ):
        identifier_version = identifier_match.group("version")
        if identifier_version != expected_profile_version:
            diagnostics.append(
                f"{package.relative}/profile.json: profile_id version "
                f"{identifier_version} does not match profile_version "
                f"{expected_profile_version}"
            )
        if expected_profile_version != package.directory.name:
            diagnostics.append(
                f"{package.relative}/profile.json: profile_version "
                f"{expected_profile_version} does not match profile version "
                f"directory {package.directory.name}"
            )
    for component, document in sorted(package.documents.items()):
        if component == "profile":
            continue
        relative = f"{package.relative}/{PACKAGE_FILES[component]}"
        if document.get("profile_id") != expected_profile_id:
            diagnostics.append(
                f"{relative}: profile_id does not match profile.json"
            )
        if document.get("profile_version") != expected_profile_version:
            diagnostics.append(
                f"{relative}: profile_version does not match profile.json"
            )

    conditions = objects(profile.get("applicability_conditions"))
    risks = objects(risk_document.get("risks"))
    overlays = objects(risk_document.get("overlays"))
    expectations = objects(evidence_document.get("expectations"))
    selections = objects(selections_document.get("selections"))
    duplicate_sets = (
        (
            conditions,
            "condition_id",
            "applicability condition",
            "profile.json",
        ),
        (risks, "risk_id", "risk", "risk-overlays.json"),
        (overlays, "overlay_id", "overlay", "risk-overlays.json"),
        (
            expectations,
            "expectation_id",
            "evidence expectation",
            "evidence-expectations.json",
        ),
    )
    for records, field, label, filename in duplicate_sets:
        for identifier in sorted(duplicate_identifiers(records, field)):
            diagnostics.append(
                f"{package.relative}/{filename}: duplicate {label} {identifier}"
            )

    population = control_population(root)
    selection_ids = [
        value
        for selection in selections
        if isinstance((value := selection.get("control_id")), str)
    ]
    for identifier in sorted(set(selection_ids) - population):
        diagnostics.append(
            f"{package.relative}/control-selections.json: "
            f"unknown control selection {identifier}"
        )
    for identifier in sorted(population - set(selection_ids)):
        diagnostics.append(
            f"{package.relative}/control-selections.json: "
            f"missing control selection {identifier}"
        )
    for identifier in sorted(
        identifier
        for identifier in set(selection_ids)
        if selection_ids.count(identifier) > 1
    ):
        diagnostics.append(
            f"{package.relative}/control-selections.json: "
            f"duplicate control selection {identifier}"
        )
    if len(selection_ids) != len(population):
        diagnostics.append(
            f"{package.relative}/control-selections.json: "
            f"selection record count {len(selection_ids)} does not match "
            f"control population {len(population)}"
        )

    condition_ids = {
        value
        for condition in conditions
        if isinstance((value := condition.get("condition_id")), str)
    }
    condition_users = [
        ("control-selections.json", selection)
        for selection in selections
    ]
    condition_users.extend(
        ("risk-overlays.json", overlay) for overlay in overlays
    )
    condition_users.extend(
        ("evidence-expectations.json", expectation)
        for expectation in expectations
    )
    for filename, record in condition_users:
        for identifier in strings(record.get("activation_conditions")):
            if identifier not in condition_ids:
                diagnostics.append(
                    f"{package.relative}/{filename}: unresolved "
                    f"applicability condition {identifier}"
                )

    for selection in selections:
        status = selection.get("status")
        activation_conditions = strings(
            selection.get("activation_conditions")
        )
        if status == "conditional" and not activation_conditions:
            diagnostics.append(
                f"{package.relative}/control-selections.json: conditional "
                "selection requires activation conditions"
            )
        if status != "conditional" and activation_conditions:
            diagnostics.append(
                f"{package.relative}/control-selections.json: only conditional "
                "selections may use activation conditions"
            )
    for overlay in overlays:
        applicability = overlay.get("applicability")
        activation_conditions = strings(overlay.get("activation_conditions"))
        if applicability == "conditional" and not activation_conditions:
            diagnostics.append(
                f"{package.relative}/risk-overlays.json: conditional overlay "
                "requires activation conditions"
            )
        if applicability != "conditional" and activation_conditions:
            diagnostics.append(
                f"{package.relative}/risk-overlays.json: only conditional "
                "overlays may use activation conditions"
            )

    references = objects(reference_document.get("external_references"))
    reference_ids = [
        value
        for reference in references
        if isinstance((value := reference.get("mapping_set_id")), str)
    ]
    for identifier in sorted(
        identifier
        for identifier in set(reference_ids)
        if reference_ids.count(identifier) > 1
    ):
        diagnostics.append(
            f"{package.relative}/external-references.json: "
            f"duplicate mapping reference {identifier}"
        )

    for reference in references:
        identifier = reference.get("mapping_set_id")
        observed_path = reference.get("registry_path")
        expected_status = reference.get("expected_status")
        if (
            not isinstance(identifier, str)
            or not isinstance(observed_path, str)
            or not isinstance(expected_status, str)
        ):
            continue
        try:
            metadata = mapping_reference_metadata(
                root, identifier, observed_path
            )
        except OSError as exc:
            raise OperationalProfileError(
                f"{observed_path}: cannot read mapping reference metadata"
            ) from exc
        except (UnicodeError, ValueError) as exc:
            diagnostics.append(
                f"{package.relative}/external-references.json: mapping "
                f"{identifier}: {exc}"
            )
            continue
        if metadata.get("mapping_set_id") != identifier:
            diagnostics.append(
                f"{observed_path}: registry mapping_set_id does not match "
                f"{identifier}"
            )
        for lifecycle_diagnostic in mapping_lifecycle_diagnostics(
            metadata, expected_status
        ):
            diagnostics.append(
                f"{observed_path}: {lifecycle_diagnostic}"
            )

    if expected_profile_id == UK_PILOT_PROFILE_ID:
        for identifier in sorted(
            set(reference_ids) - UK_PILOT_MAPPING_REFERENCES
        ):
            diagnostics.append(
                f"{package.relative}/external-references.json: unexpected "
                f"UK pilot mapping reference {identifier}"
            )
        for identifier in sorted(
            UK_PILOT_MAPPING_REFERENCES - set(reference_ids)
        ):
            diagnostics.append(
                f"{package.relative}/external-references.json: missing "
                f"UK pilot mapping reference {identifier}"
            )
        if (
            len(references) != 3
            or set(reference_ids) != UK_PILOT_MAPPING_REFERENCES
        ):
            diagnostics.append(
                f"{package.relative}/external-references.json: UK pilot "
                "mapping references must contain exactly three references"
            )
        for reference in references:
            identifier = reference.get("mapping_set_id")
            if (
                not isinstance(identifier, str)
                or identifier not in UK_PILOT_REGISTRY_PATHS
            ):
                continue
            expected_path = UK_PILOT_REGISTRY_PATHS[identifier]
            if reference.get("registry_path") != expected_path:
                diagnostics.append(
                    f"{package.relative}/external-references.json: mapping "
                    f"{identifier} registry path must be {expected_path!r}"
                )
            if reference.get("expected_status") != "draft":
                diagnostics.append(
                    f"{package.relative}/external-references.json: mapping "
                    f"{identifier} expected_status must be 'draft'"
                )
            if reference.get("reference_use") != "lifecycle_reference_only":
                diagnostics.append(
                    f"{package.relative}/external-references.json: mapping "
                    f"{identifier} reference_use must be "
                    "'lifecycle_reference_only'"
                )
            if reference.get("qualified_review_required") is not True:
                diagnostics.append(
                    f"{package.relative}/external-references.json: mapping "
                    f"{identifier} requires qualified review"
                )
            if reference.get("non_import_statement") != NON_IMPORT_STATEMENT:
                diagnostics.append(
                    f"{package.relative}/external-references.json: mapping "
                    f"{identifier} non_import_statement must be "
                    f"{NON_IMPORT_STATEMENT!r}"
                )
    return sorted(set(diagnostics))


def traceability_diagnostics(package: ProfilePackage) -> list[str]:
    """Validate the closed risk, overlay, and evidence reference graph."""
    diagnostics: list[str] = []
    risk_document = package.documents["risk_overlays"]
    evidence_document = package.documents["evidence_expectations"]
    risks = objects(risk_document.get("risks"))
    overlays = objects(risk_document.get("overlays"))
    expectations = objects(evidence_document.get("expectations"))
    risk_map = {
        record["risk_id"]: record
        for record in risks
        if isinstance(record.get("risk_id"), str)
    }
    overlay_map = {
        record["overlay_id"]: record
        for record in overlays
        if isinstance(record.get("overlay_id"), str)
    }
    evidence_map = {
        record["expectation_id"]: record
        for record in expectations
        if isinstance(record.get("expectation_id"), str)
    }
    population = {
        selection["control_id"]
        for selection in objects(
            package.documents["control_selections"].get("selections")
        )
        if isinstance(selection.get("control_id"), str)
    }

    def check_controls(filename: str, record: dict[str, object]) -> None:
        for identifier in strings(
            record.get("affected_controls", record.get("control_ids"))
        ):
            if identifier not in population:
                diagnostics.append(
                    f"{package.relative}/{filename}: unresolved control "
                    f"reference {identifier}"
                )

    for risk in risks:
        check_controls("risk-overlays.json", risk)
        risk_id = risk.get("risk_id")
        for overlay_id in strings(risk.get("overlay_ids")):
            overlay = overlay_map.get(overlay_id)
            if overlay is None:
                diagnostics.append(
                    f"{package.relative}/risk-overlays.json: unresolved "
                    f"overlay reference {overlay_id}"
                )
            elif isinstance(risk_id, str) and risk_id not in strings(
                overlay.get("risk_ids")
            ):
                diagnostics.append(
                    f"{package.relative}/risk-overlays.json: risk {risk_id} "
                    f"and overlay {overlay_id} must reference each other"
                )

    for overlay in overlays:
        check_controls("risk-overlays.json", overlay)
        overlay_id = overlay.get("overlay_id")
        for risk_id in strings(overlay.get("risk_ids")):
            risk = risk_map.get(risk_id)
            if risk is None:
                diagnostics.append(
                    f"{package.relative}/risk-overlays.json: unresolved risk "
                    f"reference {risk_id}"
                )
            elif isinstance(overlay_id, str) and overlay_id not in strings(
                risk.get("overlay_ids")
            ):
                diagnostics.append(
                    f"{package.relative}/risk-overlays.json: risk {risk_id} "
                    f"and overlay {overlay_id} must reference each other"
                )
        for expectation_id in strings(
            overlay.get("evidence_expectation_ids")
        ):
            expectation = evidence_map.get(expectation_id)
            if expectation is None:
                diagnostics.append(
                    f"{package.relative}/risk-overlays.json: unresolved "
                    "evidence expectation reference "
                    f"{expectation_id}"
                )
            elif isinstance(overlay_id, str) and overlay_id not in strings(
                expectation.get("overlay_ids")
            ):
                diagnostics.append(
                    f"{package.relative}/risk-overlays.json: overlay "
                    f"{overlay_id} and evidence expectation {expectation_id} "
                    "must reference each other"
                )

    for expectation in expectations:
        check_controls("evidence-expectations.json", expectation)
        expectation_id = expectation.get("expectation_id")
        for overlay_id in strings(expectation.get("overlay_ids")):
            overlay = overlay_map.get(overlay_id)
            if overlay is None:
                diagnostics.append(
                    f"{package.relative}/evidence-expectations.json: "
                    f"unresolved overlay reference {overlay_id}"
                )
            elif isinstance(
                expectation_id, str
            ) and expectation_id not in strings(
                overlay.get("evidence_expectation_ids")
            ):
                diagnostics.append(
                    f"{package.relative}/evidence-expectations.json: overlay "
                    f"{overlay_id} and evidence expectation {expectation_id} "
                    "must reference each other"
                )
    return sorted(set(diagnostics))


def walk_json(
    value: object, location: str = "document"
) -> list[tuple[str, str | None, object]]:
    """Flatten JSON values with deterministic dotted locations."""
    found: list[tuple[str, str | None, object]] = []
    if isinstance(value, dict):
        for key in sorted(value):
            child_location = f"{location}.{key}"
            child = value[key]
            found.append((child_location, key, child))
            found.extend(walk_json(child, child_location))
    elif isinstance(value, list):
        for index, child in enumerate(value):
            child_location = f"{location}[{index}]"
            found.append((child_location, None, child))
            found.extend(walk_json(child, child_location))
    return found


def proposition_bounds(
    text: str, index: int
) -> tuple[int, int, list[re.Match[str]]]:
    """Return the proposition containing ``index`` and preceding boundaries."""
    preceding = list(PROFILE_PROPOSITION_BOUNDARY.finditer(text, 0, index))
    start = preceding[-1].end() if preceding else 0
    following = PROFILE_PROPOSITION_BOUNDARY.search(text, index)
    end = following.start() if following else len(text)
    return start, end, preceding


def predicate_is_negated(prefix: str) -> bool:
    """Return whether the local predicate phrase is denied."""
    semantic_prefix = prefix
    while re.search(r",[^,\r\n]*,", semantic_prefix):
        semantic_prefix = re.sub(
            r",[^,\r\n]*,",
            " ",
            semantic_prefix,
            count=1,
        )
    semantic_prefix = re.sub(
        r"\bnot\s+(?=(?:only|merely|just)\b)",
        "",
        semantic_prefix,
        flags=re.IGNORECASE,
    )
    boundaries = [
        boundary
        for boundary in PROFILE_PROPOSITION_BOUNDARY.finditer(semantic_prefix)
        if boundary.group(0) != ","
    ]
    if boundaries:
        semantic_prefix = semantic_prefix[boundaries[-1].end() :]
    subjects = list(ASSERTION_SUBJECT.finditer(semantic_prefix))
    if subjects:
        semantic_prefix = semantic_prefix[subjects[-1].start() :]
    if DIRECT_NEGATED_PROPOSITION.search(semantic_prefix):
        return True
    if re.search(r"\b(?:no|neither)\s*$", semantic_prefix, re.IGNORECASE):
        return True
    for match in PREDICATE_NEGATION.finditer(semantic_prefix):
        trailing = semantic_prefix[match.end() :]
        if re.search(
            r"\b(?:that|which|who|to\s+(?:see|observe|find))\b",
            trailing,
            re.IGNORECASE,
        ):
            continue
        return True
    return False


def postposed_denial(text: str) -> bool:
    """Recognize a denied agent or object after a matched predicate."""
    denial_noun = (
        r"(?:profile|authority|source|body|organization|agency|overlay)"
    )
    bounded_noun = rf"{denial_noun}(?!['’]s|\w)"
    qualifier = (
        r"(?:\s+(?:under|within|in)\s+(?:this|the)\s+"
        r"(?:profile|scheme|document|overlay))?"
    )
    return bool(
        re.match(
            r"^\s*(?:by|from|to)\s+"
            rf"(?:no\s+{bounded_noun}"
            rf"|neither\s+(?:(?:this|the|any)\s+)?{bounded_noun}\s+"
            rf"nor\s+(?:(?:this|the|any)\s+)?{bounded_noun})"
            rf"{qualifier}(?=\s*(?:$|,?\s*"
            r"(?:and|while|whereas|but)\b))",
            text,
            re.IGNORECASE,
        )
    )


def sentence_suffix(text: str, index: int) -> str:
    """Return the remainder of the containing sentence."""
    endings = [
        position
        for delimiter in ".!?;\r\n"
        if (position := text.find(delimiter, index)) >= 0
    ]
    return text[index : min(endings) if endings else len(text)]


def sentence_prefix(text: str, index: int) -> str:
    """Return text from the containing sentence start to ``index``."""
    start = max(text.rfind(delimiter, 0, index) for delimiter in ".!?;\r\n")
    return text[start + 1 : index]


def discussion_head_is_negated(context: str, index: int) -> bool:
    """Return whether the nearest rejection/denial copula is negated."""
    auxiliaries = list(
        re.finditer(
            r"\b(?:is|are|was|were|has|have|had|cannot"
            r"|can['’]t|can)\b",
            context,
            re.IGNORECASE,
        )
    )
    if not auxiliaries:
        return False
    auxiliary = auxiliaries[-1]
    local = context[auxiliary.end() : index]
    return bool(
        auxiliary.group(0).casefold()
        in {"cannot", "can't", "can’t"}
        or re.search(
            r"\b(?:not|never|neither|by\s+no\s+means)\b",
            local,
            re.IGNORECASE,
        )
    )


def assertion_outcome_start(match: re.Match[str]) -> int:
    """Return the asserted outcome start for an alternative-rich pattern."""
    for name in ("outcome", "active_outcome", "passive_outcome"):
        if name in match.re.groupindex and match.start(name) >= 0:
            return match.start(name)
    return match.start()


def occurrence_is_metalinguistic(
    text: str, start: int, end: int
) -> bool:
    """Recognize bounded quotations and explicit non-assertive discussion."""
    if quoted_occurrence_is_metalinguistic(text, start, end):
        return True
    sentence_start = max(
        text.rfind(delimiter, 0, start) for delimiter in ".!?;\r\n"
    )
    sentence_end_candidates = [
        position
        for delimiter in ".!?;\r\n"
        if (position := text.find(delimiter, end)) >= 0
    ]
    sentence_end = (
        min(sentence_end_candidates)
        if sentence_end_candidates
        else len(text)
    )
    context = text[sentence_start + 1 : sentence_end]
    relative_start = start - sentence_start - 1
    relative_end = end - sentence_start - 1
    related_discussion = False
    for discussion in METALINGUISTIC_DISCUSSION.finditer(context):
        if (
            discussion.group(0).casefold()
            in {"false", "rejected", "denied"}
            and discussion_head_is_negated(context, discussion.start())
        ):
            continue
        if (
            discussion.start() >= relative_end
            and not PROFILE_PROPOSITION_BOUNDARY.search(
                context[relative_end : discussion.start()]
            )
        ) or (
            discussion.end() <= relative_start
            and not PROFILE_PROPOSITION_BOUNDARY.search(
                context[discussion.end() : relative_start]
            )
        ):
            related_discussion = True
            break
    affirmative_assertion = False
    for match in ASSERTIVE_DISCUSSION.finditer(context):
        if relative_start <= match.start() and match.end() <= relative_end:
            continue
        boundaries = list(
            PROFILE_PROPOSITION_BOUNDARY.finditer(
                context, 0, match.start()
            )
        )
        clause_start = boundaries[-1].end() if boundaries else 0
        prefix = context[clause_start : match.start()]
        if predicate_is_negated(prefix) or re.search(
            r"\bwithout\s*$", prefix, re.IGNORECASE
        ):
            continue
        affirmative_assertion = True
        break
    return bool(
        METALINGUISTIC_REFERENCE.search(context)
        and related_discussion
        and not affirmative_assertion
    )


def clause_has_negated_profile_assertion(clause: str) -> bool:
    """Return whether one clause contains a directly denied claim family."""
    for _, pattern in PROFILE_ASSERTION_PATTERNS:
        for match in pattern.finditer(clause):
            outcome_start = assertion_outcome_start(match)
            if predicate_is_negated(clause[:outcome_start]):
                return True
    return False


def coordinated_assertion_is_negated(
    text: str,
    match: re.Match[str],
    preceding: list[re.Match[str]],
) -> bool:
    """Propagate denial only across an adjacent assertion joined by or/nor."""
    if not preceding or preceding[-1].group(0).casefold() not in {"or", "nor"}:
        return False
    if text[preceding[-1].end() : match.start()].strip():
        return False
    previous_end = preceding[-1].start()
    previous_start = preceding[-2].end() if len(preceding) > 1 else 0
    return clause_has_negated_profile_assertion(
        text[previous_start:previous_end]
    )


def coordinated_weakening_is_negated(
    text: str, preceding: list[re.Match[str]]
) -> bool:
    """Propagate a weakening denial only across an adjacent ``or``/``nor``."""
    if not preceding or preceding[-1].group(0).casefold() not in {"or", "nor"}:
        return False
    previous_end = preceding[-1].start()
    previous_start = preceding[-2].end() if len(preceding) > 1 else 0
    previous = text[previous_start:previous_end]
    weakening = WEAKENING_PREDICATE.search(previous)
    if weakening is None:
        return False
    return predicate_is_negated(previous[: weakening.start()])


def contains_affirmative_weakening(text: str) -> bool:
    """Recognize weakening predicates with assertion-aware polarity."""
    for weakening in WEAKENING_PREDICATE.finditer(text):
        start, end, preceding = proposition_bounds(text, weakening.start())
        proposition = text[start:end]
        relative_predicate = weakening.start() - start
        prefix = proposition[:relative_predicate]
        control = CONTROL_LANGUAGE.search(proposition)
        if control is None:
            continue
        word = weakening.group(0).casefold()
        if word.startswith(("mak", "render")) and not re.search(
            r"\boptional\b", proposition, re.IGNORECASE
        ):
            continue
        if word.startswith("mark") and not re.search(
            r"\binapplicable\b", proposition, re.IGNORECASE
        ):
            continue
        relative_control_start = control.start()
        relative_control_end = control.end()
        between_start = min(
            relative_predicate + len(weakening.group(0)),
            relative_control_end,
        )
        between_end = max(relative_predicate, relative_control_start)
        between = proposition[between_start:between_end]
        if (
            predicate_is_negated(prefix)
            or POST_PREDICATE_NEGATION.search(between)
            or coordinated_weakening_is_negated(text, preceding)
        ):
            continue
        occurrence_start = min(weakening.start(), start + control.start())
        occurrence_end = max(weakening.end(), start + control.end())
        if occurrence_is_metalinguistic(
            text, occurrence_start, occurrence_end
        ):
            continue
        if postposed_denial(sentence_suffix(text, weakening.end())):
            continue
        return True
    for pattern in DIRECT_CONTROL_WEAKENING:
        for weakening in pattern.finditer(text):
            predicate_start = weakening.start("predicate")
            if predicate_is_negated(
                sentence_prefix(text, predicate_start)
            ):
                continue
            if occurrence_is_metalinguistic(
                text, weakening.start(), weakening.end()
            ):
                continue
            if SAFE_DIRECT_CONTROL_COMPLEMENT.fullmatch(
                sentence_suffix(text, weakening.end())
            ):
                continue
            if postposed_denial(sentence_suffix(text, weakening.end())):
                continue
            return True
    for weakening in PASSIVE_WEAKENING.finditer(text):
        predicate_start = weakening.start("predicate")
        start, _, _ = proposition_bounds(text, predicate_start)
        if predicate_is_negated(text[start:predicate_start]):
            continue
        if occurrence_is_metalinguistic(
            text, weakening.start(), weakening.end()
        ):
            continue
        if postposed_denial(sentence_suffix(text, weakening.end())):
            continue
        return True
    for pattern in ASPECTUAL_WEAKENING:
        for weakening in pattern.finditer(text):
            predicate_start = weakening.start("predicate")
            if predicate_is_negated(
                sentence_prefix(text, predicate_start)
            ):
                continue
            if occurrence_is_metalinguistic(
                text, weakening.start(), weakening.end()
            ):
                continue
            if postposed_denial(sentence_suffix(text, weakening.end())):
                continue
            return True
    for pattern in ADJECTIVAL_WEAKENING:
        for weakening in pattern.finditer(text):
            predicate_start = weakening.start("predicate")
            if predicate_is_negated(
                sentence_prefix(text, predicate_start)
            ):
                continue
            if postposed_denial(sentence_suffix(text, weakening.end())):
                continue
            if occurrence_is_metalinguistic(
                text, weakening.start(), weakening.end()
            ):
                continue
            return True
    return False


def asserted_profile_phrases(text: str) -> list[str]:
    """Reuse ESAF-1500 assertion context for profile-specific claim phrases."""
    safe_readiness = list(SAFE_READINESS_DENIAL.finditer(text))
    generic_text = SAFE_READINESS_DENIAL.sub(
        lambda match: re.sub(
            r"\bproduction readiness\b",
            "readiness status",
            match.group(0),
            flags=re.IGNORECASE,
        ),
        text,
    )
    assertions = list(asserted_prohibited_phrases(generic_text))
    for label, pattern in PROFILE_ASSERTION_PATTERNS:
        for match in pattern.finditer(text):
            outcome_start = assertion_outcome_start(match)
            readiness_phrase = (
                re.search(
                    r"\bproduction readiness\b",
                    match.group(0),
                    re.IGNORECASE,
                )
                if label == "production readiness"
                else None
            )
            readiness_start = (
                match.start() + readiness_phrase.start()
                if readiness_phrase is not None
                else outcome_start
            )
            readiness_end = (
                match.start() + readiness_phrase.end()
                if readiness_phrase is not None
                else match.end()
            )
            if (
                label == "production readiness"
                and any(
                    safe.start() <= readiness_start
                    and readiness_end <= safe.end()
                    for safe in safe_readiness
                )
            ):
                continue
            _, _, preceding = proposition_bounds(text, outcome_start)
            if (
                predicate_is_negated(sentence_prefix(text, outcome_start))
                or postposed_denial(sentence_suffix(text, match.end()))
                or coordinated_assertion_is_negated(
                    text, match, preceding
                )
            ):
                continue
            if occurrence_is_metalinguistic(
                text, match.start(), match.end()
            ):
                continue
            assertions.append(label)
    return assertions


def source_authority_is_excluded(
    source: str, excluded_sources: list[str]
) -> bool:
    """Resolve a bounded named source to an excluded source declaration."""
    normalized_source = source.casefold()
    normalized_exclusions = " ".join(excluded_sources).casefold()
    if any(
        normalized_source in excluded.casefold()
        or excluded.casefold() in normalized_source
        for excluded in excluded_sources
    ):
        return True
    if normalized_source == "uk gdpr":
        return bool(
            re.search(
                r"\b(?:laws?|regulations?|regulatory)\b",
                normalized_exclusions,
            )
        )
    if normalized_source in {"cyber essentials", "ncsc"}:
        return bool(
            re.search(
                r"\b(?:assurance|certification|external|mapping|substantive)\b",
                normalized_exclusions,
            )
        )
    return False


def matched_source_is_excluded(
    text: str,
    match: re.Match[str],
    excluded_sources: list[str],
) -> bool:
    """Resolve a named source or bounded pronoun antecedent."""
    source = match.group("source")
    if source.casefold() not in {"it", "that source"}:
        return source_authority_is_excluded(source, excluded_sources)
    return any(
        source_authority_is_excluded(candidate, excluded_sources)
        for candidate in ("UK GDPR", "Cyber Essentials", "NCSC")
        if re.search(
            rf"\b{re.escape(candidate)}\b",
            text[: match.start()],
            re.IGNORECASE,
        )
    )


def contains_affirmative_source_authority(
    text: str, excluded_sources: list[str]
) -> bool:
    """Reject affirmative authority claims for declared excluded sources."""
    profile_selection = (
        r"(?:(?:this|the)\s+profile\s+"
        r"(?:selection(?:\s+for\s+"
        r"[A-Z][A-Z0-9]{1,15}-[0-9]{3})?|scope|requirement)"
        r"|(?:this|the)\s+"
        r"[A-Z][A-Z0-9]{1,15}-[0-9]{3}\s+profile\s+selection)"
    )
    declared_passive_patterns = tuple(
        re.compile(
            r"\b(?:this|the)\s+profile\s+"
            rf"(?:(?:is|was)\s+{BOUNDED_PREDICATE_MODIFIERS}"
            rf"|(?:has|had)\s+{BOUNDED_PREDICATE_MODIFIERS}been\s+"
            rf"{BOUNDED_PREDICATE_MODIFIERS})"
            r"(?P<outcome>governed\s+by)\s+"
            rf"(?P<source>{re.escape(source)})(?!\w)",
            re.IGNORECASE,
        )
        for source in excluded_sources
        if source.strip()
    )
    declared_supply_patterns = tuple(
        pattern
        for source in excluded_sources
        if source.strip()
        for forms in (
            {
                "base": "supply",
                "present": "supplies",
                "past": "supplied",
                "participle": "supplied",
                "progressive": "supplying",
            },
            {
                "base": "provide",
                "present": "provides",
                "past": "provided",
                "participle": "provided",
                "progressive": "providing",
            },
        )
        for pattern in bounded_aspect_voice_patterns(
            active_subject=(
                rf"(?P<source>{re.escape(source)})(?!\w)"
            ),
            active_object=profile_selection,
            passive_subject=profile_selection,
            passive_agent=(
                rf"by\s+(?P<source>{re.escape(source)})(?!\w)"
            ),
            **forms,
        )
    )
    declared_derivation_patterns = tuple(
        pattern
        for source in excluded_sources
        if source.strip()
        for pattern in (
            re.compile(
                rf"\b{profile_selection}\s+"
                rf"(?:{ASPECT_VOICE_AUXILIARY_MATRIX['passive_simple']}"
                rf"|{ASPECT_VOICE_AUXILIARY_MATRIX['passive_perfect']})"
                r"(?P<outcome>derived)\s+from\s+"
                rf"(?P<source>{re.escape(source)})(?!\w)",
                re.IGNORECASE,
            ),
            re.compile(
                rf"\b(?P<source>{re.escape(source)})(?!\w)\s+"
                rf"(?:{ASPECT_VOICE_AUXILIARY_MATRIX['passive_simple']}"
                rf"|{ASPECT_VOICE_AUXILIARY_MATRIX['passive_perfect']})"
                r"(?P<outcome>the\s+source\s+for\s+"
                rf"{profile_selection})\b",
                re.IGNORECASE,
            ),
            re.compile(
                r"\b(?:this|the)\s+profile\s+"
                r"(?:selection|scope|requirement)\s+"
                r"(?:(?:does|did)\s+(?:not\s+)?)?"
                r"(?P<outcome>deriv(?:e|es|ed)\s+from)\s+"
                rf"(?P<source>{re.escape(source)})(?!\w)",
                re.IGNORECASE,
            ),
            re.compile(
                rf"\b{profile_selection}\s+"
                rf"(?:{ASPECT_VOICE_AUXILIARY_MATRIX['passive_simple']}"
                rf"|{ASPECT_VOICE_AUXILIARY_MATRIX['passive_perfect']})"
                r"(?P<outcome>based\s+on)\s+"
                rf"(?P<source>{re.escape(source)})(?!\w)",
                re.IGNORECASE,
            ),
        )
    )
    for pattern in (
        *declared_passive_patterns,
        *declared_supply_patterns,
        *declared_derivation_patterns,
        *SOURCE_AUTHORITY_PATTERNS,
    ):
        for match in pattern.finditer(text):
            if not matched_source_is_excluded(
                text, match, excluded_sources
            ):
                continue
            outcome_start = match.start("outcome")
            if predicate_is_negated(sentence_prefix(text, outcome_start)):
                continue
            if occurrence_is_metalinguistic(
                text, match.start(), match.end()
            ):
                continue
            return True
    return False


def source_boundary_diagnostics(
    package: ProfilePackage, controls: set[str]
) -> list[str]:
    """Validate declared risk sources and excluded-authority assertions."""
    diagnostics: list[str] = []
    profile = package.documents["profile"]
    boundary = profile.get("source_boundary")
    permitted_sources: list[str] = []
    excluded_sources: list[str] = []
    if isinstance(boundary, dict):
        permitted_sources = strings(boundary.get("permitted_sources"))
        excluded_sources = strings(boundary.get("excluded_sources"))
    allowed_source_basis = controls | set(permitted_sources)
    risks = objects(package.documents["risk_overlays"].get("risks"))
    relative = f"{package.relative}/{PACKAGE_FILES['risk_overlays']}"
    for risk_index, risk in enumerate(risks):
        for source_index, source_basis in enumerate(
            strings(risk.get("source_basis"))
        ):
            if source_basis not in allowed_source_basis:
                diagnostics.append(
                    f"{relative}: document.risks[{risk_index}]."
                    f"source_basis[{source_index}]: unresolved risk "
                    f"source basis {source_basis!r}"
                )

    for component, document in sorted(package.documents.items()):
        filename = PACKAGE_FILES[component]
        component_relative = f"{package.relative}/{filename}"
        for location, _, value in walk_json(document):
            if not isinstance(value, str):
                continue
            if contains_affirmative_source_authority(
                value, excluded_sources
            ):
                diagnostics.append(
                    f"{component_relative}: {location}: prohibited source "
                    "authority language"
                )

    readme_relative = f"{package.relative}/{PACKAGE_FILES['readme']}"
    try:
        readme = (package.directory / PACKAGE_FILES["readme"]).read_text(
            encoding="utf-8"
        )
    except UnicodeError:
        return sorted(set(diagnostics))
    if contains_affirmative_source_authority(readme, excluded_sources):
        diagnostics.append(
            f"{readme_relative}: prohibited source authority language"
        )
    return sorted(set(diagnostics))


def claim_diagnostics(package: ProfilePackage) -> list[str]:
    """Reject imported outcomes, local scales, weakening, and positive claims."""
    diagnostics: list[str] = []
    for component, document in sorted(package.documents.items()):
        filename = PACKAGE_FILES[component]
        relative = f"{package.relative}/{filename}"
        for location, key, value in walk_json(document):
            normalized = (
                key.casefold().replace("_", "-")
                if isinstance(key, str)
                else None
            )
            if (
                component == "external_references"
                and normalized in EXTERNAL_IMPORT_FIELDS
            ):
                diagnostics.append(
                    f"{relative}: {location}: prohibited "
                    f"external-reference field {key!r}"
                )
            if normalized in LOCAL_MATURITY_FIELDS:
                diagnostics.append(
                    f"{relative}: {location}: prohibited profile-local "
                    f"maturity field {key!r}"
                )
            if not isinstance(value, str):
                continue
            if contains_affirmative_weakening(value):
                diagnostics.append(
                    f"{relative}: {location}: prohibited control weakening "
                    "language"
                )
            for phrase in asserted_profile_phrases(value):
                diagnostics.append(
                    f"{relative}: {location}: prohibited assertion "
                    f"{phrase!r}"
                )

    readme_relative = f"{package.relative}/{PACKAGE_FILES['readme']}"
    try:
        readme = (package.directory / PACKAGE_FILES["readme"]).read_text(
            encoding="utf-8"
        )
    except UnicodeError:
        diagnostics.append(
            f"{readme_relative}: cannot decode UTF-8 content"
        )
        return sorted(set(diagnostics))
    if contains_affirmative_weakening(readme):
        diagnostics.append(
            f"{readme_relative}: prohibited control weakening language"
        )
    for phrase in asserted_profile_phrases(readme):
        diagnostics.append(
            f"{readme_relative}: prohibited assertion {phrase!r}"
        )
    return sorted(set(diagnostics))


def validate(root: Path = ROOT) -> list[str]:
    """Return all deterministic content diagnostics for discovered packages."""
    diagnostics: list[str] = []
    try:
        packages, diagnostics = inventory_profile_packages(root)
        for directory in packages:
            package = load_package(root, directory, diagnostics)
            if package is None:
                continue
            diagnostics.extend(semantic_diagnostics(root, package))
            diagnostics.extend(traceability_diagnostics(package))
            diagnostics.extend(
                source_boundary_diagnostics(
                    package, control_population(root)
                )
            )
            diagnostics.extend(claim_diagnostics(package))
        return sorted(set(diagnostics))
    except ContentProfileError as exc:
        diagnostics.append(str(exc))
        return sorted(set(diagnostics))
    except OperationalProfileError:
        raise
    except OSError as exc:
        raise OperationalProfileError(
            "profiles: repository content could not be read"
        ) from exc


def main(argv: Sequence[str] | None = None, *, root: Path | None = None) -> int:
    """Run profile validation in check mode."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", required=True)
    try:
        arguments = parser.parse_args(argv)
    except SystemExit as exc:
        return int(exc.code)
    if not arguments.check:
        return 2

    try:
        validation_root = root if root is not None else ROOT
        diagnostics = validate(validation_root)
        package_count = len(discover_profile_packages(validation_root))
    except OperationalProfileError as exc:
        print(f"Profile validation could not run: {exc}", file=sys.stderr)
        return 2
    except Exception:
        print(
            "Profile validation could not run: unexpected operational error",
            file=sys.stderr,
        )
        return 2
    if diagnostics:
        print(
            f"Profile validation failed with {len(diagnostics)} error(s):",
            file=sys.stderr,
        )
        for diagnostic in diagnostics:
            print(f"- {diagnostic}", file=sys.stderr)
        return 1
    print(f"Successfully validated {package_count} profile package(s).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
