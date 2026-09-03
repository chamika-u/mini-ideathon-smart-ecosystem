from datetime import datetime, timezone


class CommandPolicy:
    def __init__(self, approved_commands: set[str]):
        self.approved_commands = approved_commands

    def validate(self, command: dict) -> tuple[bool, str]:
        if command.get("command_set_id") not in self.approved_commands:
            return False, "command set is not approved"
        authorization = command.get("authorization", {})
        if authorization.get("policy_result") != "approved":
            return False, "authorization is not approved"
        if not command.get("stop_condition"):
            return False, "stop condition is required"
        try:
            expires_at = datetime.fromisoformat(command["expires_at"].replace("Z", "+00:00"))
        except (KeyError, ValueError):
            return False, "invalid expiry"
        if expires_at <= datetime.now(timezone.utc):
            return False, "command expired"
        return True, "approved"
