import unittest

from device.src.config import VirtualSensorConfig
from device.src.network import MockEdgeServer
from device.src.security import CredentialStore, DeviceCredential, ServerCertificateValidator
from device.src.telemetry import VirtualSensor, serialize_observation
from edge.services.reliability import ReliableBuffer


class DeviceRecoveryTests(unittest.TestCase):
    def test_failed_delivery_is_buffered_and_replayed(self):
        config = VirtualSensorConfig("energy-node-01")
        credentials = CredentialStore([DeviceCredential(config.device_id, config.credential)])
        server = MockEdgeServer(config.device_id, credentials, ServerCertificateValidator("demo-server-fingerprint"), transient_failures=3)
        sensor = VirtualSensor(config, server, credentials, ServerCertificateValidator("demo-server-fingerprint"))
        self.assertEqual(sensor.send("voltage", 230, "V").status_code, 503)
        self.assertEqual(len(sensor.buffer.items), 1)
        server.transient_failures = 0
        replayed = sensor.replay_buffer()
        self.assertTrue(replayed[0].accepted)
        self.assertEqual(server.received[0]["metric"], "voltage")

    def test_transient_http_failure_is_retried(self):
        config = VirtualSensorConfig("energy-node-01")
        credentials = CredentialStore([DeviceCredential(config.device_id, config.credential)])
        server = MockEdgeServer(config.device_id, credentials, ServerCertificateValidator("demo-server-fingerprint"), transient_failures=1)
        sensor = VirtualSensor(config, server, credentials, ServerCertificateValidator("demo-server-fingerprint"))
        self.assertTrue(sensor.send("voltage", 230).accepted)
        self.assertEqual(len(server.received), 1)

    def test_invalid_certificate_is_rejected(self):
        config = VirtualSensorConfig("energy-node-01")
        credentials = CredentialStore([DeviceCredential(config.device_id, config.credential)])
        server = MockEdgeServer(config.device_id, credentials, ServerCertificateValidator("trusted"))
        sensor = VirtualSensor(config, server, credentials, ServerCertificateValidator("untrusted"))
        self.assertEqual(sensor.send("voltage", 230).status_code, 495)


if __name__ == "__main__":
    unittest.main()