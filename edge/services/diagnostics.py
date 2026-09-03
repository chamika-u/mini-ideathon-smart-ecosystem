from edge.models import DiagnosticWorkItem


class DiagnosticCoordinator:
    def create_work_item(self, device_id: str, failure_signal: str, hypothesis: str) -> DiagnosticWorkItem:
        return DiagnosticWorkItem(
            work_item_id=f"diagnostic-{device_id}",
            failure_signal=failure_signal,
            hypothesis=hypothesis,
            diagnostic_steps=["read_packet_sequence", "inspect_value_variation", "compare_expected_range"],
            test_result="pending",
            authorization_state="read_only",
            dashboard_destination="platform/alerts/diagnostics.json",
        )

    def run_read_only(self, item: DiagnosticWorkItem, values: list[float], expected_range: tuple[float, float]) -> DiagnosticWorkItem:
        item.test_result = "degraded_measurement" if len(set(values)) == 1 or not all(expected_range[0] <= value <= expected_range[1] for value in values) else "no_failure_detected"
        return item

    def authorize_control_change(self, item: DiagnosticWorkItem, approved: bool) -> DiagnosticWorkItem:
        item.authorization_state = "validator_approved" if approved else "blocked_pending_validator"
        return item
