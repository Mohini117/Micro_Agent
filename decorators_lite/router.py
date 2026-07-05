import sys
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.append(str(PROJECT_ROOT))

from registry import TOOLS


def route_action(action, tools=None):
    if tools is None:
        tools = TOOLS

    match action["type"]:
        case "tool_call":
            return execute_tool(action, tools)
        case "final_answer":
            return f"Final answer: {action['content']}"
        case "error":
            return f"Error occurred: {action['message']}"
        case _:
            return "Unrecognized action type"


def execute_tool(action, tools):
    tool_name = action["tool_name"]
    arguments = action.get("arguments", {})
    tool = tools.get(tool_name)

    if tool is None:
        return f"Unknown tool: {tool_name}"

    try:
        result = tool(**arguments)
    except TypeError as exc:
        return f"Tool argument error for {tool_name}: {exc}"

    return f"Tool result: {result}"


if __name__ == "__main__":
    examples = [
        {"type": "tool_call", "tool_name": "search_medicine_db", "arguments": {"query": "paracetamol"}},
        {"type": "tool_call", "tool_name": "get_weather", "arguments": {"city": "New York"}},
        {"type": "final_answer", "content": "The medicine is safe to take with food."},
        {"type": "error", "message": "Could not parse model output"},
        {"type": "unknown_thing"},
    ]

    for example in examples:
        print(route_action(example))
