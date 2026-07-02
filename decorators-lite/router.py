def route_action(action):
    # action is a dict, e.g. {"type": "tool_call", "tool_name": "...", "arguments": {...}}
    match action["type"]:
        case "tool_call":
            return f"Executing tool: {action['tool_name']}"
        case "final_answer":
            return f"Final answer: {action['content']}"
        case "error":
            return f"Error occurred: {action['message']}"
        case _:
            return "Unrecognized action type"
        
        
print(route_action({"type": "tool_call", "tool_name": "search_medicine_db", "arguments": {"query": "paracetamol"}}))
# Output: "Executing tool: search_medicine_db"

print(route_action({"type": "final_answer", "content": "The medicine is safe to take with food."}))
# Output: "Final answer: The medicine is safe to take with food."

print(route_action({"type": "error", "message": "Could not parse model output"}))
# Output: "Error occurred: Could not parse model output"

print(route_action({"type": "unknown_thing"}))
# Output: "Unrecognized action type"

