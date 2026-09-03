class PlannerAgent:
    def plan(self, assessment, constraints: dict) -> dict:
        return {"assessment_id": assessment.assessment_id, "action": assessment.requested_action, "constraints": constraints, "evidence": assessment.feature_summary, "authorized": False}
