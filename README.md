# Agentic Edge-AI Smart Surveillance System (AE-SSS)

Architectural Developer Onboarding Guide

> **Scope boundary:** AE-SSS is a simulation-only conceptual blueprint. This
> repository does not contain production surveillance, hardware firmware, live
> emergency integrations, or an authorization to operate in a public environment.
> The implementation uses Python virtual sensors to model field devices and a
> local Edge control loop.

---

### 📚 Architecture & Problem Statement Documentation

Comprehensive specifications, real-world deployment problem statements, and detailed architectural blueprints are documented in the [`docs/`](docs/) directory:

| Document | Focus & Key Highlights |
|---|---|
| [**Problem Statement & Solution Overview**](docs/problem_statement.README.md) | Real-world deployment scenario at **Pettah Central Bus Stand (Colombo)**: legacy CCTV limitations, multi-modal threat detection, active vs. silent deterrence, 10-minute zero-access privacy buffer, and UN SDG alignment (SDGs 3, 8, 9, 11). |
| [**End-to-End IoT Pipeline Architecture**](docs/iot-pipeline-architecture.md) | 5-stage enterprise IoT telemetry and command architecture: **1. Physical Sensors**, **2. Edge Gateway**, **3. Network & Transport Protocols** (LoRaWAN, 5G, Wi-Fi 6, MQTT/TLS 1.3), **4. Cloud Ingestion & Stream Processing**, and **5. Real-Time Intelligence Analytics & LLM Ingestion & Reasoning Engine (In Scope)**. |
| [**Security Architecture & Trust Boundaries**](docs/security-architecture.md) | Threat modeling across Perimeters A–C, mutual TLS (mTLS) with X.509 certificates, HMAC-SHA256 payload signing, ephemeral token lifecycles, and closed-loop safety guardrails. |
| [**Agentic AI OS Blueprint**](docs/agentic-ai-os-blue-print.md) | Closed-loop edge intelligence blueprint covering the 5-stage feedback cycle (`Monitor -> Reason -> Validate -> Act -> Learn`), Policy-as-Code enforcement, and Human-in-the-Loop (HITL) safety. |

---

## 1. System Overview & Purpose

### Core Purpose

AE-SSS is an architectural blueprint for turning a passive sensing environment into an autonomous, governed, closed-loop ecosystem. Developed for the **IEEE CS R10 Summer School Mini Ideathon**, the primary real-world anchor deployment scenario is the **Pettah Central Bus Stand (Colombo)**—transforming high-density public transit safety from passive CCTV recording into an edge-computed, privacy-preserving, context-aware surveillance and emergency response system. The underlying agentic control loops and telemetry contracts seamlessly generalize across transit security, public safety, municipal air/water monitoring, and village micro-grids.

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
For the real-world deployment scenario, challenges, and UN SDG alignment at Pettah Central Bus Stand, see [docs/problem_statement.README.md](docs/problem_statement.README.md). For the autonomous decision cycle and agent boundaries, see [docs/agentic-ai-os-blue-print.md](docs/agentic-ai-os-blue-print.md).

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

- **Transit, municipal, or ecosystem operators:** need an understandable view of real-time conditions,
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

> *For the complete physical-to-cloud specification across all 5 architectural tiers, see [`docs/iot-pipeline-architecture.md`](docs/iot-pipeline-architecture.md). For device trust perimeters and cryptographic standards, see [`docs/security-architecture.md`](docs/security-architecture.md).*

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

## 3. SOFTWARE ARCHITECTURE & COMPONENT BREAKDOWN

- **High-Level Architecture Pattern:**
  The AE-SSS relies on an Edge-First, Event-Driven architecture. This design shifts the computational burden away from the cloud, placing the Agentic AI OS directly at the local gateway to process the continuous feedback loop: monitor $\rightarrow$ reason $\rightarrow$ validate $\rightarrow$ act $\rightarrow$ learn. By deciding locally, the system ensures ultra-low latency, preserves network bandwidth (using send-on-delta telemetry), and maintains operational autonomy during internet outages.  
  *(For the complete agentic state transitions and contract definitions, refer to [`docs/agentic-ai-os-blue-print.md`](docs/agentic-ai-os-blue-print.md). For cloud ingestion, stream processing, and data warehousing, see [`docs/iot-pipeline-architecture.md`](docs/iot-pipeline-architecture.md).)*  

**ASCII Architecture Data Flow:**

```text
[PHYSICAL ECOSYSTEM (Simulated)]
      │
      ▼
[DEVICE TIER: VIRTUAL SENSORS]
 (Generates JSON Telemetry: visual/acoustic mock data)
      │
      ▼
[EDGE TIER: AGENTIC AI OS] 
 ┌─────────────────────────────────────────────────────────┐
 │ 1. MONITOR AGENT: Observe signals & detect thresholds   │
 │ 2. PLANNER AGENT: Reason & plan (SDG data inputs)       │
 │ 3. VALIDATOR AGENT: Check policy & cyber constraints    │
 │ 4. ACTION AGENT: Execute alert / optimize               │
 └─────────────┬───────────────────────────────────────────┘
               │
     (Send-on-Delta JSON Payload)
               │
      ▼        ▼ 
[LOCAL ACTUATOR]  [PLATFORM / DASHBOARD]
(PA/GPS Alert)    (Human-in-the-Loop Override / Analytics)
```

- **Core Component Deep-Dive:**

  - **Device Layer (`device/src/virtual_sensors.py`)**
    - *Purpose:* Mocks the physical ecosystem hardware (e.g., ESP32, IP cameras, microphones) by generating simulated physical quantities transduced into bits.
    - *Tech Stack:* Python, standard JSON libraries.
    - *Inputs/Outputs:* Takes configuration parameters (e.g., anomaly frequency) and outputs standard JSON telemetry payloads (timestamp, device ID, metric, value).

  - **Agent 1: Monitor Agent (`edge/agents/monitor_agent.py`)**
    - *Purpose:* Configured to actively observe signals streaming from the virtual sensors, specifically searching to detect thresholds or patterns indicating multi-modal threats or silent hardware failures.
    - *Tech Stack:* Python, local thresholding algorithms.
    - *Inputs/Outputs:* Ingests raw JSON telemetry; outputs filtered anomaly events to the Planner.

  - **Agent 2: Planner Agent (`edge/agents/planner_agent.py`)**
    - *Purpose:* Tasked to reason and plan based on the observed signals. It ingests SDG data and system constraints to classify the severity of the anomaly (e.g., Level 1 Civic vs. Level 3 Critical).
    - *Tech Stack:* Python, LLM integration/Rule-based engines.
    - *Inputs/Outputs:* Ingests anomaly events and SDG constraints; outputs classified threat profiles and proposed tactical responses.

  - **Agent 3: Decision / Validator Agent (`edge/agents/validator_agent.py`)**
    - *Purpose:* Acts as the system's immune system. It must strictly check policy and constraints before any execution. It enforces least-privilege access, verifies against an approved command set, and manages the mandatory Human-in-the-Loop (HITL) override/stop rule countdown.
    - *Tech Stack:* Python, Policy-as-Code frameworks.
    - *Inputs/Outputs:* Ingests proposed tactical responses; outputs digitally signed "Authorized Execution" tokens or halts the process.

  - **Agent 4: Action Agent (`edge/agents/action_agent.py`)**
    - *Purpose:* Programmed to trigger alerts or optimizations that change the physical quantity. It routes the finalized GPS coordinates and dispatch payloads to local deterrents or remote officer terminals.
    - *Tech Stack:* Python, simulated HTTP webhook dispatchers.
    - *Inputs/Outputs:* Ingests authorized tokens; outputs physical actuator commands and feedback loop signals.

  - **Platform Dashboard (`platform/api/dashboard.py`)**
    - *Purpose:* Provides the required human override / stop rule interface and fulfills the requirement to log and monitor agent actions for complete auditability.
    - *Tech Stack:* Python (FastAPI/Flask).
    - *Inputs/Outputs:* Ingests send-on-delta metadata and action logs; outputs system state visualizations and human override commands.

## 4. NETWORKING & ROUTING

- **Network Topology:**

  The simulation models a highly decoupled local edge network. Virtual sensors and the Agentic AI OS live on a simulated local subnet, preventing raw data from traversing public networks. Only processed, validated metadata crosses the simulated WAN boundary to the Platform layer.

- **Ingress & Routing:**
  
  Virtual sensors push data to the Edge gateway via mocked HTTP POST requests or local message brokers (e.g., a lightweight local MQTT setup). The `Validator Agent` acts as the primary reverse proxy and security gatekeeper for any inbound external commands, enforcing least-privilege access strictly.

- **Service-to-Service Communication:**

  Internal agents communicate via Python-native event buses (in-memory simulation). Telemetry moving from the Edge to the Platform uses a strict "send-on-delta" REST API pattern. The JSON payloads require explicit `Content-Type: application/json` headers and include routing targets (e.g., `officer_id`) to ensure targeted dispatch.

  *(For full transport protocol layers, MQTT/TLS 1.3 broker topology, and cryptographic trust boundaries, see [`docs/iot-pipeline-architecture.md`](docs/iot-pipeline-architecture.md) and [`docs/security-architecture.md`](docs/security-architecture.md).)*

## 5. CODEBASE WALKTHROUGH TEMPLATE

- **Directory Structure:**
  
  To guarantee this repository is structurally clear enough for another team to build, the following layout is strictly enforced:  

```text
mini-ideathon-smart-ecosystem/
├── README.md                 # System overview and how to run
├── CLAUDE.md                 # System scope + agent roles
├── spec.md                   # Inputs, outputs + constraints
├── docs/                     # Architectural documentation & problem statements
│   ├── problem_statement.README.md  # Real-world Pettah deployment & problem analysis
│   ├── iot-pipeline-architecture.md # End-to-end 5-stage IoT telemetry & cloud pipeline
│   ├── security-architecture.md     # mTLS, zero-trust & cryptographic guardrails
│   └── agentic-ai-os-blue-print.md  # 5-stage Agentic AI OS control loop blueprint
├── device/                   
│   └── src/
│       ├── virtual_sensors.py# Mocks physical quantity transduction
│       └── config.py         # Anomaly generation parameters
├── edge/
│   ├── agents/
│   │   ├── monitor_agent.py  # Observes signals
│   │   ├── planner_agent.py  # Reasons + plans
│   │   ├── validator.py      # Checks policy + constraints
│   │   └── action_agent.py   # Alerts / optimizes
│   └── services/
│       └── core_loop.py      # Executes the continuous feedback loop
├── platform/
│   └── api/
│       └── dashboard.py      # Logs + monitors agent actions
└── tests/
    ├── contract/             # Validates JSON telemetry schemas
    └── integration/          # Verifies closed-loop state changes
```

- **Code Component Explanation & Data Flow (The OS Loop):**
  
  The most critical file in this repository is `edge/services/core_loop.py`. It orchestrates the entire continuous feedback loop. The logic pattern enforces that the system cannot act without passing the validator's security boundaries, and every physical action must route back to the monitor to learn and close the loop.

- **Critical File Pattern Template (`edge/services/core_loop.py`):**

```python
import time
from edge.agents.monitor_agent import Monitor
from edge.agents.planner_agent import Planner
from edge.agents.validator import Validator
from edge.agents.action_agent import Action

class AgenticOS:
    def __init__(self):
        # Initialize the autonomous agent team
        self.monitor = Monitor()
        self.planner = Planner()
        self.validator = Validator()
        self.action = Action()

    def run_continuous_loop(self):
        """
        Executes the 5-stage feedback loop: 
        monitor -> reason -> validate -> act -> learn
        """
        while True:
            # 1. MONITOR: Observe signals & detect thresholds
            raw_signals = self.monitor.observe_signals()
            if raw_signals.anomaly_detected:

                # 2. REASON: Ingest SDG data + constraints to reason and plan
                plan = self.planner.reason_and_plan(raw_signals)

                # 3. VALIDATE: Check policy, constraints, and approved command set
                is_safe = self.validator.check_policy_and_constraints(plan)

                if is_safe:
                    # 4. ACT: Trigger alerts or optimizations
                    result = self.action.execute_alert_or_optimize(plan)

                    # 5. LEARN: Log and monitor agent actions, feed result back
                    self.monitor.log_and_monitor_actions(result)

            time.sleep(1) # Simulation tick

if __name__ == "__main__":
    os = AgenticOS()
    os.run_continuous_loop()
```
