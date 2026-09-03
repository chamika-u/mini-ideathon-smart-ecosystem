import json
from datetime import datetime, timezone

from .config import VirtualSensorConfig
from .network import MockEdgeServer, TransportResult, VirtualHTTPClient, VirtualWiFi
from .security import CredentialStore, ServerCertificateValidator


REQUIRED_FIELDS = ("timestamp", "device_id", "metric", "value")


def serialize_observation(device_id: str, metric: str, value, unit: str = "") -> str:
    observation = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "device_id": device_id,
        "metric": metric,
        "value": value,
        "unit": unit,
        "schema_version": "1.0",
        "source_health": {"uptime": 1.0, "packet_sequence": 1},
    }
    return json.dumps(observation, sort_keys=True)


class VirtualSensor:
    def __init__(self, config: VirtualSensorConfig, server: MockEdgeServer, credential_store: CredentialStore, certificate_validator: ServerCertificateValidator):
        self.config = config
        self.server = server
        self.credentials = credential_store
        self.certificates = certificate_validator
        self.wifi = VirtualWiFi(config)
        self.http = VirtualHTTPClient()

    def connect(self) -> str:
        if not self.wifi.connect(self.config.credential):
            raise ConnectionError("virtual Wi-Fi connection failed")
        address = self.wifi.localIP()
        print(address)
        return address

    def send(self, metric: str, value, unit: str = "") -> TransportResult:
        if not self.credentials.authenticate(self.config.device_id, self.config.credential):
            return TransportResult(401, False, "device credential rejected")
        if not self.certificates.validate("demo-server-fingerprint"):
            return TransportResult(495, False, "server certificate rejected")
        payload = serialize_observation(self.config.device_id, metric, value, unit)
        return self.http.post(payload, {"Content-Type": "application/json"}, self.server)
