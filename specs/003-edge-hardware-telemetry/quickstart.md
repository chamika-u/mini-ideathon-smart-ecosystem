# Quickstart Validation Guide

This guide validates the conceptual contract without authorizing production
surveillance, emergency calls, or uncontrolled physical actuation.

## Prerequisites

- A simulated ESP32/ESP8266 Device or compatible test board
- A local mock HTTP server representing the Edge ingress
- The contracts in `contracts/telemetry.md` and `contracts/actuation-command.md`
- A test fixture runner capable of replaying valid and invalid JSON observations

## Validation Scenarios

1. **Device connectivity**: Provide valid credentials, start the Device, and
   verify a successful connection plus an operator-visible `WiFi.localIP()` value.
2. **Telemetry POST**: Send the example observation and verify HTTP POST,
   `Content-Type: application/json`, per-device authentication, and required fields.
3. **Edge boundary**: Replay malformed, stale, duplicate, delayed, and out-of-order
   observations; verify rejection or quarantine and no raw-stream forwarding.
4. **Agentic loop**: Replay an anomaly with SDG constraints; verify Monitor,
   Planner, Validator, and Action evidence in the order monitor -> reason ->
   validate -> act -> learn.
5. **Physical feedback**: Verify the Action Agent reports a changed state and a
   follow-up observation influences the next decision.
6. **Silent failure**: Keep packets and current nominal while replaying static or
   implausible measurements; verify an integrity alert and read-only diagnostic.
7. **Security rejection**: Verify invalid certificates, missing or revoked
   credentials, cross-device credentials, expired commands, and unknown command
   sets are rejected and audited.
8. **Latency**: Measure representative validated local Edge-to-Act scenarios and
   confirm at least 95% complete in under 1 second.

## Expected Evidence

Record timestamped transport outcomes, validation decisions, audit references,
actuator state reports, follow-up measurements, and diagnostic work-item results.
The evidence is sufficient only when every scenario is traceable to the entities
and contracts in this feature directory.