# Data Model: Edge Hardware Telemetry

## Device Observation

Represents one measurement emitted by a Device and received at the Edge boundary.

- `timestamp`: required event time
- `device_id`: required stable device identity
- `metric`: required canonical measurement name
- `value`: required numeric or bounded scalar measurement
- `unit`: required measurement unit when the metric has one
- `schema_version`: contract version
- `transport_status`: delivery result and retry context
- `source_health`: freshness, plausibility, drift, and diagnostic indicators

Validation: reject missing identity or measurement fields; quarantine malformed,
duplicate, delayed, or out-of-order observations according to contract policy.

## Edge Assessment

Represents the Edge result after feature extraction and local reasoning.

- `assessment_id`: unique assessment identity
- `device_id`: source identity
- `feature_summary`: pruned derived features
- `classification`: event or health classification
- `confidence`: bounded confidence value
- `health_state`: healthy, degraded, or unknown
- `retention_decision`: retained, aggregated, pruned, or forwarded
- `requested_action`: optional proposed command
- `provenance`: source and transformation references

## Validated Command

Represents an action approved by the Decision / Validator Agent.

- `command_id`: unique command identity
- `target`: actuator identity
- `command_set_id`: approved command-set reference
- `scope`: permitted effect and resource boundary
- `expires_at`: command expiry
- `stop_condition`: mandatory safety stop
- `authorization`: actor and policy result
- `audit_reference`: immutable decision link

## Diagnostic Work Item

Represents proactive silent-failure investigation.

- `work_item_id`: unique diagnostic identity
- `failure_signal`: observed integrity anomaly
- `hypothesis`: Researcher output
- `diagnostic_steps`: read-only checks prepared by Engineer
- `test_result`: Tester output
- `authorization_state`: whether changes require Validator approval
- `dashboard_destination`: Designer-routed alert location

## Feedback Record

Represents loop closure.

- `command_id`: executed command reference
- `intended_effect`: target physical change
- `observed_effect`: follow-up Device measurement
- `outcome`: success, degraded, or failed
- `learning_approval`: approval to update rules or models

Relationships: Device Observation produces an Edge Assessment; an assessment may
request a Validated Command; the command produces a Feedback Record; degraded
observations produce a Diagnostic Work Item.