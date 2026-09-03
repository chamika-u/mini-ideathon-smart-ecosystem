# Research: Edge Hardware Telemetry

## Decisions

### Board transport boundary

- **Decision**: Use Arduino-compatible C++ conventions at the Device boundary:
  `WiFi.h` for ESP32, `ESP8266WiFi.h` for ESP8266, `WiFi.localIP()` for visible
  network identity, and `HTTPClient` for JSON HTTP POST.
- **Rationale**: These are explicit feature constraints and keep the Device role
  limited to sensing and minimal forwarding.
- **Alternatives considered**: Moving parsing, inference, or pruning onto the
  Device was rejected because it violates the constitution’s energy boundary.

### Transport security

- **Decision**: Use HTTPS, per-device credentials, server certificate validation,
  and device-scoped authorization.
- **Rationale**: This supports authenticated provenance, credential revocation,
  least privilege, and cross-device isolation.
- **Alternatives considered**: Shared API keys and simulated-only authentication
  were rejected because they weaken identity and security acceptance tests.

### Edge decision boundary

- **Decision**: Edge validates the JSON envelope, derives features, detects health
  anomalies, prunes data, and owns the first intelligence decision.
- **Rationale**: Local processing protects bandwidth and energy while allowing
  autonomy when upstream services are unavailable.
- **Alternatives considered**: Cloud-first inference was rejected because it adds
  latency and violates the mandated hierarchy.

### Silent-failure detection

- **Decision**: Compare physical plausibility, freshness, drift, context, and
  independent diagnostics rather than trusting packets or current draw alone.
- **Rationale**: A sensor can be transport-healthy while physically blind or biased.
- **Alternatives considered**: Uptime-only health was rejected as insufficient.

### Diagnostic safety

- **Decision**: Automatically run read-only diagnostics; require Validator approval
  for control-changing diagnostic deployment.
- **Rationale**: This enables proactive integrity response without allowing an
  autonomous agent to alter control behavior outside the approved command set.
- **Alternatives considered**: Automatic control-changing deployment was rejected
  due to rollback, authorization, and physical safety risk.

### Planning unknowns

- **Decision**: Defer exact board model, pin mapping, endpoint, units, sampling,
  retention, and server implementation language to implementation planning.
- **Rationale**: These choices do not change the feature’s contract or tier boundary.
- **Alternatives considered**: Prematurely selecting a server stack was rejected
  because this is a conceptual blueprint and no existing runtime is present.