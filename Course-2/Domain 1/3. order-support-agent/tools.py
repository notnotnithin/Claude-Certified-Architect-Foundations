"""
tools.py
---------
The TOOLS our agents can use. Same idea as before: each tool has a SCHEMA
(what the model reads to choose a tool) and a FUNCTION (the code that runs).

Tools are grouped by SPECIALIST ROLE (same as Demo 1.2):
  - ORDER tools    -> get_customer, get_order
  - POLICY tools   -> get_refund_policy, get_shipping_policy

Giving each subagent only the tools it needs keeps tool selection reliable.
"""

from mock_data import CUSTOMERS, ORDERS, REFUND_POLICY, SHIPPING_POLICY


# ==========================================================================
# TOOL SCHEMAS, grouped by specialist role
# ==========================================================================
ORDER_TOOL_SCHEMAS = [
    {
        "name": "get_customer",
        "description": (
            "Look up a customer's account record using their customer ID "
            "(format: 'CUST-XXXX'). Returns name, email, city, and loyalty "
            "tier. Use this to verify who the customer is. Do NOT use this to "
            "look up orders — use get_order for that."
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "customer_id": {
                    "type": "string",
                    "description": "The customer ID, e.g. 'CUST-1001'.",
                }
            },
            "required": ["customer_id"],
        },
    },
    {
        "name": "get_order",
        "description": (
            "Retrieve a single order using its order ID (format: 'ORD-XXXX'). "
            "Returns item, amount in INR, status ('Delivered' or 'In Transit'), "
            "and delivery date. Use this for any question about a specific "
            "order or its status. Do NOT use this for customer account info — "
            "use get_customer for that."
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "order_id": {
                    "type": "string",
                    "description": "The order ID, e.g. 'ORD-5001'.",
                }
            },
            "required": ["order_id"],
        },
    },
]

POLICY_TOOL_SCHEMAS = [
    {
        "name": "get_refund_policy",
        "description": (
            "Return the store's written REFUND policy as plain text. Use this "
            "whenever the customer asks whether something can be refunded, or "
            "before promising a refund. Takes no inputs."
        ),
        "input_schema": {"type": "object", "properties": {}},
    },
    {
        "name": "get_shipping_policy",
        "description": (
            "Return the store's written SHIPPING / delivery policy as plain "
            "text. Use this for questions about delivery times, cancellation, "
            "or reporting damage. Takes no inputs."
        ),
        "input_schema": {"type": "object", "properties": {}},
    },
]


# ==========================================================================
# TOOL IMPLEMENTATIONS  (the real code that runs)
# ==========================================================================
def get_customer(customer_id: str) -> dict:
    customer = CUSTOMERS.get(customer_id)
    if customer is None:
        return {"error": f"No customer found with ID '{customer_id}'."}
    return customer


def get_order(order_id: str) -> dict:
    order = ORDERS.get(order_id)
    if order is None:
        return {"error": f"No order found with ID '{order_id}'."}
    return order


def get_refund_policy() -> dict:
    return {"policy": REFUND_POLICY}


def get_shipping_policy() -> dict:
    return {"policy": SHIPPING_POLICY}


# One lookup table so the agent loop can find a function by tool name.
TOOL_FUNCTIONS = {
    "get_customer": get_customer,
    "get_order": get_order,
    "get_refund_policy": get_refund_policy,
    "get_shipping_policy": get_shipping_policy,
}


def run_tool(tool_name: str, tool_input: dict) -> dict:
    """Look up the function for `tool_name` and call it with `tool_input`."""
    func = TOOL_FUNCTIONS.get(tool_name)
    if func is None:
        return {"error": f"Unknown tool: {tool_name}"}
    return func(**tool_input)
