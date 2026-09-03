import json
import unittest

from device.src.config import VirtualSensorConfig
from device.src.network import MockEdgeServer
from device.src.security import CredentialStore, DeviceCredential, ServerCertificateValidator
from device.src.telemetry import VirtualSensor


class DeviceTelemetryContractTests(unittest.TestCase):
    def test_virtual_sensor_sends_authenticated_json(self):
        config = VirtualSensorConfig("energy-node-01")
        credentials = CredentialStore([DeviceCredential(config.device_id, config.credential)])
        server = MockEdgeServer(config.device_id, credentials, ServerCertificateValidator("demo-server-fingerprint"))
        sensor = VirtualSensor(config, server, credentials, ServerCertificateValidator("demo-server-fingerprint"))
        self.assertEqual(sensor.connect(), "192.0.2.10")
        result = sensor.send("voltage", 230.4, "V")
        self.assertTrue(result.accepted)
        self.assertEqual(set(("timestamp", "device_id", "metric", "value")), set(server.received[0]).intersection(("timestamp", "device_id", "metric", "value")))

    def test_invalid_credential_is_rejected(self):
        config = VirtualSensorConfig("energy-node-01", credential="wrong")
        credentials = CredentialStore([DeviceCredential(config.device_id, "real")])
        server = MockEdgeServer(config.device_id, credentials, ServerCertificateValidator("demo-server-fingerprint"))
        sensor = VirtualSensor(config, server, credentials, ServerCertificateValidator("demo-server-fingerprint"))
        self.assertFalse(sensor.send("voltage", 1).accepted)


if __name__ == "__main__":
    unittest.main()