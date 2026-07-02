import datetime
import random
import uuid
import json
class Message:
    def __init__(self, role, content, timestamp=None):
        self.role = role
        self.content = content
        if timestamp is None:
           timestamp = datetime.datetime.now()
        self.timestamp=timestamp
        
    def __str__(self):
        # Always return a string
        return f"[{self.role}] : {self.content}"

import uuid

class ToolCall:
    def __init__(self, tool_name, arguments, call_id=None):
        self.tool_name = tool_name
        self.arguments = arguments
        if call_id is None:
            call_id = str(uuid.uuid4())
        self.call_id = call_id
    def __str__(self):
    # return something like: ToolCall(search_medicine_db, {'query': 'paracetamol'})
      return f"ToolCall({self.tool_name}, {self.arguments})"

    def __repr__(self):
        # return something like: ToolCall(tool_name='search_medicine_db', arguments={'query': 'paracetamol'})
        return f"ToolCall(tool_name='{self.tool_name}', arguments={self.arguments})"
    
    def __eq__(self, other):
        # return True if self.tool_name == other.tool_name AND self.arguments == other.arguments
        # return False if other is not even a ToolCall
        if isinstance(other , ToolCall):
          if self.tool_name == other.tool_name and self.arguments == other.arguments:
              return True
        return False
            
            