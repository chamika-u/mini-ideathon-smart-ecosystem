import unittest

from device.src.config import VirtualSensorConfig
from device.src.network import MockEdgeServer
from device.src.security import CredentialStore, DeviceCredential, ServerCertificateValidator
from device.src.telemetry import VirtualSensor, serialize_observation
from edge.services.reliability import ReliableBuffer


class DeviceRecoveryTests(unittest.TestCase):
    def test_failed_delivery_is_buffered_and_replayed(self):
        buffer = ReliableBuffer(capacity=2)
        payload = serialize_observation("energy-node-01", "voltage", 230, "V")
        buffer.add(payload)
        replayed = buffer.drain()
        self.assertEqual(len(replayed), 1)
        self.assertIn('"metric": "voltage"', replayed[0])

    def test_invalid_certificate_is_rejected(self):
        config = VirtualSensorConfig("energy-node-01")
        credentials = CredentialStore([DeviceCredential(config.device_id, config.credential)])
        server = MockEdgeServer(config.device_id, credentials, ServerCertificateValidator("trusted"))
        sensor = VirtualSensor(config, server, credentials, ServerCertificateValidator("untrusted"))
        self.assertEqual(sensor.send("voltage", 230).status_code, 495)


if __name__ == "__main__":
    unittest.main()