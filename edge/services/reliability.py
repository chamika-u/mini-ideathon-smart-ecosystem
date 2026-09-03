from collections import deque


class ReliableBuffer:
    def __init__(self, capacity: int = 100):
        self.items = deque(maxlen=capacity)
        self.audit: list[dict] = []

    def add(self, item) -> None:
        self.items.append(item)
        self.audit.append({"event": "buffered", "size": len(self.items)})

    def drain(self) -> list:
        result = list(self.items)
        self.items.clear()
        return result
