from message import Message, ToolCall


if __name__ == "__main__":
    first = Message("user", "first message")
    second = Message("user", "second message")

    print(first)
    print(second)
    print(first.timestamp <= second.timestamp)

    tc1 = ToolCall("search_medicine_db", {"query": "paracetamol"})
    tc2 = ToolCall("search_medicine_db", {"query": "paracetamol"})
    tc3 = ToolCall("search_medicine_db", {"query": "ibuprofen"})

    print(tc1 == tc2)
    print(tc1 == tc3)
    print(hash(tc1) == hash(tc2))
    print(repr(tc1))
