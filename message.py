from datetime import datetime
from uuid import uuid4


class Message:
    def __init__(self, role, content, timestamp=None):
        self.role = role
        self.content = content
        if timestamp is None:
            timestamp = datetime.now()
        self.timestamp = timestamp

    def __str__(self):
        return f"[{self.role}] : {self.content}"


class ToolCall:
    def __init__(self, tool_name, arguments, call_id=None):
        self.tool_name = tool_name
        self.arguments = arguments
        if call_id is None:
            call_id = str(uuid4())
        self.call_id = call_id

    def __str__(self):
        return f"ToolCall({self.tool_name}, {self.arguments})"

    def __repr__(self):
        return f"ToolCall(tool_name='{self.tool_name}', arguments={self.arguments})"

    def __eq__(self, other):
        if not isinstance(other, ToolCall):
            return False
        return self.tool_name == other.tool_name and self.arguments == other.arguments

    def __hash__(self):
        return hash((self.tool_name, make_hashable(self.arguments)))


def make_hashable(value):
    if isinstance(value, dict):
        return tuple(sorted((key, make_hashable(item)) for key, item in value.items()))
    if isinstance(value, list):
        return tuple(make_hashable(item) for item in value)
    if isinstance(value, set):
        return frozenset(make_hashable(item) for item in value)
    return value
