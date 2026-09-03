# AE-SSS System Scope and Agent Roles

## System Scope

AE-SSS is a conceptual five-tier architecture for a closed-loop Agentic Edge-AI
Smart Surveillance System:

1. **Device**: transduces physical quantities into electrical signals and emits
   minimal observations.
2. **Edge**: extracts features, performs local inference, prunes data, detects
   sensor health anomalies, and controls local actuators.
3. **Network**: transports authenticated summaries and commands between edge and
   mains-powered platform services.
4. **Platform**: stores approved event metadata, coordinates HITL decisions, and
   exposes governed services.
5. **Application**: presents validated events and issues authorized commands that
   terminate in physical actuation.

The blueprint MUST preserve the hierarchy `Device -> Edge -> Network -> Platform
-> Application` and the return path to an actuator. Device nodes MUST not perform
cloud intelligence. Edge nodes MUST perform feature extraction, inference, and
data pruning before transmission. The design is conceptual and does not authorize
production deployment or real emergency integrations.

## Agent Roles

- **Architecture Agent**: maintains tier boundaries, contracts, assumptions, and
  traceability to the project constitution.
- **Perception Agent**: defines sensor modalities, transduction behavior, feature
  semantics, and physical plausibility checks.
- **Edge Intelligence Agent**: defines local inference, event levels, send-on-delta
  behavior, degraded operation, and silent-failure detection.
- **Safety and Security Agent**: reviews RAID controls, authorization, provenance,
  HITL countdown behavior, auditability, and safe actuation.
- **Specification Agent**: maintains `spec.md`, telemetry schemas, acceptance
  scenarios, measurable outcomes, and hand-off readiness.

All agents MUST document assumptions and MUST not bypass the monitor -> reason ->
validate -> act -> learn loop. No agent may move raw-data intelligence or pruning
onto the energy-constrained Device tier.