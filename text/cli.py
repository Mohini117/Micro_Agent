from message import Message
from text.memory import create_memory
from decorators_lite.parser import parse_tool_call
from decorators_lite.router import route_action
from text.persistence import save_history

def add_user_message(text, add_message):
    msg = Message(role="user", content=text)
    add_message(msg)

def parse_and_route(text):
    parsed_result = parse_tool_call(text)
    if parsed_result:
        action = {"type": "tool_call", **parsed_result}
    else:
        action = {"type": "final_answer", "content": text}
    result = route_action(action)
    print(result)

if __name__ == "__main__":
    add_message, get_history = create_memory()

    while True:
        text = input("> ")

        if text == "exit":
            save_history(get_history(), "conversation.json")
            print("Saving conversation... done.")
            break

        add_user_message(text, add_message)
        parse_and_route(text)