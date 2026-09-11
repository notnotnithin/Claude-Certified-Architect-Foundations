"""
subagent.py
------------
A SCOPED subagent for DocDesk's research pipeline (Task 2.3).

Each subagent is created with ONLY the tools for its role:
  - the Searcher gets search tools,
  - the Analyzer gets load tools,
  - the Synthesizer gets the scoped verify_fact tool.

This file also shows tool_choice configuration, which controls HOW the model
is allowed to use tools on a given call:

  - "auto"  : the model may call a tool OR just answer with text (default).
  - "any"   : the model MUST call one of the available tools (no plain text).
  - forced  : the model MUST call one SPECIFIC named tool, e.g.
              {"type": "tool", "name": "search_documents"}.
"""

import json
from dataclasses import dataclass
from typing import Callable
import anthropic
from dotenv import load_dotenv

load_dotenv()
client = anthropic.Anthropic()
MODEL = "claude-sonnet-4-6"
MAX_LOOPS = 8


@dataclass
class AgentDefinition:
    name: str
    system_prompt: str
    tool_schemas: list        # ONLY this role's tools
    run_tool: Callable        # scoped runner (from tools.make_runner)


class SubAgent:
    def __init__(self, definition: AgentDefinition):
        self.d = definition

    def run(self, task: str, tool_choice: dict | str = "auto") -> str:
        """
        Run the agent on one task.

        `tool_choice` controls the FIRST model call:
          - "auto"                          -> may use a tool or answer
          - "any"                           -> must use some tool
          - {"type":"tool","name":"..."}    -> must use that exact tool
        After the first call we switch to "auto" so the agent can finish with text.
        """
        messages = [{"role": "user", "content": task}]
        choice = _normalize_choice(tool_choice)

        for step in range(MAX_LOOPS):
            kwargs = dict(
                model=MODEL, max_tokens=800,
                system=self.d.system_prompt,
                tools=self.d.tool_schemas,
                messages=messages,
            )
            if choice is not None:
                kwargs["tool_choice"] = choice

            response = client.messages.create(**kwargs)
            messages.append({"role": "assistant", "content": response.content})

            # After the first (possibly forced) call, let the model finish freely.
            choice = None

            if response.stop_reason == "end_turn":
                return _text(response)

            if response.stop_reason == "tool_use":
                results = []
                for block in response.content:
                    if block.type == "tool_use":
                        print(f"      [{self.d.name}] uses {block.name}({block.input})")
                        result = self.d.run_tool(block.name, block.input)
                        results.append({
                            "type": "tool_result",
                            "tool_use_id": block.id,
                            "content": json.dumps(result),
                        })
                if not results:
                    return _text(response) or "[no result]"
                messages.append({"role": "user", "content": results})
                continue

            return f"[stopped: {response.stop_reason}]"

        return "[stopped: loop limit]"


def _normalize_choice(tool_choice):
    if tool_choice in (None, "auto"):
        return {"type": "auto"}
    if tool_choice == "any":
        return {"type": "any"}
    if isinstance(tool_choice, dict):
        return tool_choice           # e.g. {"type":"tool","name":"..."}
    return {"type": "auto"}


def _text(response) -> str:
    return "\n".join(b.text for b in response.content if b.type == "text").strip()
