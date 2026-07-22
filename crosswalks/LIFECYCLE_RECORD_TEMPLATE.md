---
schema_version: 1.0.0
mapping_set_id: example-authority--example-standard--2026.1--esaf-0.5-beta--1.0.0
snapshot_digest: aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa
events:
  - event_id: evt-001
    state: approved
    date: "2026-07-13"
    actor: reviewer-1
    reason: Café
    approval_reference: APR-001
    previous_event_digest: "0000000000000000000000000000000000000000000000000000000000000000"
    event_digest: dce6853af1e45395304b66d057807375f8c0d61e7393a725f4776e9fba00b811
  - event_id: evt-002
    state: published
    date: "2026-07-14"
    actor: publisher-1
    reason: Initial publication.
    predecessor_id: example-authority--example-standard--2025.1--esaf-0.5-beta--1.0.0
    previous_event_digest: dce6853af1e45395304b66d057807375f8c0d61e7393a725f4776e9fba00b811
    event_digest: 4c614083713b08a7ae9b92bfd9c43543c4962fd213797c6942d942c210642979
  - event_id: evt-003
    state: deprecated
    date: "2027-01-15"
    actor: publisher-1
    reason: Replaced by a reviewed successor.
    successor_id: example-authority--example-standard--2026.1--esaf-0.5-beta--1.1.0
    previous_event_digest: 4c614083713b08a7ae9b92bfd9c43543c4962fd213797c6942d942c210642979
    event_digest: f346f3ddd729240c30622a494e9f4f00b72d9117bbec032eed5c077cb9539c81
  - event_id: evt-004
    state: retired
    date: "2027-07-15"
    actor: publisher-1
    reason: Historical retention only; successor remains available.
    successor_id: example-authority--example-standard--2026.1--esaf-0.5-beta--1.1.0
    previous_event_digest: f346f3ddd729240c30622a494e9f4f00b72d9117bbec032eed5c077cb9539c81
    event_digest: 7d966364ead82eee2329e829e04aa83e46f15c4f4501fbfa349ed66a29733ff0
---
# Lifecycle record authoring template

This non-authoritative example demonstrates the complete append-only chain. Its first event is the frozen Unicode NFC digest vector: the displayed `Café` reason hashes to `dce6853af1e45395304b66d057807375f8c0d61e7393a725f4776e9fba00b811`, including when authored with a decomposed accent before normalization.

Draft and reviewed mapping sets use the same lifecycle-record metadata with `events: []`. Only an approved snapshot begins this demonstrated event chain. Every predecessor or successor in an authoritative record shall resolve to another mapping set and shall be reciprocated by that set's mapping metadata and lifecycle record.

Replace the example identifiers, dates, actors, snapshot digest, linkage, reasons, approval reference, and every recomputed event digest before creating an authoritative registry record.
