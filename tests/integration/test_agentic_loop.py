import unittest
from time import perf_counter
from datetime import datetime, timedelta, timezone

from edge.agents.action import ActionAgent
from edge.agents.monitor import MonitorAgent
from edge.agents.planner import PlannerAgent
from edge.agents.validator import ValidatorAgent
from edge.models import DeviceObservation
from edge.services.feedback import record_feedback
from edge.services.validator import CommandPolicy


class AgenticLoopTests(unittest.TestCase):
    def test_validated_action_changes_state_and_creates_feedback(self):
        timestamp = datetime.now(timezone.utc).isoformat()
        observation = DeviceObservation(timestamp, "energy-node-01", "voltage", 950, "V", source_health={"uptime": 1.0, "packet_sequence": 1})
        assessment = MonitorAgent().assess(observation, expected_range=(0, 240), sdg_constraints={"energy": "efficient"})
        plan = PlannerAgent().plan(assessment, {"max_voltage": 240})
        self.assertFalse(plan["authorized"])
        command = {"command_id": "cmd-1", "target": "load_group_a", "command_set_id": "microgrid-safe-v1", "scope": "reduce_load_group_a", "expires_at": (datetime.now(timezone.utc) + timedelta(seconds=5)).isoformat(), "stop_condition": "voltage_outside_safe_range", "authorization": {"policy_result": "approved"}, "audit_reference": assessment.assessment_id}
        validator = ValidatorAgent(CommandPolicy({"microgrid-safe-v1"}))
        self.assertTrue(validator.validate(command))
        result = ActionAgent(validator).execute(command)
        feedback = record_feedback(command["command_id"], "reduce load", result, "success", True)
        self.assertTrue(feedback.observed_effect["changed"])
        self.assertEqual(feedback.outcome, "success")

    def test_local_actions_meet_latency_target_and_feedback_changes_next_decision(self):
        validator = ValidatorAgent(CommandPolicy({"microgrid-safe-v1"}))
        action = ActionAgent(validator)
        monitor = MonitorAgent()
        durations = []
        for index in range(100):
            command = {"command_id": f"latency-{index}", "target": "load_group_a", "command_set_id": "microgrid-safe-v1", "scope": "reduce_load_group_a", "expires_at": (datetime.now(timezone.utc) + timedelta(seconds=5)).isoformat(), "stop_condition": "voltage_outside_safe_range", "authorization": {"policy_result": "approved"}, "audit_reference": f"assessment-{index}"}
            start = perf_counter()
            result = action.execute(command)
            durations.append(perf_counter() - start)
            feedback = record_feedback(command["command_id"], "reduce load", result, "success", True)
            follow_up = monitor.assess(DeviceObservation(datetime.now(timezone.utc).isoformat(), "energy-node-01", "load_state", feedback.observed_effect["state"], source_health={"uptime": 1.0, "packet_sequence": index + 1}))
            self.assertEqual(follow_up.feature_summary["latest"], "reduced")
        self.assertGreaterEqual(sum(duration < 1.0 for duration in durations), 95)

    def test_action_rejects_invalid_commands(self):
        validator = ValidatorAgent(CommandPolicy({"microgrid-safe-v1"}))
        action = ActionAgent(validator)
        base = {"command_id": "negative-1", "target": "load_group_a", "command_set_id": "microgrid-safe-v1", "scope": "reduce_load_group_a", "expires_at": (datetime.now(timezone.utc) + timedelta(seconds=5)).isoformat(), "stop_condition": "voltage_outside_safe_range", "authorization": {"policy_result": "approved"}, "audit_reference": "assessment-negative"}
        self.assertRaises(PermissionError, ActionAgent().execute, base)
        expired = dict(base, command_id="negative-2", expires_at=(datetime.now(timezone.utc) - timedelta(seconds=1)).isoformat())
        self.assertRaises(PermissionError, action.execute, expired)
        missing_stop = dict(base, command_id="negative-3", stop_condition="")
        self.assertRaises(PermissionError, action.execute, missing_stop)
        unsupported = dict(base, command_id="negative-4", scope="open_breaker")
        self.assertRaises(ValueError, action.execute, unsupported)
        action.execute(base)
        self.assertRaises(ValueError, action.execute, base)


if __name__ == "__main__":
    unittest.main()