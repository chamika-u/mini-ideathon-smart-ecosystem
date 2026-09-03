from dataclasses import dataclass

from .config import VirtualSensorConfig


@dataclass(frozen=True)
class TransportResult:
    status_code: int
    accepted: bool
    detail: str


class VirtualWiFi:
    """Mock Wi-Fi facade retaining the names used by the hardware contract."""

    def __init__(self, config: VirtualSensorConfig):
        self.config = config
        self.connected = False

    def connect(self, credentials: str) -> bool:
        self.connected = credentials == self.config.credential
        return self.connected

    def localIP(self) -> str:
        if not self.connected:
            raise RuntimeError("virtual sensor is not connected")
        return self.config.local_ip


class VirtualHTTPClient:
    """Mock HTTPClient facade for deterministic Device-to-Edge tests."""

    def post(self, payload: str, headers: dict[str, str], server: "MockEdgeServer") -> TransportResult:
        if headers.get("Content-Type") != "application/json":
            return TransportResult(415, False, "application/json content type required")
        return server.receive(payload)


class MockEdgeServer:
    def __init__(self, expected_device_id: str, credential_store, certificate_validator):
        self.expected_device_id = expected_device_id
        self.credential_store = credential_store
        self.certificate_validator = certificate_validator
        self.received: list[dict] = []
        from edge.services.telemetry_ingress import TelemetryIngress

        self.ingress = TelemetryIngress()

    def receive(self, payload: str) -> TransportResult:
        import json

        try:
            observation = json.loads(payload)
        except json.JSONDecodeError:
            return TransportResult(400, False, "malformed JSON")
        if observation.get("device_id") != self.expected_device_id:
            return TransportResult(403, False, "device identity rejected")
        try:
            self.ingress.accept(payload)
        except (ValueError, TypeError) as error:
            return TransportResult(400, False, str(error))
        self.received.append(observation)
        return TransportResult(202, True, "accepted for Edge processing")
