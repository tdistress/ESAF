# ESAF Architecture Principles

These principles apply to every ESAF reference pattern and in-scope capability design.

## 1. Identity-centered access

Every human, service, workload, API, model-management process, and agent crossing a trust boundary shall be attributable and authorized. Designs shall avoid shared identities and implicit authority. Primary control families: `IAM`, `AGT`, and `API`.

## 2. Explicit trust boundaries

Components, actors, flows, control points, providers, and responsibility changes shall be documented. Trust shall not be inferred solely from network location or supplier status. Primary control families: `ARC`, `INF`, and `GOV`.

## 3. Data authorization before processing

Data classification, purpose, source authorization, residency, retention, and handling obligations shall follow information through ingestion, retrieval, inference, output, feedback, logging, and retirement. Primary control families: `DAT`, `CMP`, and `MOD`.

## 4. Least agency

AI systems and agents shall receive only the tools, permissions, memory, time, data, delegation, and resources required for an approved purpose. Primary control families: `AGT`, `IAM`, and `APP`.

## 5. Policy enforcement at boundaries

Identity, data, instruction, action, provider, and administrative boundary crossings shall invoke risk-appropriate authentication, authorization, validation, inspection, and logging. Primary control families: `API`, `APP`, `DAT`, and `MON`.

## 6. Defense in depth

No single gateway, filter, model, provider, prompt, or human review shall be treated as a complete safeguard. Designs shall use independent preventive, detective, responsive, and recovery measures. Primary control families: `APP`, `MOD`, `INF`, `MON`, and `OPS`.

## 7. Observable and attributable operation

Material requests, retrievals, model calls, decisions, approvals, tool actions, changes, and failures shall produce protected and correlated evidence appropriate to risk. Primary control families: `MON`, `AUD`, and `OPS`.

## 8. Safe failure and reversibility

Designs shall define bounded retry, fallback, isolation, suspension, rollback, recovery, and retirement behavior. Failure shall not expand authority or silently degrade required safeguards. Primary control families: `OPS`, `ARC`, and `AGT`.

## 9. Portable integration

Interfaces, formats, dependencies, configurations, and provider responsibilities shall be documented sufficiently to govern change, replace services, export required records, and execute an exit plan. Primary control families: `API`, `MOD`, `CMP`, and `ARC`.

## 10. Human accountability

Architecture shall preserve assigned human ownership, decision rights, intervention, challenge, and appeal appropriate to impact. Automation shall not obscure accountability. Primary control families: `GOV`, `RSK`, `AGT`, and `EDU`.
