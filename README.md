# Agentic Edge-AI Smart Surveillance System (AE-SSS)

Architectural Developer Onboarding Guide

> **Scope boundary:** AE-SSS is a simulation-only conceptual blueprint. This
> repository does not contain production surveillance, hardware firmware, live
> emergency integrations, or an authorization to operate in a public environment.
> The implementation uses Python virtual sensors to model field devices and a
> local Edge control loop.

## 1. System Overview & Purpose

### Core Purpose

AE-SSS is an anchor architecture for turning a passive sensing environment into a
governed, closed-loop ecosystem. The reference scenario is a village micro-grid,
but the same contracts apply to energy, air, water, and safety observations.

The system solves four related problems:

1. **Physical-to-digital translation:** virtual Devices represent sensors that
	 transduce a physical quantity into a timestamped observation.
2. **Resource-aware intelligence:** the Edge receives minimal observations,
	 validates them, derives features, detects health anomalies, and prunes data
	 before any mains-powered service receives it.
3. **Governed autonomy:** an Agentic AI OS runs `monitor -> reason -> validate ->
	 act -> learn`; no consequential command bypasses policy, authorization, expiry,
	 or a safety stop condition.
4. **Proof of control:** the Action stage changes a simulated physical state, and
	 a later observation records whether the intended effect occurred. A dashboard
	 notification without a physical effect is not considered success.

The canonical physical pipeline is:

```text
Sense -> Communicate -> Decide -> Act
	^                                  |
	|________ follow-up measurement ___|
```

The canonical agent pipeline is:

```text
Monitor -> Reason -> Validate -> Act -> Learn
```

`CLAUDE.md` defines system scope and agent roles. The canonical detailed feature
contract is [specs/003-edge-hardware-telemetry/spec.md](specs/003-edge-hardware-telemetry/spec.md).

### Key KPIs

These targets are simulation acceptance targets, not production operating limits.

| KPI | Target | Measurement point |
|---|---:|---|
| Local Edge-to-Act latency | At least 95% under 1 second | Validator release to physical-state report |
| Closed-loop completion | 100% of demonstrations | Action followed by a measurement that informs the next decision |
| Silent-failure detection | 100% of defined fixtures | Integrity signal before unsafe consequential action |
| Transport contract validity | 100% of valid submissions | Required JSON fields and authenticated Device identity accepted |
| Security rejection | 100% of negative fixtures | Invalid certificate, missing/revoked, and cross-device credentials rejected |
| Test baseline | 13 automated tests currently pass | `python3 -m unittest discover -s tests -p "test_*.py" -v` |
| Data minimization | Raw streams do not cross Edge | Forwarded payload contains pruned observations or metadata |

Production capacity metrics such as concurrent Device count, sustained message
rate, retention volume, and deployment uptime are intentionally not claimed by
this blueprint. They must be baselined during a future production design.

### Target Audience

- **Municipal or village operators:** need an understandable view of conditions,
	validated actions, alerts, and sensor health.
- **Edge and platform engineers:** implement the tier contracts without moving
	inference or pruning onto the energy-constrained Device boundary.
- **Security and safety reviewers:** verify least privilege, authenticated
	provenance, command allowlists, stop rules, auditability, and safe degradation.
- **Test engineers:** replay valid, malformed, delayed, duplicated, out-of-order,
	drifted, and transport-failure fixtures.
- **Documentation and delivery teams:** use this README with `CLAUDE.md`, the
	feature `spec.md`, contracts, and traceability records to hand off the design.

## 2. Hardware Architecture (Simulation Blueprint)

### Physical and Edge Infrastructure

The repository models the following five-tier hierarchy:

```text
Device -> Edge -> Network -> Platform -> Application
	 |       |        |          |             |
sensor   local    summary    governed     operator UI
signal  insight  transport  services     and commands
																							|
																			simulated Actuator
```

The implementation maps the physical components as follows:

| Conceptual component | Simulation representation | Responsibility |
|---|---|---|
| Field Device | `device/src/` Python virtual sensors | Produce minimal observations and model connectivity; no inference or pruning |
| Sensors | `VirtualSensor`, serialized JSON fixtures | Represent energy, air, water, and health measurements |
| Edge gateway | `edge/agents/` and `edge/services/` | Validate, deduplicate, order, assess health, prune, reason, validate, and coordinate action |
| Network | `VirtualHTTPClient` and `MockEdgeServer` | Model HTTP JSON transport, status outcomes, retryable failures, and identity checks |
| Platform alert surface | `platform/alerts/diagnostics.json` | Define the canonical hardware-integrity alert shape |
| Application | Conceptual operator and command surface | Present governed results and issue only authorized commands |
| Actuator | `edge/agents/action.py` state model | Change simulated state and report the observed effect |

No GPU cluster, physical gateway, camera, microphone, relay, GPS unit, EMS
integration, or public network is provisioned by this repository. Those are
future deployment concerns and must remain behind the same contracts.

### Minimum Simulation Specifications

Because the current Device is virtual, minimum hardware requirements apply to the
developer or CI host rather than to a physical sensor board:

| Resource | Minimum for this repository | Reason |
|---|---:|---|
| CPU | 2 logical cores | Run Python tests and a local mock transport concurrently |
| RAM | 2 GB available | Python interpreter, test runner, and bounded fixtures |
| Storage | 500 MB free | Repository, bytecode cache, and test output |
| Runtime | Python 3.10+ recommended | Type annotations, dataclasses, and standard-library tests |
| Network | Not required for tests | Transport is modeled locally; future external services must be mocked |

For a future physical mapping, the Edge gateway must be selected to run local
feature extraction and inference within the one-second local target while retaining
bounded queues during upstream loss. Device energy, sensor sampling, gateway CPU,
RAM, storage, and chipset requirements must be measured from a representative
workload before deployment. This README does not invent production values.

### Hardware-Software Interface

The Device contract is intentionally expressed through Python mocks rather than
firmware:

- `VirtualWiFi` models connection state and exposes `localIP()` for operator-visible
	diagnosis.
- `VirtualHTTPClient` models a POST request and requires
	`Content-Type: application/json`.
- `MockEdgeServer` validates Device identity and forwards accepted JSON into
	`TelemetryIngress` before storing the observation.
- `CredentialStore` models per-device credentials and revocation.
- `ServerCertificateValidator` models server-certificate trust.
- `VirtualSensor` serializes the required fields: `timestamp`, `device_id`,
	`metric`, and `value`, plus unit, schema version, and source-health context.

A future physical adapter may map sensors to I2C, SPI, serial, or a board driver,
but that adapter is outside this simulation. The adapter must emit the same JSON
contract, must not perform Edge inference or pruning, and must never bypass
authenticated provenance. The current repository intentionally contains no
production C/C++ firmware.

### Telemetry Example

```json
{
	"timestamp": "2026-09-04T12:00:00+00:00",
	"device_id": "energy-node-01",
	"metric": "voltage",
	"value": 230.4,
	"unit": "V",
	"schema_version": "1.0",
	"source_health": {
		"uptime": 1.0,
		"packet_sequence": 1
	}
}
```

The full request and response behavior is defined in
[contracts/telemetry.md](specs/003-edge-hardware-telemetry/contracts/telemetry.md).

## 3. Software Architecture & Component Breakdown

### High-Level Architecture Pattern

AE-SSS uses an **event-driven, contract-first, layered architecture**. The
simulation has independently replaceable Device, Edge, Network, Platform, and
Application responsibilities. It is not a deployed microservice system yet; the
directory boundaries are the preparation for one.

```text
													 +----------------------+
													 | Application          |
													 | operator view        |
													 +----------+-----------+
																			|
												 validated command / alert
																			v
Device          Network             Platform
sensor JSON --> transport --> governed metadata/alerts
	 |                |                  |
	 +--------------> Edge <-------------+
										|
			 +------------+-------------+
			 | Monitor -> Planner       |
			 |          -> Validator    |
			 |          -> Action       |
			 |               |           |
			 |          physical effect |
			 +---------------+-----------+
											 |
								 follow-up Sense
```

Every boundary has a contract. The Edge is the first intelligence boundary; the
Platform receives only pruned observations, assessments, alerts, and audit data.

### Core Component Deep-Dive

#### Device virtual-sensor layer

**Path:** `device/src/`

- **Purpose:** Model a low-energy field node that senses, identifies itself,
	serializes an observation, and sends it toward Edge.
- **Tech stack:** Python standard library; dataclasses, JSON, and mocked transport
	facades retaining compatibility names such as `WiFi.localIP()` and `HTTPClient`.
- **Inputs:** Device configuration, device credential, metric, value, unit, and
	mock certificate fingerprint.
- **Outputs:** Connection address, JSON telemetry payload, transport status, retry
	state, and bounded buffered payloads.

#### Network and Edge ingress

**Paths:** `device/src/network.py`, `edge/services/telemetry_ingress.py`

- **Purpose:** Model authenticated submission and enforce the observation envelope
	before Edge processing.
- **Tech stack:** Python standard library and JSON parsing.
- **Inputs:** JSON payload, content type, Device identity, credential result, and
	certificate result.
- **Outputs:** Accepted `DeviceObservation`, HTTP-like status result, or a rejection
	reason for malformed, duplicate, out-of-order, or unauthorized input.

#### Edge data model and schemas

**Paths:** `edge/models.py`, `edge/telemetry_schema.json`,
`edge/actuation_command_schema.json`

- **Purpose:** Provide stable representations for observations, assessments,
	commands, diagnostic work, and feedback records.
- **Tech stack:** Python dataclasses and JSON Schema-shaped documents.
- **Inputs:** Validated observations and proposed commands.
- **Outputs:** Typed entities, schema validation rules, provenance links, and
	command requirements.

#### Monitor Agent and health service

**Paths:** `edge/agents/monitor.py`, `edge/services/health.py`

- **Purpose:** Detect thresholds, patterns, stale values, physical implausibility,
	static readings, drift, and degraded sensor health.
- **Tech stack:** Python standard library, history windows, statistics, and bounded
	health scoring.
- **Inputs:** `DeviceObservation`, expected range, SDG constraints, uptime, packet
	sequence, and measurement history.
- **Outputs:** `EdgeAssessment` with classification, confidence, health state,
	feature summary, retention decision, and optional requested action.

#### Planner Agent

**Path:** `edge/agents/planner.py`

- **Purpose:** Turn monitored evidence and constraints into a bounded proposal.
- **Tech stack:** Python service boundary; model or rule integration is replaceable.
- **Inputs:** Edge assessment and SDG/system constraints.
- **Outputs:** Evidence-backed plan with requested action and `authorized: false`.
	Planning never authorizes physical execution.

#### Decision / Validator Agent

**Paths:** `edge/agents/validator.py`, `edge/services/validator.py`

- **Purpose:** Enforce policy before a physical action.
- **Tech stack:** Python policy object, allowlisted command sets, expiry parsing,
	stop-condition checks, and audit records.
- **Inputs:** Proposed command, command-set identity, authorization result, expiry,
	stop condition, and scope.
- **Outputs:** Approval or rejection plus an audit entry. Rejected commands cannot
	reach the Action Agent.

#### Action Agent and feedback service

**Paths:** `edge/agents/action.py`, `edge/services/feedback.py`

- **Purpose:** Apply an approved simulated physical effect and close the loop.
- **Tech stack:** Python state model and dataclass feedback record.
- **Inputs:** Validator-approved command with target, scope, expiry, stop condition,
	and audit reference.
- **Outputs:** Physical-state report, duplicate-command protection, and a
	`FeedbackRecord` linking intended effect to observed effect and learning approval.

#### Reliability service

**Path:** `edge/services/reliability.py`

- **Purpose:** Provide bounded buffering and auditable recovery behavior during
	transient transport loss.
- **Tech stack:** Python `deque` with bounded capacity.
- **Inputs:** Failed or pending payloads.
- **Outputs:** FIFO replay candidates, buffer state, and buffering audit events.

#### Diagnostic Coordinator

**Path:** `edge/services/diagnostics.py`

- **Purpose:** Coordinate proactive silent-failure investigation.
- **Tech stack:** Python work-item coordinator with role audit records.
- **Inputs:** Failure signal, device identity, hypothesis, measurement values, and
	expected range.
- **Outputs:** Researcher, Engineer, Tester, and Designer audit entries, read-only
	diagnostic result, authorization state, and canonical dashboard alert payload.

#### Platform alert contract

**Path:** `platform/alerts/diagnostics.json`

- **Purpose:** Define the platform-facing integrity alert shape.
- **Tech stack:** JSON contract; no deployed alert broker is included.
- **Inputs:** Device identity, degraded health, failure reason, and work-item ID.
- **Outputs:** `hardware_integrity_alert` metadata suitable for a future dashboard.

#### Frontend application

No frontend application is implemented in this repository. The conceptual
Application tier consumes validated assessments, alerts, audit records, and
actuation outcomes. A future frontend must not issue a command directly to an
actuator; it must submit an authorized request through the Validator contract and
display uncertainty and degraded sensor state.

#### Database and caching layers

No production database or cache is implemented. The current simulation uses Python
in-memory collections and bounded buffers. A future Platform design may introduce
durable event/audit storage and an Edge-local cache, but it must define retention,
eviction, replay, provenance, and failure semantics before implementation.

## 4. Networking & Routing

### Network Topology

The repository models a private, local-first topology rather than provisioning a
cloud VPC:

```text
			simulated Device network
								|
								v
			 +----------------+
			 | local Edge     |  first validation and intelligence boundary
			 +--------+-------+
								|
			 authenticated summaries only
								v
			 +----------------+
			 | private Network |
			 +--------+-------+
								v
			 +----------------+       +------------------+
			 | Platform       | ----> | Application      |
			 | metadata/audit |       | operator surface |
			 +----------------+       +------------------+
```

For a production deployment, Devices and Edge gateways belong in private network
segments. Platform services should be isolated from public ingress, and only a
dedicated Application/API boundary should be exposed externally. Raw sensor data
must not be routed directly from Device to cloud services.

### Ingress and Routing

Current simulation ingress is `MockEdgeServer.receive()`:

1. `VirtualSensor.send()` authenticates the Device credential.
2. The virtual certificate validator checks the trusted server fingerprint.
3. `VirtualHTTPClient.post()` requires `Content-Type: application/json`.
4. `MockEdgeServer` checks the expected `device_id`.
5. `TelemetryIngress.accept()` validates required fields, duplicate identity, and
	 timestamp ordering.
6. Accepted data becomes an Edge assessment; rejected data returns an explicit
	 failure result and is never treated as accepted telemetry.

There is no public API gateway, load balancer, reverse proxy, or production DNS in
the repository. A future deployment must place TLS termination and authentication
at a controlled ingress, route only to Edge or Platform endpoints, apply request
limits, and preserve the Device identity through authenticated provenance.

### Service-to-Service Communication

The current implementation uses direct Python calls for deterministic testing.
There are no Kafka topics, AMQP exchanges, gRPC services, or service-discovery
registries. The logical routing table is:

| Route | Current mechanism | Payload |
|---|---|---|
| Device -> Edge | Mock HTTP POST | JSON `DeviceObservation` |
| Edge ingress -> Monitor | Python service call | Typed observation |
| Monitor -> Planner | Python service call | `EdgeAssessment` |
| Planner -> Validator | Command proposal | Unvalidated command |
| Validator -> Action | Validated command | Allowlisted command with expiry and stop condition |
| Action -> Monitor | Follow-up observation | Physical-state feedback |
| Diagnostics -> Platform | Canonical JSON alert | Hardware-integrity metadata |

If a broker is introduced later, routing keys must preserve at least
`device_id`, `metric`, `schema_version`, and event type. The broker must not become
the only path for required local Edge safety behavior.

## 5. Codebase Walkthrough Template

### Directory Structure

```text
mini-ideathon-smart-ecosystem/
├── CLAUDE.md                         # System scope and agent roles
├── README.md                         # This onboarding guide
├── LICENSE
├── .gitignore
├── .specify/                         # Spec Kit workflows and project memory
├── specs/
│   ├── 001-five-tier-surveillance-loop/
│   ├── 002-agentic-microgrid-team/
│   └── 003-edge-hardware-telemetry/  # Active canonical feature
│       ├── spec.md
│       ├── plan.md
│       ├── tasks.md
│       ├── research.md
│       ├── data-model.md
│       ├── quickstart.md
│       ├── traceability.md
│       └── contracts/
│           ├── telemetry.md
│           └── actuation-command.md
├── device/
│   └── src/
│       ├── config.py                 # Virtual Device configuration
│       ├── network.py                 # Virtual Wi-Fi and HTTP facades
│       ├── security.py                # Credential and certificate mocks
│       └── telemetry.py               # Observation serialization and retry
├── edge/
│   ├── agents/
│   │   ├── action.py
│   │   ├── monitor.py
│   │   ├── planner.py
│   │   └── validator.py
│   ├── services/
│   │   ├── diagnostics.py
│   │   ├── feedback.py
│   │   ├── health.py
│   │   ├── reliability.py
│   │   ├── telemetry_ingress.py
│   │   └── validator.py
│   ├── actuation_command_schema.json
│   ├── models.py
│   └── telemetry_schema.json
├── platform/
│   ├── __init__.py
│   └── alerts/
│       └── diagnostics.json
└── tests/
		├── contract/
		│   ├── test_device_telemetry.py
		│   └── test_schema_compatibility.py
		├── integration/
		│   ├── test_agentic_loop.py
		│   ├── test_device_recovery.py
		│   └── test_silent_failure.py
		├── fixtures/
		│   ├── integrity/
		│   └── telemetry/
		└── results/
				└── edge-hardware-telemetry.md
```

### Code Component Explanation

#### `/device`

This directory represents the sensing boundary. Its mathematical responsibility
is observation formation, not intelligence: a physical quantity $q$ becomes a
timestamped value $x(t)$ with identity and health context. In the simulation,
`VirtualSensor` produces that value and models transport. Do not add feature
extraction, classification, pruning, or autonomous actuation here.

#### `/edge`

This is the intelligence and safety boundary. `TelemetryIngress` turns untrusted
JSON into a typed observation. `MonitorAgent` derives a bounded assessment from
history and constraints. `PlannerAgent` proposes; `ValidatorAgent` authorizes;
`ActionAgent` changes simulated state; `feedback.py` records the result.

The health logic deliberately separates transport health from physical health:

```text
transport healthy != measurement physically trustworthy
```

Static values, implausible ranges, stale readings, drift, and environmental
context must be evaluated even when packet delivery and current draw appear normal.

#### `/platform`

This directory contains platform-facing contracts, currently the canonical
hardware-integrity alert. It is the boundary for durable governance, audit,
operator-facing alerts, and future external integrations. It must not become a
shortcut around Edge validation or the command policy.

#### `/tests`

Tests are organized by contract and behavior rather than by implementation class:

- `contract/` checks payload and schema boundaries.
- `integration/` checks end-to-end feedback, recovery, latency, and silent failure.
- `fixtures/` contains deterministic valid and negative inputs.
- `results/` records the latest validation evidence without replacing executable
	tests.

### Critical File Pattern: Observation Through the Layers

The following is a commented template, not a complete implementation:

```python
def process_observation(raw_payload, device_context):
		# Device: sense and serialize only. Do not infer or prune here.
		observation = virtual_sensor.serialize(raw_payload, device_context)

		# Network: authenticate the source and deliver the JSON envelope.
		receipt = edge_transport.post(observation, content_type="application/json")
		if not receipt.accepted:
				reliability.buffer_for_bounded_replay(observation, receipt.detail)
				return receipt

		# Edge: validate, deduplicate, order, and prune before intelligence.
		typed_observation = telemetry_ingress.accept(observation)
		assessment = monitor.assess(typed_observation, constraints)

		# Reason: propose a bounded action, never authorize it.
		proposal = planner.plan(assessment, constraints)

		# Validate: enforce identity, policy, allowlist, expiry, stop condition, and audit.
		command = validator.approve_or_reject(proposal)
		if not command.approved:
				return command

		# Act: change the physical state and report what actually changed.
		effect = action.execute(command)

		# Learn: sense the effect, link it to the command, and update only by policy.
		follow_up = virtual_sensor.measure_effect(effect)
		return feedback.record(command, effect, follow_up, learning_approval=True)
```

### First-Day Developer Workflow

1. Read [CLAUDE.md](CLAUDE.md), then the active [spec.md](specs/003-edge-hardware-telemetry/spec.md),
	 [plan.md](specs/003-edge-hardware-telemetry/plan.md), and contracts.
2. Run the validation suite:

	 ```text
	 python3 -m unittest discover -s tests -p "test_*.py" -v
	 ```

3. Run syntax and JSON checks:

	 ```text
	 python3 -m compileall -q device edge platform tests
	 python3 -c "import json; json.load(open('edge/telemetry_schema.json')); json.load(open('edge/actuation_command_schema.json')); json.load(open('platform/alerts/diagnostics.json'))"
	 ```

4. Use [quickstart.md](specs/003-edge-hardware-telemetry/quickstart.md) for
	 scenario-by-scenario evidence.
5. Keep the Device boundary virtual and minimal. Put inference, pruning, health
	 reasoning, and safety policy in Edge services.
6. For every consequential action, demonstrate validation, actuation, and a
	 follow-up measurement.
7. For every sensor-health claim, include a silent-failure fixture; uptime and
	 packet continuity alone are not sufficient.

### Delivery Guardrails

- Do not commit credentials, certificates, private keys, or real endpoint secrets.
- Do not connect this simulation to live surveillance, emergency, utility, GPS, or
	EMS systems.
- Do not move intelligence or pruning into `device/src/`.
- Do not allow Planner output to call Action directly.
- Do not treat a dashboard notification as proof of controllability.
- Do not mark a sensor healthy solely from transport metrics.
- Changes to telemetry or actuation contracts require compatibility notes, updated
	fixtures, and updated traceability evidence.

The repository is ready for another team to extend as a governed simulation. Any
production implementation must first establish deployment-specific threat models,
capacity tests, hardware qualification, privacy review, operational ownership,
and regulatory authorization outside this conceptual blueprint.
