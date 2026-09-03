---

description: "Task list for Edge Hardware Telemetry"
---

# Tasks: Edge Hardware Telemetry

**Input**: Design documents from `/specs/003-edge-hardware-telemetry/`

**Prerequisites**: [plan.md](plan.md), [spec.md](spec.md), [research.md](research.md),
[data-model.md](data-model.md), [contracts/](contracts/), [quickstart.md](quickstart.md)

**Tests**: Contract and acceptance validation tasks are included because the feature
specification defines independent test scenarios and measurable outcomes.

**Organization**: Tasks are grouped by user story so each increment can be built
and validated independently.

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Establish the source and test layout described by the implementation plan.

- [ ] T001 Create the Device, Edge, Platform, and tests directories with `mkdir -p device/src edge/agents edge/services platform/api tests/contract tests/integration tests/results tests/fixtures`.
- [ ] T002 [P] Add the feature contract references and validation scope to `README.md`.
- [ ] T003 [P] Create the Python virtual-sensor configuration template in `device/src/config.py`.
- [ ] T004 [P] Create the test fixture directories for telemetry, security, feedback, and integrity scenarios in `tests/fixtures/`.

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Implement shared contracts and boundaries required by every story.

- [ ] T005 Define the observation schema and validation rules from `specs/003-edge-hardware-telemetry/contracts/telemetry.md` in `edge/telemetry_schema.json`.
- [ ] T006 [P] Define validated command schema and rejection rules from `specs/003-edge-hardware-telemetry/contracts/actuation-command.md` in `edge/actuation_command_schema.json`.
- [ ] T007 [P] Create shared entity types for Device Observation, Edge Assessment, Validated Command, Diagnostic Work Item, and Feedback Record in `edge/models/`.
- [ ] T008 Create the bounded retry, buffering, provenance, and audit interfaces in `edge/services/reliability.py`.
- [ ] T009 Create the approved-command, least-privilege, expiry, stop-rule, and authorization policy interface in `edge/services/validator.py`.
- [ ] T010 Document Device -> Edge -> Network -> Platform -> Application ownership and retained/pruned/forwarded data in `README.md`.

## Phase 3: User Story 1 - Connect a Field Node (Priority: P1)

**Goal**: Connect a simulated Device and deliver authenticated JSON telemetry to Edge.

**Independent Test**: A Python virtual sensor exposes a simulated local address,
sends an HTTP POST using `Content-Type: application/json`, and receives a handled response.

- [ ] T011 [US1] Implement Python virtual-sensor network connection simulation and failure states in `device/src/network.py`. *Constraint:* This task must only build Python virtual sensors that stream JSON telemetry. Do not write production hardware firmware.
- [ ] T012 [US1] Expose the simulated network address and connection diagnostics in `device/src/network.py`. *Constraint:* This task must only build Python virtual sensors that stream JSON telemetry. Do not write production hardware firmware.
- [ ] T013 [US1] Implement Python virtual-sensor observation serialization with `timestamp`, `device_id`, `metric`, `value`, unit, and schema version in `device/src/telemetry.py`. *Constraint:* This task must only build Python virtual sensors that stream JSON telemetry. Do not write production hardware firmware.
- [ ] T014 [US1] Implement simulated HTTPS JSON POST transport with `Content-Type: application/json` in `device/src/telemetry.py`. *Constraint:* This task must only build Python virtual sensors that stream JSON telemetry. Do not write production hardware firmware.
- [ ] T015 [US1] Add per-device credential loading and server certificate validation boundaries to the Python virtual-sensor simulation in `device/src/security.py`. *Constraint:* This task must only build Python virtual sensors that stream JSON telemetry. Do not write production hardware firmware.
- [ ] T016 [P] [US1] Add transport failure, retry, malformed payload, certificate, revoked credential, and cross-device credential fixtures in `tests/fixtures/telemetry/`.
- [ ] T017 [US1] Add the Device-to-Edge validation runner and response-outcome checks in `tests/contract/test_device_telemetry.py`.

## Phase 4: User Story 2 - Run the Edge Agentic Loop (Priority: P1)

**Goal**: Process observations through Monitor, Planner, Validator, and Action with measured physical feedback.

**Independent Test**: Replay an anomaly and verify monitor -> reason -> validate ->
act -> learn evidence, authorized action, state change, and follow-up observation.

- [ ] T018 [US2] Implement Edge envelope validation, deduplication, ordering, and data-pruning decisions in `edge/services/telemetry_ingress.py`.
- [ ] T019 [US2] Implement Monitor Agent signal, SDG constraint, threshold, pattern, freshness, drift, and plausibility evaluation in `edge/agents/monitor.py`.
- [ ] T020 [US2] Implement Planner Agent bounded evidence-backed plans without direct action authorization in `edge/agents/planner.py`.
- [ ] T021 [US2] Implement Decision / Validator Agent policy, least-privilege, approved-command, stop-rule, and audit checks in `edge/agents/validator.py`.
- [ ] T022 [US2] Implement Action Agent command execution and physical-state reporting in `edge/agents/action.py`.
- [ ] T023 [US2] Implement Feedback Record creation linking command, observed effect, outcome, and learning approval in `edge/services/feedback.py`.
- [ ] T024 [US2] Add the closed-loop acceptance runner for Sense, Communicate, Decide, Act, and follow-up measurement in `tests/integration/test_agentic_loop.py`.

## Phase 5: User Story 3 - Respond to Silent Hardware Failure (Priority: P2)

**Goal**: Detect physically degraded sensors despite nominal packets/current and produce bounded diagnostics plus a dashboard alert.

**Independent Test**: Replay static, drifting, or implausible readings with nominal
uptime and packet delivery, then verify integrity alert and diagnostic work item.

- [ ] T025 [US3] Implement independent physical-health scoring for freshness, expected variation, calibration drift, and environmental context in `edge/services/health.py`.
- [ ] T026 [US3] Implement Monitor Agent degraded-health classification for silent failure in `edge/agents/monitor.py`.
- [ ] T027 [US3] Implement Researcher, Engineer, Tester, and Designer diagnostic hand-off records in `edge/services/diagnostics.py`.
- [ ] T028 [US3] Enforce read-only automatic diagnostics and Validator approval for control-changing diagnostics in `edge/services/diagnostics.py`.
- [ ] T029 [US3] Route diagnostic integrity alerts and unresolved uncertainty to the dashboard contract in `platform/alerts/diagnostics.json`.
- [ ] T030 [P] [US3] Add static, drift, occlusion, nominal-current, and nominal-packet fixtures in `tests/fixtures/integrity/`.
- [ ] T031 [US3] Add silent-failure acceptance checks proving alerting occurs before unsafe actuation in `tests/integration/test_silent_failure.py`.

## Phase 6: Polish & Cross-Cutting Concerns

- [ ] T032 [P] Add the complete quickstart validation commands and expected evidence to `README.md`.
- [ ] T033 [P] Add contract compatibility and schema-version checks in `tests/contract/test_schema_compatibility.py`.
- [ ] T034 Add traceable requirement-to-task references for FR-001 through FR-016 in `specs/003-edge-hardware-telemetry/traceability.md`.
- [ ] T035 Run the latency, security, RAID, data-reduction, and closed-loop acceptance scenarios from `specs/003-edge-hardware-telemetry/quickstart.md` and record results in `tests/results/edge-hardware-telemetry.md`.
- [ ] T036 Verify `CLAUDE.md` (system scope and agent roles), `spec.md` (inputs, outputs, and constraints), and `README.md` (how to run and understand) are fully aligned and structurally clear enough for another team to build, and record the SC-006 result in `tests/results/edge-hardware-telemetry.md`.

## Dependencies

```text
T001-T004 -> T005-T010
T005-T010 -> US1, US2, US3
US1: T011-T015 -> T017
US2: T018-T023 -> T024
US3: T025-T029 -> T031
US1 and US2 -> US3 validation
US1, US2, US3 -> T032-T036
```

User Story 1 and User Story 2 can proceed in parallel after foundational contracts.
User Story 3 depends on shared health and validator interfaces but can develop its
fixtures in parallel with User Story 2.

## Parallel Execution Examples

### User Story 1

```text
Parallel: T011, T013, T015, T016
Sequential: T012 after T011; T014 after T013; T017 after T011-T016
```

### User Story 2

```text
Parallel: T019, T020, T022
Sequential: T018 before T019; T021 after T020; T023 after T022; T024 after T018-T023
```

### User Story 3

```text
Parallel: T025, T027, T030
Sequential: T026 after T025; T028 after T027; T029 after T028; T031 after T025-T030
```

## Implementation Strategy

1. Deliver the MVP as User Story 1 plus the shared telemetry and security boundary:
   a Device can connect and submit one authenticated observation to Edge.
2. Add User Story 2 to demonstrate the value-producing closed loop with validated
   actuation and measured feedback.
3. Add User Story 3 for proactive integrity and bounded autonomous diagnostics.
4. Finish with contract compatibility, traceability, quickstart evidence, and the
   under-one-second local latency measurement.