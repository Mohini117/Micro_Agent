from message import ToolCall


def make_hashable(tool_call):
    return (tool_call.tool_name, frozenset(tool_call.arguments.items()))


def is_duplicate_call(tool_call, seen_calls):
    hashable = make_hashable(tool_call)
    return hashable in seen_calls


if __name__ == "__main__":
    seen_calls = set()

    tc1 = ToolCall("search_medicine_db", {"query": "paracetamol"})
    tc2 = ToolCall("search_medicine_db", {"query": "paracetamol"})
    tc3 = ToolCall("search_medicine_db", {"query": "ibuprofen"})

    print(is_duplicate_call(tc1, seen_calls))
    seen_calls.add(make_hashable(tc1))
    print(seen_calls)
    print(is_duplicate_call(tc2, seen_calls))
    print(is_duplicate_call(tc3, seen_calls))
