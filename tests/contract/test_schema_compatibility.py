import json
import unittest
from pathlib import Path


class SchemaCompatibilityTests(unittest.TestCase):
    def test_contract_schemas_have_stable_required_fields(self):
        root = Path(__file__).parents[2]
        telemetry = json.loads((root / "edge/telemetry_schema.json").read_text())
        command = json.loads((root / "edge/actuation_command_schema.json").read_text())
        self.assertEqual(telemetry["required"], ["timestamp", "device_id", "metric", "value"])
        self.assertIn("command_id", command["required"])


if __name__ == "__main__":
    unittest.main()