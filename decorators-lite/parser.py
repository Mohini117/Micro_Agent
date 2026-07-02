import re
 
def parse_tool_call(text):
    match = re.search(r'TOOL_CALL: (\w+)\((\w+)="(\w+)"\)', text)
    if match:
        # build and return the dict here using match.group(1), group(2), group(3)
        group1 = match.group(1)
        group2 = match.group(2)
        group3 = match.group(3)
        return {"tool_name": group1, "arguments": {group2: group3}}
    
    return None


text1 = 'TOOL_CALL: search_medicine_db(query="paracetamol")'
print(parse_tool_call(text1))
# Output: {'tool_name': 'search_medicine_db', 'arguments': {'query': 'paracetamol'}}

text2 = "The medicine is safe to take with food."
print(parse_tool_call(text2))
# Output: None

text3 = 'TOOL_CALL: get_weather(city="Nagpur")'
print(parse_tool_call(text3))
# Output: {'tool_name': 'get_weather', 'arguments': {'city': 'Nagpur'}}