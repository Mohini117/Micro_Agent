TOOLS = {}

def register_tool(func):
    # func is the function passed in (like Layer 3)
    # your job: save func into TOOLS, keyed by its name
    # then return func back (like Layer 4, but returning the SAME func, not a new one)
    TOOLS[func.__name__] = func
    return func



@register_tool
def search_medicine_db(query):
    return f"Results for {query}"

@register_tool
def get_weather(city):
    return f"Weather in {city}"

print(TOOLS)
# Output: {'search_medicine_db': <function search_medicine_db at 0x...>, 'get_weather': <function get_weather at 0x...>}

result = TOOLS["search_medicine_db"]("paracetamol")
print(result)
# Output: Results for paracetamol

"""
def log_call(func):
    def wrapper( *args, **kwargs):
        print(f"calling {func.__name__}...")
        result = func(*args,**kwargs)
        print(f"{func.__name__}  finished")
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
