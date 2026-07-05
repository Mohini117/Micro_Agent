from message import Message, ToolCall
from text.memory import create_memory
from decorators_lite.parser import parse_tool_call
from decorators_lite.router import route_action
from text.dedupe import is_duplicate_call, remember_call
from text.persistence import save_history


def add_user_message(text, add_message):
    msg = Message(role="user", content=text)
    add_message(msg)


def parse_and_route(text, seen_calls):
    try:
        parsed_result = parse_tool_call(text)
    except (SyntaxError, ValueError) as exc:
        action = {"type": "error", "message": str(exc)}
        print(route_action(action))
        return

    if parsed_result:
        tool_call = ToolCall(parsed_result["tool_name"], parsed_result["arguments"])
        if is_duplicate_call(tool_call, seen_calls):
            print(f"Duplicate tool call skipped: {tool_call.tool_name}")
            return

        remember_call(tool_call, seen_calls)
        action = {"type": "tool_call", **parsed_result}
    else:
        action = {"type": "final_answer", "content": text}

    result = route_action(action)
    print(result)


if __name__ == "__main__":
    add_message, get_history = create_memory()
    seen_calls = set()

    while True:
        text = input("> ")

        if text == "exit":
            save_history(get_history(), "conversation.json")
            print("Saving conversation... done.")
            break

        add_user_message(text, add_message)
        parse_and_route(text, seen_calls)
