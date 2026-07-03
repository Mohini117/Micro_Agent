# from text import memory
from message import Message
import json 
from datetime import datetime

def convert_to_dict(message):
    return {
        "role": message.role,
        "content": message.content,
        "timestamp": str(message.timestamp)  # Convert datetime to string for JSON serialization
    }
  

def save_history(history, filepath):
    # history is a list of Message objects
    # 1. convert EACH Message into a plain dict (like you just did for one)
    history_dicts = [convert_to_dict(msg) for msg in history]
    
    # 2. json.dump the resulting LIST of dicts to filepath
    json.dump(history_dicts, open(filepath, "w"), indent=4)
    with open(filepath, "w") as f:
        json.dump(history_dicts, f, indent=4)
    

def load_history(filepath) :
    with open(filepath, "r") as f:
        history_dicts = json.load(f)
        for msg_dict in history_dicts:
            msg_dict["timestamp"] = datetime.fromisoformat(msg_dict["timestamp"])
            
    return [Message(**msg_dict) for msg_dict in history_dicts]


"""
class Message:
    def __init__(self, role, content):
        self.role = role
        self.content = content
        


m = Message("user", "hello")

with open("test.json", "w") as f:
    json.dump(m, f)
    """ 
 

history = [
    Message("user", "What does this medicine do?"),
    Message("assistant", "It's for blood pressure.")
]

save_history(history, "conversation.json")
loaded = load_history("conversation.json")

print(type(loaded[0].timestamp))     # should be <class 'datetime.datetime'>, not str
print(loaded[0].role)
print(loaded[0].content)
print(loaded[0].timestamp == history[0].timestamp)   # should be True — same value, real datetime
    