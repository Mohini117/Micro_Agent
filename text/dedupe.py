from message import ToolCall, make_hashable


def make_call_key(tool_call):
    return (tool_call.tool_name, make_hashable(tool_call.arguments))


def is_duplicate_call(tool_call, seen_calls):
    return make_call_key(tool_call) in seen_calls


def remember_call(tool_call, seen_calls):
    seen_calls.add(make_call_key(tool_call))


if __name__ == "__main__":
    seen_calls = set()

    tc1 = ToolCall("search_medicine_db", {"query": "paracetamol"})
    tc2 = ToolCall("search_medicine_db", {"query": "paracetamol"})
    tc3 = ToolCall("search_medicine_db", {"query": "ibuprofen"})

    print(is_duplicate_call(tc1, seen_calls))
    remember_call(tc1, seen_calls)
    print(seen_calls)
    print(is_duplicate_call(tc2, seen_calls))
    print(is_duplicate_call(tc3, seen_calls))
