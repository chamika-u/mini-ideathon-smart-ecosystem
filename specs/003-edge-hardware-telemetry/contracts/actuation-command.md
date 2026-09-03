# Actuation Command Contract

## Validated Command

Only the Decision / Validator Agent may issue this contract to the Action Agent.

```json
{
  "command_id": "cmd-0001",
  "target": "local-relay-01",
  "command_set_id": "microgrid-safe-v1",
  "scope": "reduce_load_group_a",
  "expires_at": "2026-09-04T12:00:05Z",
  "stop_condition": "voltage_outside_safe_range",
  "authorization": {
    "actor": "validator-agent",
    "policy_result": "approved"
  },
  "audit_reference": "assessment-0001"
}
```

The receiving Action Agent MUST reject missing authorization, expired commands,
unknown command sets, duplicate command IDs, and commands outside their declared
scope. The actuator MUST report whether the intended physical state changed. A
follow-up Device Observation MUST reference the command to close the loop.