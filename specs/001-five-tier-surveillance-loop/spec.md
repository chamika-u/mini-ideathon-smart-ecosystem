# Feature Specification: Five-Tier Surveillance Loop

**Feature Branch**: `001-five-tier-surveillance-loop`

**Created**: 2026-09-04

**Status**: Draft

**Input**: User description: Design a five-tier Device, Edge, Network, Platform,
Application architectural blueprint for AE-SSS with edge inference, a closed-loop
actuator path, telemetry contracts, HITL escalation, and silent-failure detection.

## Clarifications

### Session 2026-09-04

- Q: Should the final architecture specification live only in the existing feature
  file, be duplicated as a root-level `spec.md`, or use the feature file as the
  canonical source with a root-level summary? -> A: Use the feature specification
  as canonical and create a root-level summary during planning or implementation.
- Q: If the Network or Platform is unavailable during a Level 3 event, what should
  happen after the 30-second local countdown expires? -> A: Edge performs a
  pre-authorized, bounded local actuator action after 30 seconds.

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Resolve a Critical Threat (Priority: P1)

An operator needs a multi-modal threat to be classified locally, escalated with
minimal data, and resolved through a physical actuator when no human intervenes.

**Why this priority**: Critical safety events require bounded latency, privacy,
local autonomy, and proof that the system controls the physical environment.

**Independent Test**: Replay assault and acoustic-distress observations through the
five tiers and verify classification, metadata-only escalation, HITL timing, and
actuator completion without transmitting raw waveforms.

**Acceptance Scenarios**:

1. **Given** Device sensors transduce visual and acoustic signals, **When** the
   Edge aggregates and filters them, **Then** local inference classifies the event
   as Level 3 (Critical) and forwards anomaly metadata only.
2. **Given** a Level 3 event reaches the Platform, **When** no authorized human
   override occurs for 30 seconds, **Then** an authorized command travels through
   the Application path to an actuator that triggers silent GPS alerts and EMS API
   calls.
3. **Given** a human intervenes during the countdown, **When** the override is
   accepted, **Then** automatic actuation is cancelled and the decision is audited.

### User Story 2 - Deter a Civic Violation Locally (Priority: P2)

A site operator needs a minor violation to be handled at the Edge without cloud
dependence or unnecessary transmission.

**Why this priority**: Local handling reduces latency, bandwidth, and exposure of
incidental personal data while preserving autonomy during internet loss.

**Independent Test**: Replay a littering or spitting observation and verify Level 1
classification and immediate local PA-speaker actuation with no cloud event.

**Acceptance Scenarios**:

1. **Given** Edge feature extraction detects a minor civic violation, **When** the
   Edge classifies it as Level 1 (Civic), **Then** it bypasses the cloud and sends
   an authorized local actuator command that produces a physical deterrent.
2. **Given** the internet connection is unavailable, **When** a Level 1 event is
   detected, **Then** local classification and actuation still complete.

### User Story 3 - Detect a Silent Sensor Failure (Priority: P3)

An operator needs the system to detect physical measurement degradation even when
transport telemetry reports perfect uptime.

**Why this priority**: A false healthy signal can hide blind spots and undermine
every downstream decision.

**Independent Test**: Replay an occluded lens whose MCU current and packet delivery
remain nominal, then verify a degraded-health signal and hardware integrity alert.

**Acceptance Scenarios**:

1. **Given** a sensor reports 100% uptime and no missing packets, **When** its
   measured quantity becomes physically implausible or static, **Then** Edge health
   reasoning marks it degraded and dispatches a hardware integrity alert.
2. **Given** a degraded sensor is detected, **When** a consequential action is
   considered, **Then** validation accounts for the degraded source before action.

### Edge Cases

- If Network connectivity fails, Edge retains required local autonomy and queues or
  discards data according to the documented retention policy.
- If duplicate, delayed, malformed, or out-of-order observations arrive, Edge
  validates them and prevents duplicate actuation.
- If the HITL countdown expires while Platform or Network is unavailable, the
  Edge executes only a pre-authorized, bounded local actuator fallback and records
  its audit event; no unauthenticated or unapproved command is executed.
- If sensor values drift gradually while changing, physical plausibility,
  calibration, peer, and environmental checks still raise degraded health.
- If an actuator does not confirm state change, the system records an actuation
  failure and applies the documented safe recovery path.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: The blueprint MUST define Device, Edge, Network, Platform, and
  Application responsibilities and both forward sensing and return actuation paths.
- **FR-002**: Device nodes MUST transduce physical quantities into electrical
  signals and MUST spend irreplaceable energy on sensing and minimal forwarding.
- **FR-003**: Edge nodes MUST perform feature extraction, multi-modal aggregation,
  filtering, on-device inference, and data pruning before cloud transmission.
- **FR-004**: The design MUST target a transmitted-data reduction factor of
  $10^3$ to $10^5$ relative to raw streams and MUST document the measurement basis.
- **FR-005**: The control loop MUST explicitly terminate in an actuator that changes
  the environment; a dashboard notification alone MUST NOT satisfy controllability.
- **FR-006**: The Agentic AI OS MUST represent monitor -> reason -> validate -> act
  -> learn, with authorization and safety validation before every consequential act.
- **FR-007**: Multi-modal assault and acoustic-distress evidence MUST be classified
  locally as Level 3 (Critical) without sending heavy raw waveforms to the cloud.
- **FR-008**: Level 3 events MUST use send-on-delta anomaly metadata over Network,
  then initiate a 30-second Platform HITL manual-override countdown.
- **FR-009**: On countdown expiry without intervention, the authorized command path
  MUST reach an actuator that triggers silent GPS alerts and EMS API calls.
- **FR-010**: Locally detected littering or spitting MUST be classified as Level 1
  (Civic), bypass the cloud, and trigger an authorized local physical deterrent.
- **FR-011**: Level 1 operation MUST remain available when the internet connection
  fails, subject to local safety and authorization rules.
- **FR-012**: The telemetry contract MUST support mock JSON observations containing
  `timestamp`, `device_id`, `metric`, and `value`; units, schema version, and source
  health semantics MUST be defined for energy, air, and water examples.
- **FR-013**: Edge health reasoning MUST detect occlusion, stale values, drift, and
  physical implausibility even when MCU current, uptime, and packet delivery are
  nominal, then dispatch a hardware integrity alert.
- **FR-014**: Every event, override, validation result, command, actuator outcome,
  and learning approval MUST have auditable provenance and least-privilege access.
- **FR-015**: The specification MUST identify retained, aggregated, pruned, and
  forwarded data at each boundary and define behavior for invalid observations.
- **FR-016**: The blueprint MUST name the canonical physical-to-digital pipeline
  steps as Sense, Communicate, Decide, and Act, and MUST show that Act changes a
  physical quantity whose effect is measured by a later Sense step.
- **FR-017**: The Agentic AI OS MUST continuously represent monitor -> reason ->
  validate -> act -> learn across the canonical pipeline, with the Monitor Agent
  ingesting signals, SDG data, constraints, thresholds, and patterns; the Planner
  Agent producing a plan; the Decision / Validator Agent enforcing least privilege,
  approved commands, human stop or override, and action logging; and the Action
  Agent producing a physical effect.
- **FR-018**: The final presentation specification MUST define an 8-minute pitch
  covering the SDG problem, GitHub Spec, Agentic AI OS design, IoT simulation
  architecture, and evidence that makes the technical story trustworthy.
- **FR-019**: Repository hand-off requirements MUST identify `CLAUDE.md` for system
  scope and agent roles, the canonical feature `spec.md` for inputs, outputs, and
  constraints, and `README.md` for how to run and understand the blueprint.
- **FR-020**: If Network or Platform is unavailable when the Level 3 countdown
  expires, Edge MUST execute only a pre-authorized, bounded local actuator action,
  enforce its safety checks and expiry, and record the outcome for later sync.

### Key Entities *(include if data involved)*

- **Sensor Observation**: A timestamped device measurement containing device,
  metric, value, unit, schema version, and source-health context.
- **Event Assessment**: Edge-produced classification, confidence, evidence summary,
  event level, delta, validation state, and retention decision.
- **HITL Decision**: A time-bounded override request containing deadline, actor,
  decision, authorization result, and audit record.
- **Actuation Command**: An authorized instruction with target actuator, intended
  physical effect, safety checks, expiry, and execution outcome.
- **Sensor Health Assessment**: Evidence about data freshness, plausibility, drift,
  diagnostics, and degraded or healthy status independent of transport uptime.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: In representative simulations, Edge processing reduces transmitted
  data by at least $10^3$ and records whether the target up to $10^5$ is achieved.
- **SC-002**: Every Level 3 simulation produces a metadata-only escalation, a
  measurable 30-second HITL deadline, and an auditable final decision.
- **SC-003**: At least 99% of critical test scenarios terminate in a verified
  actuator state change or an explicit safe actuation-failure state.
- **SC-004**: At least 99% of Level 1 test scenarios complete local deterrence
  without a cloud dependency, including during simulated internet loss.
- **SC-005**: All silent-failure fixtures with nominal uptime and packet delivery
  produce a degraded-health or hardware-integrity signal before consequential act.
- **SC-006**: Another engineering team can trace 100% of functional requirements
  to a tier, telemetry field, acceptance scenario, and measurable outcome.
- **SC-007**: The architecture walkthrough demonstrates all four canonical steps,
  a measured action effect, and a complete monitor -> reason -> validate -> act ->
  learn cycle without an open-loop notification-only path.
- **SC-008**: A timed presentation rehearsal completes the required story in 8
  minutes and covers all five specified pitch topics with no omitted section.

## Assumptions

- The blueprint uses simulated sensor streams and mock external alert calls; it does
  not authorize real surveillance, emergency dispatch, or public-address deployment.
- Mains-powered servers provide durable coordination, while Edge retains enough
  state for Level 1 autonomy and the pre-authorized, bounded Level 3 fallback.
- Authorized operators and actuator capabilities are defined by the future build
  team; absent authorization, the system fails closed for consequential actions.
- The exact reduction baseline, sensor sampling rates, physical units, and retention
  periods will be fixed during planning and recorded as versioned contract decisions.
- The constitution and `CLAUDE.md` govern scope, roles, hierarchy, and compliance.