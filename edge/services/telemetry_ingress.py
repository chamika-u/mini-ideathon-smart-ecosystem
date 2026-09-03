import json

from edge.models import DeviceObservation


class TelemetryIngress:
    required = ("timestamp", "device_id", "metric", "value")

    def __init__(self):
        self.seen: set[tuple[str, str]] = set()
        self.last_timestamp: dict[str, str] = {}

    def accept(self, payload: str) -> DeviceObservation:
        data = json.loads(payload)
        missing = [field for field in self.required if field not in data]
        if missing:
            raise ValueError(f"missing required fields: {', '.join(missing)}")
        key = (data["device_id"], data["timestamp"])
        if key in self.seen:
            raise ValueError("duplicate observation")
        previous = self.last_timestamp.get(data["device_id"])
        if previous and data["timestamp"] < previous:
            raise ValueError("out-of-order observation")
        self.seen.add(key)
        self.last_timestamp[data["device_id"]] = data["timestamp"]
        return DeviceObservation(**{field: data[field] for field in self.required}, unit=data.get("unit", ""), schema_version=data.get("schema_version", "1.0"), source_health=data.get("source_health", {}))

    def prune(self, observation: DeviceObservation) -> dict:
        return {"device_id": observation.device_id, "metric": observation.metric, "value": observation.value, "unit": observation.unit, "schema_version": observation.schema_version}
