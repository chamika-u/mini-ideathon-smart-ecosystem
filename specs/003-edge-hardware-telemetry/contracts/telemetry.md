# Telemetry Contract

## Device-to-Edge Request

The Device sends an HTTP POST with `Content-Type: application/json` over HTTPS.
The request is authenticated with credentials scoped to the sending device.

```json
{
  "timestamp": "2026-09-04T12:00:00Z",
  "device_id": "energy-node-01",
  "metric": "voltage",
  "value": 230.4,
  "unit": "V",
  "schema_version": "1.0",
  "source_health": {
    "uptime": 1.0,
    "packet_sequence": 1842
  }
}
```

Required fields are `timestamp`, `device_id`, `metric`, and `value`. Energy, air,
and water metrics use the same envelope. Edge MUST reject missing or invalid
required fields and MUST not forward raw streams to Platform services.

## Response Outcomes

- `2xx`: accepted for Edge processing
- `4xx`: rejected; Device records contract or authorization failure
- `5xx` or timeout: retry within bounded policy; Device does not claim acceptance
- certificate or credential failure: reject and raise transport-security evidence

## Health Semantics

Transport uptime and packet continuity are not physical health. Edge MUST assess
freshness, plausible range, expected variation, calibration drift, environmental
context, and independent diagnostics before marking a source healthy.