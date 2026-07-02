# micro-agent

A minimal agent-orchestration framework built **from scratch in pure Python** - no LangChain, no LangGraph, no Mastra, no external dependencies.

## Why this exists

I use frameworks like LangGraph and Mastra in my other projects (see [MedTrace](#), [Multi-Agent Finance AI System](#)), but I wanted to actually understand what they're doing under the hood instead of just calling their APIs. So I'm rebuilding the core loop of an agent framework - message handling, tool registration, action routing, and output parsing - using nothing but the Python standard library.

This is also a deliberate exercise in writing and defending code independently: every module below was built with a mentored, spec-first approach - I was given a specification and test cases, wrote the implementation myself, and debugged real bugs before moving forward.

## Architecture

```text
micro_agent/
├── message.py          # Message & ToolCall classes - structured conversation turns
├── registry.py         # @register_tool decorator - first-class functions as a tool catalog
├── router.py           # match/case based routing of agent decisions
├── parser.py           # Regex-based extraction of tool calls from raw LLM text
├── memory.py           # (planned) closure-based conversation memory
├── dedupe.py           # (planned) set-based tool-call deduplication
├── persistence.py      # (planned) JSON file save/load for conversation history
└── cli.py              # (planned) entrypoint
```

## Progress

### Module 1 - `Message` and `ToolCall` classes (`message.py`)

Models a conversation turn (`Message`) and a tool invocation request (`ToolCall`) as real objects instead of loose dicts.

- `Message(role, content)` auto-generates a fresh `timestamp` on creation.
- `ToolCall(tool_name, arguments)` auto-generates a unique `call_id` (UUID4) per instance.
- Implements `__str__`, `__repr__`, and a type-safe `__eq__`.
- Two `ToolCall`s are equal if `tool_name` and `arguments` match. `call_id` is intentionally excluded from equality.

**Bugs caught and fixed during development:**

- Mutable/stale default argument trap: `timestamp=datetime.datetime.now()` in a function signature evaluates once, at function definition time, not per call. Fixed by using `timestamp=None` and computing the real value inside the function body.
- Unsafe `__eq__`: comparing `other.tool_name` before checking `isinstance(other, ToolCall)` crashes on `AttributeError` if compared against a non-`ToolCall`. Fixed by guarding with `isinstance` first.

### Module 2 - Tool Registry (`registry.py`)

A `@register_tool` decorator that catalogs any function into a shared `TOOLS` dict, keyed by function name, so agent code can look up and call tools dynamically by name rather than hardcoding references.

Also explored decorator behavior more broadly:

- A registry-style decorator returns the original function unchanged and records it as a side effect.
- A wrapping-style decorator (`log_call`) builds a new function around the original to add behavior, generalized with `*args, **kwargs` to work on any function signature.

### Module 3 - Action Router (`router.py`)

`route_action(action)` uses Python 3.10+ `match`/`case` to route a parsed agent decision (`tool_call`, `final_answer`, `error`, or unrecognized) to the correct handling string, with a `case _:` wildcard to guarantee unrecognized action types are surfaced explicitly rather than silently returning `None`.

### Module 4 - Output Parser (`parser.py`) - in progress

`parse_tool_call(text)` uses regex with capture groups to extract a structured tool call from raw LLM text formatted as `TOOL_CALL: tool_name(arg="value")`, returning `None` if no tool call is present. Currently supports single-argument tool calls; multi-argument parsing is a planned extension.

## Planned modules

- Closure-based memory: conversation memory built as a closure (`add_message`/`get_history` functions) instead of a class.
- Set-based deduplication: skip redundant tool calls with identical `tool_name` + `arguments` within a loop.
- JSON persistence: save/resume conversation history via `json.dump`/`json.load`.
- CLI entrypoint: tie everything together with `argparse`.
- Real LLM integration: wire in a live model call so the loop is end-to-end.

## Method

Every module here was built spec-first: given a requirement and expected input/output, write the implementation independently, run it, and debug real failures before moving to the next piece. This is intentional: the goal is not just a working demo, it is closing the gap between using AI tools to build projects and being able to write and defend production code independently.
