<!--
Sync Impact Report
- Version change: unversioned scaffold -> 1.0.0
- Modified principles: five scaffold placeholders -> Edge-Cloud Separation,
  Agentic AI OS Feedback Loop, IoT Simulation and Telemetry Contracts,
  Secure-by-Design RAID, and Build-Ready Specification Quality
- Added sections: System Constraints; Delivery and Compliance Workflow
- Removed sections: none
- Follow-up TODOs: ratification date requires confirmation from the project owner
-->
# AE-SSS Constitution

## Core Principles

### I. Edge-Cloud Separation
Field nodes MUST spend irreplaceable energy only on sensing and the minimum
communication required to forward observations. Edge gateways MUST perform
normalization, validation, intelligence, anomaly triage, and data pruning before
any data reaches mains-powered servers. Field, edge, and cloud responsibilities
MUST remain independently replaceable behind explicit contracts; no cloud service
may become a prerequisite for field sensing. This preserves sensing continuity
under intermittent connectivity and prevents avoidable energy expenditure.

### II. Agentic AI OS Feedback Loop
The conceptual control loop MUST be expressed as monitor -> reason -> validate
-> act -> learn. Monitoring MUST collect observations and health signals; reason
must produce bounded hypotheses or recommendations; validation MUST check policy,
confidence, safety, and authorization; action MUST be auditable and reversible
where feasible; learning MUST update models or rules only from approved outcomes.
No autonomous action may bypass validation or conceal uncertainty. This keeps the
Agentic AI OS explainable, governable, and suitable for eventual implementation.

### III. IoT Simulation and Telemetry Contracts
Every simulated sensor stream MUST emit mock JSON observations with at least
`timestamp`, `device_id`, `metric`, and `value`, plus an explicit schema version
when the contract evolves. Virtual energy, air, and water sensors MUST be
representable through the same contract used by the Agentic AI OS. Specifications
MUST define input semantics, units, sampling assumptions, outputs, and invalid
data behavior. Deterministic fixtures MUST cover normal, delayed, duplicated,
malformed, and out-of-order observations so the conceptual pipeline can be handed
to another team without inventing missing interfaces.

### IV. Secure-by-Design RAID
All designs MUST address RAID as Reliability, Availability, Integrity, and Data
minimization. Reliability MUST include retries, bounded queues, and recovery
behavior; availability MUST preserve local sensing and safe degradation during
gateway or cloud loss; integrity MUST include authenticated provenance,
tamper-evident audit records, validation, and least-privilege actions; data
minimization MUST prune or aggregate data at the edge and retain only what the
stated purpose requires. A design is incomplete until each RAID dimension has a
failure signal, a mitigation, and an observable acceptance condition.

### V. Build-Ready Specification Quality
System specifications MUST be structured for immediate hand-off and MUST map
inputs, transformations, outputs, constraints, assumptions, ownership, and
acceptance checks. `CLAUDE.md` MUST define system scope and agent roles, while
`spec.md` MUST map the telemetry and control contracts without embedding
implementation decisions that violate this constitution. Every requirement MUST
be traceable to a principle or explicit user outcome. This makes the blueprint
buildable by another team while preserving its conceptual scope.

## System Constraints

The architecture MUST remain a conceptual blueprint rather than an application
implementation. It MUST define the hierarchy `field node -> edge gateway ->
mains-powered server` and MUST prohibit direct field-to-cloud intelligence paths.
Edge processing MUST document what is retained, pruned, aggregated, or forwarded.

Silent failures are first-class risks: a sensor reporting 100% uptime and zero
missing packets MUST NOT be treated as healthy by itself. Health assessment MUST
compare physical plausibility, calibration drift, peer or environmental context,
stale-value duration, and independent diagnostics where available. Suspected drift
MUST create a distinct degraded-health signal and enter the validate stage before
any consequential action.

## Delivery and Compliance Workflow

Each future specification MUST identify the monitor, reason, validate, act, and
learn stages; the field, edge, and cloud boundary; the telemetry schema; RAID
controls; silent-failure detection; and measurable acceptance conditions. Reviews
MUST reject designs that move intelligence or pruning onto energy-constrained field
nodes, omit validation before action, or claim health from transport metrics alone.
Changes to shared contracts MUST include compatibility and migration notes.

## Governance
<!-- Example: Constitution supersedes all other practices; Amendments require documentation, approval, migration plan -->

This constitution supersedes conflicting project guidance. Amendments MUST state
the motivation, affected principles, compatibility impact, migration needs, and
updated acceptance checks. The project owner MUST approve amendments through the
repository review process, and every amendment MUST update this document's Sync
Impact Report and last-amended date.

Versioning follows semantic versioning: MAJOR for incompatible governance or
principle removal or redefinition, MINOR for a new principle or materially
expanded governance, and PATCH for clarifications or non-semantic corrections.
Every feature review MUST record compliance with this constitution, including the
edge-cloud boundary, feedback-loop validation, telemetry contract, RAID controls,
and silent-failure handling. The constitution MUST be reviewed whenever those
contracts change and at least once per major blueprint revision.

**Version**: 1.0.0 | **Ratified**: TODO(RATIFICATION_DATE): confirm original adoption date | **Last Amended**: 2026-09-04
<!-- Example: Version: 2.1.1 | Ratified: 2025-06-13 | Last Amended: 2025-07-16 -->
