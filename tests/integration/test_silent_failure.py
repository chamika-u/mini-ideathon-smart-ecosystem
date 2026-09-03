import unittest

from edge.agents.monitor import MonitorAgent
from edge.models import DeviceObservation
from edge.services.diagnostics import DiagnosticCoordinator


class SilentFailureTests(unittest.TestCase):
    def test_nominal_transport_does_not_hide_static_sensor(self):
        monitor = MonitorAgent()
        values = [42, 42, 42, 42, 42]
        assessment = None
        for value in values:
            assessment = monitor.assess(DeviceObservation("2026-09-04T12:00:00Z", "air-node-01", "pm25", value, source_health={"uptime": 1.0, "packet_sequence": len(values)}), expected_range=(0, 500))
        self.assertEqual(assessment.health_state, "degraded")
        coordinator = DiagnosticCoordinator()
        item = coordinator.create_work_item("air-node-01", "static_physical_measurement", "sensor output is not varying")
        item = coordinator.orchestrate(item, values, (0, 500))
        self.assertEqual(item.test_result, "degraded_measurement")
        self.assertEqual(item.authorization_state, "read_only")
        self.assertIn("diagnostics.json", item.dashboard_destination)
        self.assertEqual([entry["role"] for entry in coordinator.audit], ["Researcher", "Engineer", "Tester", "Designer"])


if __name__ == "__main__":
    unittest.main()