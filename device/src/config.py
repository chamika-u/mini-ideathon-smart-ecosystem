from dataclasses import dataclass


@dataclass(frozen=True)
class VirtualSensorConfig:
    device_id: str
    local_ip: str = "192.0.2.10"
    endpoint: str = "https://edge.invalid/telemetry"
    credential: str = "demo-device-credential"
