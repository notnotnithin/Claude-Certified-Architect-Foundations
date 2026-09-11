"""
tools.py
---------
The TOOLS our agent can use. Same idea as before: each tool has a SCHEMA
(what the model reads) and a FUNCTION (the code that runs).

Demo 7 keeps the tools simple — the new ideas are about SESSIONS (saving,
resuming, forking), not about new tools.
"""

from mock_data import ORDERS, REFUND_POLICY


TOOL_SCHEMAS = [
    {
        "name": "get_order",
        "description": (
            "Retrieve full details of one order by its order ID ('ORD-XXXX'): "
            "item, amount in INR, status, and delivery date."
        ),
        "input_schema": {
            "type": "object",
            "properties": {"order_id": {"type": "string"}},
            "required": ["order_id"],
        },
    },
    {
        "name": "get_refund_policy",
        "description": "Return the store's written REFUND policy. No inputs.",
        "input_schema": {"type": "object", "properties": {}},
    },
]


def get_order(order_id: str) -> dict:
    o = ORDERS.get(order_id)
    return o if o else {"error": f"No order '{order_id}'."}


def get_refund_policy() -> dict:
    return {"policy": REFUND_POLICY}


TOOL_FUNCTIONS = {
    "get_order": get_order,
    "get_refund_policy": get_refund_policy,
}


def run_tool(tool_name: str, tool_input: dict) -> dict:
    func = TOOL_FUNCTIONS.get(tool_name)
    if func is None:
        return {"error": f"Unknown tool: {tool_name}"}
    return func(**tool_input)
