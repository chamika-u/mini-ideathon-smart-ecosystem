class ActionAgent:
    def __init__(self, validator=None):
        self.state = {"load_group_a": "normal"}
        self.validator = validator
        self.executed: set[str] = set()

    def execute(self, command: dict) -> dict:
        if self.validator is None or not self.validator.validate(command):
            raise PermissionError("command was not validated")
        if command["command_id"] in self.executed:
            raise ValueError("duplicate command ID")
        if command["scope"] == "reduce_load_group_a":
            self.state["load_group_a"] = "reduced"
        else:
            raise ValueError("unsupported command scope")
        self.executed.add(command["command_id"])
        return {"target": command["target"], "state": self.state["load_group_a"], "changed": True}
