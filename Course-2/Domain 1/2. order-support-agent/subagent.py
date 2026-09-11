"""
subagent.py
------------
A SUBAGENT is just the single agent from Demo 1.1, turned into something we
can reuse. It still runs the exact same agentic loop (drive on stop_reason),
but now it has:

  - a NAME (e.g. "Order Specialist")
  - its OWN system prompt (what it specialises in)
  - its OWN small set of tools (only what its role needs)

KEY EXAM IDEA (Task 1.2): ISOLATED CONTEXT.
-------------------------------------------
Each time we call a subagent we start a FRESH conversation. A subagent does
NOT automatically see the coordinator's conversation or other subagents'
work. Whatever it needs to know must be passed IN through its task text.
That is why run() below starts `messages` from scratch every call.

This is the same loop you already learned — only the wrapping is new.
"""

import json
import anthropic
from dotenv import load_dotenv

load_dotenv()

client = anthropic.Anthropic()

MODEL = "claude-sonnet-4-6"
MAX_LOOPS = 10  # safety net only; the real stop signal is stop_reason


class SubAgent:
    """A small, focused agent with its own role and tools."""

    def __init__(self, name: str, system_prompt: str, tool_schemas: list,
                 run_tool_fn):
        self.name = name
        self.system_prompt = system_prompt
        self.tool_schemas = tool_schemas
        self.run_tool_fn = run_tool_fn          # function that executes a tool

    def run(self, task: str) -> str:
        """
        Run the agentic loop for ONE task and return the final text.

        `task` is everything this subagent needs to know, written by the
        coordinator. The subagent starts with a BLANK conversation (isolated
        context) — it only knows what is inside `task`.
        """
        # Fresh conversation every time = isolated context.
        messages = [{"role": "user", "content": task}]

        for _ in range(MAX_LOOPS):
            response = client.messages.create(
                model=MODEL,
                max_tokens=1000,
                system=self.system_prompt,
                tools=self.tool_schemas,
                messages=messages,
            )
            messages.append({"role": "assistant", "content": response.content})

            # SAME RULE AS DEMO 1.1: branch only on stop_reason.
            if response.stop_reason == "end_turn":
                return self._extract_text(response)

            if response.stop_reason == "tool_use":
                tool_results = []
                for block in response.content:
                    if block.type == "tool_use":
                        print(f"      [{self.name}] calls {block.name}({block.input})")
                        result = self.run_tool_fn(block.name, block.input)
                        tool_results.append({
                            "type": "tool_result",
                            "tool_use_id": block.id,
                            "content": json.dumps(result),
                        })
                messages.append({"role": "user", "content": tool_results})
                continue

            return f"[{self.name} stopped: unexpected stop_reason " \
                   f"'{response.stop_reason}'.]"

        return f"[{self.name} stopped: reached the safety loop limit.]"

    @staticmethod
    def _extract_text(response) -> str:
        parts = [b.text for b in response.content if b.type == "text"]
        return "\n".join(parts).strip()
