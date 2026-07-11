# ESAF Architecture Overlays

## Purpose

An overlay adds or strengthens requirements for a recurring context without copying or weakening a base architecture pattern. Overlays support consistent tailoring across patterns.

## Overlay categories

| Category | Examples |
|---|---|
| Risk and impact | Business-critical, mission-critical, safety-related, rights-affecting |
| Deployment | Public cloud, private cloud, on-premises, edge, hybrid, managed service |
| Data | Regulated, confidential, payment, health, workforce, cross-border |
| Exposure | Internal, partner, customer-facing, public, administrative |
| Autonomy | Advisory, human-approved action, supervised action, bounded autonomy |
| Obligation | Sector, jurisdiction, contract, assurance, records, accessibility |

## Overlay record

Each overlay shall identify:

- overlay ID, title, status, version, and owner;
- applicability criteria and exclusions;
- base patterns to which it may apply;
- added or strengthened controls and control points;
- architecture decisions and parameters;
- evidence and assessment expectations;
- conflicts, precedence, review triggers, and change history.

## Application rules

1. Select a base pattern before selecting an overlay.
2. Apply every overlay whose criteria match the capability unless an approved decision explains non-applicability.
3. Where overlays conflict, apply the more protective requirement until an authorized decision resolves the conflict.
4. Record overlay identifiers and versions in the capability architecture.
5. Reassess overlays upon changes to risk, deployment, data, exposure, autonomy, jurisdiction, or obligation.

An overlay cannot establish external compliance or waive an ESAF requirement.
