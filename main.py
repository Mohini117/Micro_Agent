from message import Message, ToolCall

m = Message("user", "What does this medicine do?")
print(m.role)
print(m.content)
print(m.timestamp)

print(m)
"""
import time

m1 = Message("user", "first message")
time.sleep(3)   # pause 3 seconds
m2 = Message("user", "second message")

print(m1.timestamp)
print(m2.timestamp)
"""

tc =ToolCall("search_medicine_db", {"query": "paracetamol"})


print(tc.tool_name)
# Output: search_medicine_db

print(tc.arguments)
# Output: {'query': 'paracetamol'}

print(tc.call_id)
# Output: some unique string, e.g. a UUID like 'a1b2c3d4-...'

tc1 = ToolCall("tool_a", {"x": 1})
tc2 = ToolCall("tool_a", {"x": 1})
print(tc1.call_id)
print(tc2.call_id)
print(tc1.call_id == tc2.call_id)


tc1 = ToolCall("search_medicine_db", {"query": "paracetamol"})
tc2 = ToolCall("search_medicine_db", {"query": "paracetamol"})
tc3 = ToolCall("search_medicine_db", {"query": "ibuprofen"})

print(tc1 == tc2)   # should print True
print(tc1 == tc3)   # should print False
print(tc1==5)          # readable string
print(repr(tc1))    # repr-style string