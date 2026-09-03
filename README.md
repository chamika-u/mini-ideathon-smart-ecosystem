# mini-ideathon-smart-ecosystem

AE-SSS is a simulation-only Agentic Edge-AI Smart Surveillance System blueprint.
The Device tier is represented by Python virtual sensors. Edge services validate,
extract features, detect physical-health anomalies, prune data, and coordinate
the monitor -> reason -> validate -> act -> learn loop.

## Repository Map

- `CLAUDE.md`: system scope and agent roles.
- `specs/003-edge-hardware-telemetry/spec.md`: canonical feature requirements.
- `specs/003-edge-hardware-telemetry/contracts/`: telemetry and actuation contracts.
- `device/src/`: Python virtual-sensor network, telemetry, security, and config modules.
- `edge/`: schemas, models, agents, and services.
- `platform/alerts/`: dashboard alert contract.
- `tests/`: contract, integration, and fixture validation.

The conceptual hierarchy is `Device -> Edge -> Network -> Platform -> Application`.
Device emits minimal observations; Edge performs intelligence and pruning; validated
commands return through the application path to a simulated physical effect.

## Run Validation

From the repository root, run:

```text
python3 -m unittest discover -s tests -p "test_*.py" -v
```

The suite covers authenticated JSON telemetry, required fields, command validation,
physical feedback, silent sensor failure, and schema compatibility. The full
scenario guide is [specs/003-edge-hardware-telemetry/quickstart.md](specs/003-edge-hardware-telemetry/quickstart.md).

This project does not contain production firmware, real surveillance deployment, or
live emergency integrations.
