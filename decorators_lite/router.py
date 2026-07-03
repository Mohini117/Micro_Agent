def route_action(action):
    match action["type"]:
        case "tool_call":
            return f"Executing tool: {action['tool_name']}"
        case "final_answer":
            return f"Final answer: {action['content']}"
        case "error":
            return f"Error occurred: {action['message']}"
        case _:
            return "Unrecognized action type"


if __name__ == "__main__":
    examples = [
        {"type": "tool_call", "tool_name": "search_medicine_db", "arguments": {"query": "paracetamol"}},
        {"type": "final_answer", "content": "The medicine is safe to take with food."},
        {"type": "error", "message": "Could not parse model output"},
        {"type": "unknown_thing"}
    ]

    for example in examples:
        print(route_action(example))
