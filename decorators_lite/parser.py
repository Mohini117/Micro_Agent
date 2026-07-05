import ast
import re


TOOL_CALL_PATTERN = re.compile(r'^\s*TOOL_CALL:\s*([A-Za-z_]\w*)\((.*)\)\s*$')


def parse_tool_call(text):
    match = TOOL_CALL_PATTERN.search(text)
    if not match:
        return None

    tool_name = match.group(1)
    argument_text = match.group(2).strip()
    arguments = parse_arguments(argument_text)
    return {"tool_name": tool_name, "arguments": arguments}


def parse_arguments(argument_text):
    if not argument_text:
        return {}

    expression = ast.parse(f"tool({argument_text})", mode="eval")
    call = expression.body
    if not isinstance(call, ast.Call) or call.args:
        raise ValueError("Tool calls must use keyword arguments only")

    arguments = {}
    for keyword in call.keywords:
        if keyword.arg is None:
            raise ValueError("Tool calls do not support **kwargs")
        arguments[keyword.arg] = ast.literal_eval(keyword.value)
    return arguments


if __name__ == "__main__":
    examples = [
        'TOOL_CALL: search_medicine_db(query="paracetamol")',
        'TOOL_CALL: get_weather(city="New York")',
        'TOOL_CALL: get_weather(city="Nagpur", unit="celsius")',
        "The medicine is safe to take with food.",
    ]

    for example in examples:
        print(parse_tool_call(example))
