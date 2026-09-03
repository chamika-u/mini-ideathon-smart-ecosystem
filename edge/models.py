from dataclasses import dataclass, field
from typing import Any


@dataclass
class DeviceObservation:
    timestamp: str
    device_id: str
    metric: str
    value: Any
    unit: str = ""
    schema_version: str = "1.0"
    source_health: dict[str, Any] = field(default_factory=dict)


@dataclass
class EdgeAssessment:
    assessment_id: str
    device_id: str
    feature_summary: dict[str, Any]
    classification: str
    confidence: float
    health_state: str
    retention_decision: str
    requested_action: str | None = None
    provenance: list[str] = field(default_factory=list)


@dataclass
class ValidatedCommand:
    command_id: str
    target: str
    command_set_id: str
    scope: str
    expires_at: str
    stop_condition: str
    authorization: dict[str, str]
    audit_reference: str


@dataclass
class FeedbackRecord:
    command_id: str
    intended_effect: str
    observed_effect: dict[str, Any]
    outcome: str
    learning_approval: bool


@dataclass
class DiagnosticWorkItem:
    work_item_id: str
    failure_signal: str
    hypothesis: str
    diagnostic_steps: list[str]
    test_result: str
    authorization_state: str
    dashboard_destination: str
