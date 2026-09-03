class ActionAgent:
    def __init__(self):
        self.state = {"load_group_a": "normal"}

    def execute(self, command: dict) -> dict:
        if command["scope"] == "reduce_load_group_a":
            self.state["load_group_a"] = "reduced"
        return {"target": command["target"], "state": self.state["load_group_a"], "changed": True}
