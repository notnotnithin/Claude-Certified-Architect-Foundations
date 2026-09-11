"""
hooks.py
---------
THE HEART OF DEMO 5: HOOKS that give DETERMINISTIC guarantees.

A HOOK is a small function that runs automatically around a tool call. We use
two kinds (Task 1.5):

  1. PRE-TOOL hook  (runs BEFORE a tool executes)
     - can BLOCK a tool call that breaks a rule, and redirect instead.
     - we use it for:
         * a PREREQUISITE GATE: block process_refund until identity is verified.
         * a THRESHOLD BLOCK: block automatic refunds above Rs. 500 -> escalate.

  2. POST-TOOL hook (runs AFTER a tool returns, BEFORE the model sees it)
     - can TRANSFORM / normalize the result.
     - we use it to turn legacy formats (unix timestamps, numeric status codes)
       into ONE consistent shape, so the agent always sees clean data.

WHY HOOKS INSTEAD OF JUST PROMPTING?
------------------------------------
You could WRITE in the prompt "always verify identity first" or "never refund
over Rs. 500 automatically." But a prompt is PROBABILISTIC — the model follows
it most of the time, not every time. When a rule MUST hold (money, identity),
a hook makes it DETERMINISTIC: the code blocks the action no matter what the
model decides. That guarantee is the whole point of Task 1.5.
"""

from datetime import datetime, timezone
from mock_data import STATUS_CODE_TO_TEXT

# Business rule: automatic refunds are only allowed up to this amount.
REFUND_AUTO_LIMIT_INR = 500


# ==========================================================================
# PRE-TOOL HOOK — runs before a tool executes. May BLOCK the call.
# ==========================================================================
def pre_tool_hook(tool_name: str, tool_input: dict, state: dict) -> dict | None:
    """
    Inspect a tool call BEFORE it runs.

    Returns:
      - None                -> allow the tool call to proceed.
      - a dict (tool result) -> BLOCK the real tool and use this result instead.

    `state` is a small dict the loop keeps across the conversation, e.g.
    state["verified"] = True once identity has been confirmed.
    """
    # --- track identity verification so later calls can depend on it ---
    if tool_name == "verify_identity":
        # We don't block it; we let it run. (The loop records the result.)
        return None

    # --- PREREQUISITE GATE: no refund before identity is verified ---
    if tool_name == "process_refund" and not state.get("verified"):
        print("      [HOOK] BLOCKED process_refund: identity not verified yet.")
        return {
            "blocked": True,
            "reason": "Identity must be verified before any refund. "
                      "Call verify_identity first.",
        }

    # --- THRESHOLD BLOCK: no automatic refund above the limit ---
    if tool_name == "process_refund":
        amount = tool_input.get("amount_inr", 0)
        if amount > REFUND_AUTO_LIMIT_INR:
            print(f"      [HOOK] BLOCKED process_refund: Rs. {amount} is above "
                  f"the Rs. {REFUND_AUTO_LIMIT_INR} auto-limit. Must escalate.")
            return {
                "blocked": True,
                "reason": f"Refund of Rs. {amount} exceeds the automatic limit "
                          f"of Rs. {REFUND_AUTO_LIMIT_INR}. Escalate to a human "
                          f"instead using escalate_to_human.",
            }

    # Otherwise: allow the tool to run.
    return None


# ==========================================================================
# POST-TOOL HOOK — runs after a tool returns. May TRANSFORM the result.
# ==========================================================================
def post_tool_hook(tool_name: str, result: dict) -> dict:
    """
    Normalize heterogeneous data so the agent always sees ONE clean shape.

    Specifically, for get_order results that came from the legacy system:
      - status_code (number)      -> status (text)
      - delivered_unix_ts (int)   -> delivered_on (ISO date string)
    """
    if tool_name != "get_order" or not isinstance(result, dict):
        return result
    if "error" in result:
        return result

    normalized = dict(result)  # copy so we don't mutate the stored record

    # numeric status code -> text status
    if "status_code" in normalized and "status" not in normalized:
        code = normalized.pop("status_code")
        normalized["status"] = STATUS_CODE_TO_TEXT.get(code, f"Unknown({code})")
        print(f"      [HOOK] normalized status_code {code} -> "
              f"'{normalized['status']}'")

    # unix timestamp -> ISO date string
    if "delivered_unix_ts" in normalized and "delivered_on" not in normalized:
        ts = normalized.pop("delivered_unix_ts")
        iso = datetime.fromtimestamp(ts, tz=timezone.utc).strftime("%Y-%m-%d")
        normalized["delivered_on"] = iso
        print(f"      [HOOK] normalized unix_ts {ts} -> '{iso}'")

    return normalized
