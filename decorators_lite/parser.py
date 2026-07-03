import re


def parse_tool_call(text):
    match = re.search(r'TOOL_CALL: (\w+)\((\w+)="(\w+)"\)', text)
    if match:
        tool_name = match.group(1)
        argument_name = match.group(2)
        argument_value = match.group(3)
        return {"tool_name": tool_name, "arguments": {argument_name: argument_value}}

    return None


if __name__ == "__main__":
    examples = [
        'TOOL_CALL: search_medicine_db(query="paracetamol")',
        "The medicine is safe to take with food.",
        'TOOL_CALL: get_weather(city="Nagpur")'
    ]

    for example in examples:
        print(parse_tool_call(example))
