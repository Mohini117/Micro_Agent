TOOLS = {}


def register_tool(func):
    TOOLS[func.__name__] = func
    return func


@register_tool
def search_medicine_db(query):
    return f"Results for {query}"


@register_tool
def get_weather(city, unit="celsius"):
    return f"Weather in {city} ({unit})"


if __name__ == "__main__":
    print(TOOLS)
    result = TOOLS["search_medicine_db"]("paracetamol")
    print(result)

"""
def log_call(func):
    def wrapper(*args, **kwargs):
        print(f"calling {func.__name__}...")
        result = func(*args, **kwargs)
        print(f"{func.__name__} finished")
        return result
    return wrapper


@log_call
def add(a, b):
    return a + b


@log_call
def get_weather(city):
    return f"Weather in {city}"


print(add(3, 4))
print(get_weather("Nagpur"))
"""
