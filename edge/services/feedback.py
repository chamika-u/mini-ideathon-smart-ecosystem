from edge.models import FeedbackRecord


def record_feedback(command_id: str, intended_effect: str, observed_effect: dict, outcome: str, learning_approval: bool) -> FeedbackRecord:
    return FeedbackRecord(command_id, intended_effect, observed_effect, outcome, learning_approval)
