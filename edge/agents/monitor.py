from edge.models import EdgeAssessment, DeviceObservation
from edge.services.health import assess_health


class MonitorAgent:
    def __init__(self):
        self.history: dict[tuple[str, str], list[float]] = {}

    def assess(self, observation: DeviceObservation, expected_range=(0.0, 1000.0), sdg_constraints=None) -> EdgeAssessment:
        key = (observation.device_id, observation.metric)
        values = self.history.setdefault(key, [])
        if isinstance(observation.value, (int, float)):
            values.append(float(observation.value))
        health = assess_health(values, expected_range, observation.source_health.get("uptime", 1.0), observation.source_health.get("packet_sequence", 0))
        anomaly = health["state"] == "degraded" or (isinstance(observation.value, (int, float)) and observation.value > expected_range[1])
        classification = "anomaly" if anomaly else "normal"
        action = "reduce_load" if anomaly else None
        return EdgeAssessment(f"assessment-{len(values)}", observation.device_id, {"latest": observation.value, "sdg_constraints": sdg_constraints or {}}, classification, 0.95 if anomaly else 0.8, health["state"], "forwarded" if anomaly else "pruned", action, [observation.timestamp])
