from edge.services.validator import CommandPolicy


class ValidatorAgent:
    def __init__(self, policy: CommandPolicy):
        self.policy = policy
        self.audit_log: list[dict] = []

    def validate(self, command: dict) -> bool:
        valid, reason = self.policy.validate(command)
        self.audit_log.append({"command_id": command.get("command_id"), "valid": valid, "reason": reason})
        return valid
