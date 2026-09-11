"""
subagent.py
------------
A SUBAGENT is the single agent from Demo 1.1, turned into a reusable
specialist. It runs the same agentic loop (drive on stop_reason) and:

  - is built from an AgentDefinition (name, description, system prompt, tools)
  - returns STRUCTURED findings: {"agent", "summary", "sources"}

ISOLATED CONTEXT: each run() starts a fresh conversation. A subagent does NOT
see the coordinator's history or other subagents' work — anything it needs
must be passed inside the task text.

This file is unchanged from Demo 1.3; multi-concern handling is built on top
of it in coordinator.py.
"""

import json
from dataclasses import dataclass
from typing import Callable
import anthropic
from dotenv import load_dotenv

# Load the key here too, so this file works no matter who imports it first.
load_dotenv()

client = anthropic.Anthropic()
MODEL = "claude-sonnet-4-6"
MAX_LOOPS = 10  # safety net only; the real stop signal is stop_reason


@dataclass
class AgentDefinition:
    """A reusable spec for one subagent (like the SDK's AgentDefinition)."""
    name: str
    description: str
    system_prompt: str
    tool_schemas: list
    run_tool_fn: Callable


class SubAgent:
    """A small, focused agent built from an AgentDefinition."""

    def __init__(self, definition: AgentDefinition):
        self.d = definition

    def run(self, task: str) -> dict:
        """
        Run the agentic loop for ONE task and return a STRUCTURED finding:
            {"agent", "summary", "sources"}
        """
        messages = [{"role": "user", "content": task}]
        sources = []   # metadata: which tools/IDs were touched

        for _ in range(MAX_LOOPS):
            response = client.messages.create(
                model=MODEL,
                max_tokens=1000,
                system=self.d.system_prompt,
                tools=self.d.tool_schemas,
                messages=messages,
            )
            messages.append({"role": "assistant", "content": response.content})

            if response.stop_reason == "end_turn":
                return {
                    "agent": self.d.name,
                    "summary": self._extract_text(response),
                    "sources": sources,
                }

            if response.stop_reason == "tool_use":
                tool_results = []
                for block in response.content:
                    if block.type == "tool_use":
                        print(f"      [{self.d.name}] calls {block.name}({block.input})")
                        result = self.d.run_tool_fn(block.name, block.input)
                        sources.append({"tool": block.name, "input": block.input})
                        tool_results.append({
                            "type": "tool_result",
                            "tool_use_id": block.id,
                            "content": json.dumps(result),
                        })
                messages.append({"role": "user", "content": tool_results})
                continue

            return {
                "agent": self.d.name,
                "summary": f"[stopped: unexpected stop_reason "
                           f"'{response.stop_reason}']",
                "sources": sources,
            }

        return {
            "agent": self.d.name,
            "summary": "[stopped: reached the safety loop limit]",
            "sources": sources,
        }

    @staticmethod
    def _extract_text(response) -> str:
        parts = [b.text for b in response.content if b.type == "text"]
        return "\n".join(parts).strip()
