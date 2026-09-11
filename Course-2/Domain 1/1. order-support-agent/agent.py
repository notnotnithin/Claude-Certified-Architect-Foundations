"""
agent.py
---------
This is the HEART of Demo 1.1: a single AI agent with a correct AGENTIC LOOP.

WHAT IS AN AGENTIC LOOP?  (Exam Task Statement 1.1)
---------------------------------------------------
An agent does not answer in one shot. It works in a loop:

    1. Send the conversation to Claude.
    2. Claude responds. We inspect the response's `stop_reason`:
         - "tool_use"  -> Claude wants to call a tool. We run the tool,
                          add the result to the conversation, and LOOP AGAIN.
         - "end_turn"  -> Claude is done. We show its final answer and STOP.
    3. Repeat until stop_reason is "end_turn".

THE GOLDEN RULE: drive the loop off `stop_reason`. Nothing else.

COMMON ANTI-PATTERNS THIS DEMO AVOIDS (the exam loves testing these):
  - Reading the assistant's TEXT to guess if it is "done".  ❌
  - Searching for phrases like "I have finished" to stop.    ❌
  - Using an arbitrary iteration cap as the MAIN stop signal. ❌
    (We keep a SAFETY cap to avoid runaway loops, but the REAL
     stopping condition is always stop_reason == "end_turn".)

HOW TO USE
----------
Run:  python agent.py
Then type a question and press Enter. The agent answers, then asks for the
next question. Type 'quit' (or 'exit') to stop.
"""

import os
import json
from dotenv import load_dotenv      # reads the .env file
import anthropic

from tools import TOOL_SCHEMAS, run_tool

# --------------------------------------------------------------------------
# Load the .env file. This reads ANTHROPIC_API_KEY from the .env file in this
# folder and puts it into the environment, so the Anthropic client can find it.
# load_dotenv() must run BEFORE we create the client below.
# --------------------------------------------------------------------------
load_dotenv()

# The client automatically reads ANTHROPIC_API_KEY from the environment.
client = anthropic.Anthropic()

MODEL = "claude-sonnet-4-6"

# The SYSTEM PROMPT defines the agent's role and behavior.
SYSTEM_PROMPT = (
    "You are a helpful customer support assistant for an online store called "
    "PyStack Mart. You can look up customers, look up orders, and read the "
    "refund policy using the tools provided.\n\n"
    "Guidelines:\n"
    "- Be friendly, clear, and concise.\n"
    "- Use the tools to find real information instead of guessing.\n"
    "- When a customer asks about a refund, check the refund policy and the "
    "order's status before answering.\n"
    "- All money amounts are in Indian Rupees (INR, shown as Rs.)."
)

# A SAFETY limit. This is NOT our real stopping condition — stop_reason is.
# It only protects us from an unexpected infinite loop.
MAX_LOOPS = 10


def run_agent(user_message: str) -> str:
    """
    Run the full agentic loop for a single user message and return the
    agent's final text answer.
    """
    # The conversation history. We append to this as the loop runs.
    messages = [
        {"role": "user", "content": user_message}
    ]

    for loop_number in range(1, MAX_LOOPS + 1):
        print(f"\n--- Loop iteration {loop_number} ---")

        # STEP 1: Send the conversation to Claude.
        response = client.messages.create(
            model=MODEL,
            max_tokens=1000,
            system=SYSTEM_PROMPT,
            tools=TOOL_SCHEMAS,
            messages=messages,
        )

        # Show what stop_reason we got — this is what drives the loop.
        print(f"stop_reason = {response.stop_reason!r}")

        # STEP 2: Add Claude's response to the conversation history.
        # (We must always append the assistant turn before adding tool results.)
        messages.append({"role": "assistant", "content": response.content})

        # STEP 3: Branch on stop_reason.
        if response.stop_reason == "end_turn":
            # Claude is finished. Pull out the text and return it.
            final_text = _extract_text(response)
            print("Claude is done (end_turn). Returning final answer.")
            return final_text

        if response.stop_reason == "tool_use":
            # Claude wants to call one or more tools.
            # We build a "tool_result" for each tool call and send them back.
            tool_results = []

            for block in response.content:
                if block.type == "tool_use":
                    print(f"  -> Claude wants to call: {block.name}({block.input})")

                    # Run the actual tool function.
                    result = run_tool(block.name, block.input)
                    print(f"     Tool returned: {result}")

                    # Package the result so Claude can read it next loop.
                    tool_results.append({
                        "type": "tool_result",
                        "tool_use_id": block.id,
                        "content": json.dumps(result),
                    })

            # Add all tool results as a single 'user' turn, then LOOP AGAIN.
            messages.append({"role": "user", "content": tool_results})
            continue

        # If we ever see an unexpected stop_reason, fail loudly instead of
        # guessing. (e.g. "max_tokens" means the answer was cut off.)
        return (
            f"[Stopped: unexpected stop_reason '{response.stop_reason}'. "
            "The response may be incomplete.]"
        )

    # If we exit the for-loop, we hit the SAFETY cap. This should be rare.
    return "[Stopped: reached the safety loop limit without finishing.]"


def _extract_text(response) -> str:
    """Collect all text blocks from a response into one string."""
    parts = [block.text for block in response.content if block.type == "text"]
    return "\n".join(parts).strip()


# --------------------------------------------------------------------------
# Interactive mode: type one prompt at a time.
# --------------------------------------------------------------------------
if __name__ == "__main__":
    # Make sure the API key was loaded from the .env file before we continue.
    if not os.environ.get("ANTHROPIC_API_KEY"):
        print("ERROR: ANTHROPIC_API_KEY not found.")
        print("Create a .env file in this folder with this line:")
        print('  ANTHROPIC_API_KEY=your-key-here')
        raise SystemExit(1)

    print("=" * 70)
    print("PyStack Mart — Order Support Assistant (Demo 1.1)")
    print("Type your question and press Enter. Type 'quit' or 'exit' to stop.")
    print("=" * 70)
    print("Try things like:")
    print("  - Can you tell me the status of my order ORD-5003?")
    print("  - I am customer CUST-1001. Can I get a refund for ORD-5001?")

    # Keep asking for prompts until the user types quit/exit.
    while True:
        # input() pauses and waits for you to type a prompt and press Enter.
        user_message = input("\nYour question > ").strip()

        # Allow the user to leave.
        if user_message.lower() in ("quit", "exit", "q"):
            print("Goodbye!")
            break

        # Ignore empty input (just pressing Enter).
        if not user_message:
            continue

        # Run the agentic loop for this one prompt and show the answer.
        answer = run_agent(user_message)
        print("\nFINAL ANSWER:\n" + answer)
