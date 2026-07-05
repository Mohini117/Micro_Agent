# micro-agent

A minimal agent-orchestration framework built from scratch in pure Python.

This project rebuilds the core ideas behind agent frameworks such as LangGraph, LangChain, and Mastra without depending on them: structured messages, tool-call parsing, registered tool dispatch, memory, deduplication, and JSON persistence.

The goal is not to wrap an existing framework. The goal is to understand and implement the moving pieces of an agent loop directly.

## What It Demonstrates

- Object modeling for conversation turns and tool calls
- Decorator-based tool registration
- Structured parsing of `TOOL_CALL:` model-style output
- `match` / `case` routing that dispatches registered tools
- Closure-based in-memory conversation history
- Set-based duplicate tool-call detection
- JSON save/load for conversation persistence
- A working command-line loop with conversation saving

## Demo

Run the CLI from the project root:

```powershell
python -m text.cli
```

Example session:

```text
PS D:\micro_agent> python -m text.cli
> What does this medicine do?
Final answer: What does this medicine do?
> TOOL_CALL: search_medicine_db(query="paracetamol")
Tool result: Results for paracetamol
> TOOL_CALL: get_weather(city="New York")
Tool result: Weather in New York (celsius)
> TOOL_CALL: search_medicine_db(query="paracetamol")
Duplicate tool call skipped: search_medicine_db
> exit
Saving conversation... done.
```

At the current stage, the CLI can identify a tool-call instruction, parse keyword arguments, dispatch a registered local tool, skip duplicate tool calls within a session, and save conversation history. Live LLM integration is planned next.

## Architecture

```text
micro_agent/
|-- message.py                 # Message and ToolCall domain objects
|-- registry.py                # @register_tool decorator and tool catalog
|-- decorators_lite/
|   |-- parser.py              # Parses TOOL_CALL text into structured data
|   `-- router.py              # Routes actions and dispatches registered tools
|-- text/
|   |-- cli.py                 # Interactive CLI loop
|   |-- memory.py              # Closure-based conversation memory
|   |-- dedupe.py              # Duplicate tool-call detection
|   `-- persistence.py         # JSON save/load for conversation history
|-- conversation.json          # Saved CLI conversation history
`-- main.py                    # Local smoke-test script
```

## Core Modules

### 1. Messages and Tool Calls

`message.py` defines two core objects:

- `Message(role, content, timestamp=None)` stores one conversation turn and creates a fresh timestamp per message.
- `ToolCall(tool_name, arguments, call_id=None)` stores a tool request and creates a unique UUID call id.

Important implementation detail: `ToolCall.__eq__` and `ToolCall.__hash__` compare `tool_name` and `arguments`, but intentionally ignore `call_id`. That allows the deduplication layer to detect repeated calls even when each call has a unique id.

### 2. Tool Registry

`registry.py` implements a small `@register_tool` decorator. Registered functions are stored in the shared `TOOLS` dictionary by function name, which is the same basic pattern larger agent systems use when they expose tools to a model.

Example tools currently included:

- `search_medicine_db(query)`
- `get_weather(city)`

### 3. Output Parser

`decorators_lite/parser.py` extracts a structured tool call from text like:

```text
TOOL_CALL: search_medicine_db(query="paracetamol")
```

It also supports quoted values with spaces and multiple keyword arguments:

```text
TOOL_CALL: get_weather(city="New York")
TOOL_CALL: get_weather(city="Nagpur", unit="celsius")
```

It returns:

```python
{
    "tool_name": "search_medicine_db",
    "arguments": {"query": "paracetamol"}
}
```

If the text is not a tool call, it returns `None`, allowing the CLI to treat the input as a final answer.

### 4. Action Router

`decorators_lite/router.py` uses Python `match` / `case` to route actions:

- `tool_call` -> execute a registered tool from `registry.TOOLS`
- `final_answer` -> return final response text
- `error` -> surface parser or runtime errors
- unknown action -> return an explicit fallback message

### 5. Memory

`text/memory.py` implements memory with a closure instead of a class:

- `add_message(message)` appends to the hidden history list
- `get_history()` returns the stored messages

This demonstrates Python's enclosing-scope behavior and keeps state private without global variables.

### 6. Deduplication

`text/dedupe.py` converts a `ToolCall` into a hashable key:

```python
(tool_name, make_hashable(arguments))
```

That makes it possible to store previous calls in a `set` and skip repeated calls with the same tool name and arguments. The CLI now uses this during each interactive session.

### 7. Persistence

`text/persistence.py` saves and loads conversation history as JSON. Because `datetime` objects are not directly JSON-serializable, each `Message` is converted to a plain dictionary on save and reconstructed on load.

### 8. CLI

`text/cli.py` ties the modules together:

1. Reads user input.
2. Stores each user message in memory.
3. Parses tool-call syntax if present.
4. Skips repeated tool calls in the same session.
5. Routes the action and executes registered tools.
6. Saves the conversation to `conversation.json` on `exit`.

## Requirements

- Python 3.10 or newer
- No external Python packages required

## Run Locally

```powershell
git clone https://github.com/Mohini117/Micro_Agent.git
cd Micro_Agent
python -m text.cli
```

Useful module checks:

```powershell
python main.py
python registry.py
python decorators_lite\parser.py
python decorators_lite\router.py
python -m text.memory
python -m text.persistence
python -m text.dedupe
```

## Development Notes

This project was built module by module with a spec-first approach: implement the smallest piece, run it, debug the real failure, then connect it to the next layer.

Notable bugs fixed during development:

- Avoided stale timestamps by using `timestamp=None` instead of `datetime.now()` as a default argument.
- Made `ToolCall.__eq__` type-safe before accessing attributes on `other`.
- Corrected parser output so it returns stable keys: `tool_name` and `arguments`.
- Replaced the one-word argument regex with structured keyword-argument parsing.
- Connected router tool calls to the registered `TOOLS` catalog.
- Connected duplicate tool-call detection to the CLI session.
- Added `ToolCall.__hash__` so equality and hash behavior stay consistent.
- Moved demo-only code behind `if __name__ == "__main__"` guards so imports stay clean.
- Removed duplicate JSON writes from persistence.
- Removed unrelated tutorial/demo material from the tracked project.

## Next Steps

- Add an LLM call so the CLI can receive model-generated `TOOL_CALL:` output.
- Add tests for parser, router, memory, dedupe, and persistence.
- Add CLI flags such as `--load conversation.json` to resume a previous session.

## Why This Project Matters

This repository shows the internals behind a simple agent system rather than hiding them inside a framework. It is small enough to read end to end, but it covers the concepts that matter in larger AI applications: structured state, tool selection, parsing, routing, memory, persistence, and clean module boundaries.
