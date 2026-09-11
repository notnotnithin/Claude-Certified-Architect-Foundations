"""
subagent.py
------------
Demo 1.3 upgrades the subagent in two exam-important ways (Task 1.3):

1. AGENT DEFINITION
   A subagent is now described by an AgentDefinition: a name, a description
   (what it is for), a system prompt, and its allowed tools. This mirrors the
   Agent SDK's AgentDefinition idea — a clear, reusable spec for each agent.

2. STRUCTURED FINDINGS (content + metadata)
   Instead of returning one blob of text, a subagent now returns a STRUCTURED
   result that separates the content from its metadata:

       {
         "agent": "Order Specialist",
         "summary": "...the human-readable finding...",
         "sources": [ {"type": "order", "id": "ORD-5001"}, ... ]
       }

   Keeping the sources/IDs separate preserves ATTRIBUTION as findings pass
   between agents — the coordinator can later tell exactly where each fact came
   from. This is the heart of "separate content from metadata" in Task 1.3.

The agentic loop inside run() is the SAME loop from Demo 1.1 — drive on
stop_reason. Context is still ISOLATED: each run starts a fresh conversation,
so anything the subagent should know must be passed inside the task text.
"""

import json
from dataclasses import dataclass, field
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
    description: str                 # what this agent is for
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

        `task` is everything this subagent needs to know, written by the
        coordinator. The subagent starts with a BLANK conversation (isolated
        context) — it only knows what is inside `task`.
        """
        messages = [{"role": "user", "content": task}]
        sources = []   # we record which tools/IDs were touched (= metadata)

        for _ in range(MAX_LOOPS):
            response = client.messages.create(
                model=MODEL,
                max_tokens=1000,
                system=self.d.system_prompt,
                tools=self.d.tool_schemas,
                messages=messages,
            )
            messages.append({"role": "assistant", "content": response.content})

            # SAME RULE AS DEMO 1.1: branch only on stop_reason.
            if response.stop_reason == "end_turn":
                summary = self._extract_text(response)
                return {
                    "agent": self.d.name,
                    "summary": summary,
                    "sources": sources,
                }

            if response.stop_reason == "tool_use":
                tool_results = []
                for block in response.content:
                    if block.type == "tool_use":
                        print(f"      [{self.d.name}] calls {block.name}({block.input})")
                        result = self.d.run_tool_fn(block.name, block.input)

                        # Record metadata: what was looked up, and any ID used.
                        sources.append({
                            "tool": block.name,
                            "input": block.input,
                        })

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
