from message import Message

def create_memory():
    history = []   # question: where does this live, and why does it matter?
    
    def add_message(message):
        # append message to history
        history.append(message)
    
    def get_history():
        # return history
        return history
    
    return add_message, get_history   # returning two functions at once

add_message, get_history = create_memory()

add_message(Message("user", "What does this medicine do?"))
add_message(Message("assistant", "It's for blood pressure."))

history = get_history()
print(len(history))     # Output: 2
print(history[0].content)  # Output: What does this medicine do?

# get_history, add_message = create_memory()

# get_history(Message("user", "test"))   # this variable actually holds add_message's function!
# print(add_message())                     # this variable actually holds get_history's function!