# ESAF licensing model design

## Purpose

ESAF uses separate licenses for standards content and software. The model permits commercial adoption, modification, translation, implementation, and redistribution while preserving attribution, third-party terms, and the distinction between official ESAF publications and modified works.

The copyright notice names `ESAF Project Maintainers`. Hearst is not a copyright holder, project owner, sponsor, or endorser.

## License model

Original ESAF standards content is licensed under the Creative Commons Attribution 4.0 International license (`CC-BY-4.0`). Software and implementation assets are licensed under the Apache License, Version 2.0 (`Apache-2.0`).

The root `LICENSE` contains the unmodified CC BY 4.0 legal code so GitHub can identify the repository's primary content license. The complete Apache 2.0 text is stored at `LICENSES/Apache-2.0.txt`. `LICENSE_SCOPE.md` defines which license applies to each path. A more specific path rule overrides a broader rule.

### Apache 2.0 paths

- `.github/`
- `tools/`
- `tests/`
- `requirements-dev.txt`
- `assessment/schema/`
- `controls/schema/`
- `crosswalks/schema/`

### CC BY 4.0 paths

Original ESAF material in every other path is licensed under CC BY 4.0. This includes normative publications, control content, architecture content, assessment guidance and examples, crosswalk records and catalogs, templates, project documentation, and generated publications.

License texts and third-party material are not relicensed by these path rules.

## Attribution and notices

`NOTICE` identifies:

```text
Copyright 2026 ESAF Project Maintainers
```

It also provides a preferred attribution for standards content:

```text
Enterprise Secure AI Framework (ESAF), copyright 2026 ESAF Project Maintainers, licensed under CC BY 4.0. Changes were made where applicable. Use does not imply endorsement by the ESAF Project Maintainers.
```

CC BY 4.0 controls the legal attribution obligation. The preferred wording is guidance and does not add a license restriction.

## Third-party material

`THIRD_PARTY_NOTICES.md` records material that remains subject to separate terms. The initial notice covers National Cyber Security Centre Crown copyright material reused under the Open Government Licence v3.0. Existing mapping-level rights statements remain authoritative for their exact permitted and prohibited elements.

The ESAF licenses apply only to rights held by the ESAF Project Maintainers or contributed with authority to license. They do not relicense third-party text, marks, logos, imagery, or other excluded material.

## Trademarks and conformance

`TRADEMARKS.md` separates copyright permission from project identity. It permits truthful references to ESAF and unmodified ESAF publications. It prohibits implying sponsorship, endorsement, official status, certification, or conformance without authorization.

Modified works may describe their relationship to ESAF but may not present themselves as official ESAF publications. The policy does not create a certification program or assert that any ESAF mark is registered.

## Contributions

`CONTRIBUTING.md` states that a contribution is licensed under the license applicable to its target path unless the contributor and project agree otherwise in writing. Contributors must have authority to submit the material. Third-party material must be identified and accepted under the existing rights-review process.

The contribution terms do not transfer copyright ownership. Apache 2.0 supplies its patent terms for contributions to Apache-licensed paths. This change does not create a separate contributor license agreement or patent policy for standards content.

## Repository presentation

`README.md` replaces the unfinished-license warning with a concise dual-license summary and links to `LICENSE`, `LICENSE_SCOPE.md`, `NOTICE`, `THIRD_PARTY_NOTICES.md`, and `TRADEMARKS.md`.

GitHub may display CC BY 4.0 as the repository license because the root `LICENSE` contains that license's unmodified legal code. The scope document remains controlling for Apache-licensed paths.

## Validation

Focused tests shall verify:

- the root `LICENSE` contains the complete official CC BY 4.0 English legal code;
- `LICENSES/Apache-2.0.txt` contains the complete official Apache 2.0 text;
- the scope document lists every Apache path and gives CC BY 4.0 as the default for original ESAF material;
- the notice names `ESAF Project Maintainers` and does not name Hearst as a rights holder;
- README and contribution language match the license model;
- third-party and trademark exclusions are present;
- placeholder or unfinished-license language is absent; and
- no authoritative crosswalk record or generated catalog changes as a side effect.

The existing repository-validation workflow shall run when any licensing,
notice, trademark, README, or contribution-policy file changes. Its exact
path-filter contract test shall include those files.

The full repository test suite and `git diff --check` shall pass. License texts shall be obtained from the official licensors without local rewriting.

## Non-goals

This change does not:

- create an ESAF certification scheme;
- grant rights in third-party content, patents, trademarks, or logos beyond the stated terms;
- claim that ESAF or any ESAF mark is registered;
- assign contributor copyright to the ESAF Project Maintainers;
- add a noncommercial, no-derivatives, or share-alike restriction; or
- modify normative ESAF requirements, controls, mappings, schemas, or generated catalogs.
