"""
errors.py
----------
THE HEART OF DEMO 2: a STRUCTURED ERROR format (Task 2.2).

In MCP, a tool signals failure with an `isError` flag and can return structured
metadata so the AGENT can decide what to do. A flat string like
"Operation failed" tells the agent nothing — it can't tell a temporary blip
from a permanent block, so it either gives up or retries pointlessly.

We model the MCP pattern with a small helper that every tool uses:

    {
      "isError": true,
      "errorCategory": "transient" | "validation" | "business" | "permission",
      "isRetryable": true | false,
      "message": "human-readable explanation"
    }

WHAT EACH CATEGORY MEANS (and what the agent should do):
  - transient   : a temporary blip (timeout, service busy).      -> RETRY
  - validation  : bad input (e.g. no such document name).        -> FIX INPUT, don't blind-retry
  - business    : a policy/rule blocks it (not an outage).       -> EXPLAIN, don't retry
  - permission  : not allowed to access this.                    -> STOP/ escalate, don't retry

IMPORTANT DISTINCTION (Task 2.2):
An empty result is NOT an error. "I searched and found nothing" is a SUCCESSFUL
query with zero matches — it must NOT be reported as isError. Only a real
FAILURE to access data is an error.
"""


def make_error(category: str, message: str, retryable: bool) -> dict:
    """Build one structured error result (the MCP isError pattern)."""
    return {
        "isError": True,
        "errorCategory": category,   # transient | validation | business | permission
        "isRetryable": retryable,
        "message": message,
    }


# Convenience builders so tools stay short and consistent.
def transient_error(message: str) -> dict:
    # Temporary problem -> worth retrying.
    return make_error("transient", message, retryable=True)


def validation_error(message: str) -> dict:
    # Bad input -> retrying the SAME call won't help; the input must change.
    return make_error("validation", message, retryable=False)


def business_error(message: str) -> dict:
    # A rule/policy blocks the action -> explain it; do NOT retry.
    return make_error("business", message, retryable=False)


def permission_error(message: str) -> dict:
    # Not allowed -> do NOT retry; needs different access or escalation.
    return make_error("permission", message, retryable=False)


def ok(**fields) -> dict:
    """A successful (non-error) result. Note: isError is False."""
    return {"isError": False, **fields}
