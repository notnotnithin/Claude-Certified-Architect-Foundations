"""
tools.py
---------
This file defines the TOOLS our single agent can use.

For each tool there are TWO things:
  1. A SCHEMA  -> tells Claude the tool's name, what it does, and what
                  inputs it expects. This is what the model "reads" when
                  deciding which tool to call.
  2. A FUNCTION -> the actual Python code that runs when the tool is called.

KEY EXAM IDEA (Task 2.1): Tool descriptions are the PRIMARY way the model
decides which tool to use. Notice how detailed each "description" below is —
we explain the purpose, the inputs, AND when to use it versus another tool.
Minimal descriptions like "gets an order" lead to unreliable tool selection.
"""

from mock_data import CUSTOMERS, ORDERS, REFUND_POLICY

# ==========================================================================
# 1. TOOL SCHEMAS  (what Claude sees)
# ==========================================================================
TOOL_SCHEMAS = [
    {
        "name": "get_customer",
        "description": (
            "Look up a customer's account record using their customer ID "
            "(format: 'CUST-XXXX'). Returns the customer's name, email, city, "
            "and loyalty tier. Use this FIRST to verify who you are talking to "
            "before discussing any orders or refunds. Do NOT use this to look "
            "up orders — use get_order for that."
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
            "Retrieve the details of a single order using its order ID "
            "(format: 'ORD-XXXX'). Returns the item name, amount in INR, "
            "current status (e.g. 'Delivered' or 'In Transit'), and delivery "
            "date. Use this when the customer asks about a specific order, its "
            "status, or wants a refund. Do NOT use this to look up customer "
            "account info — use get_customer for that."
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
    {
        "name": "get_refund_policy",
        "description": (
            "Return the store's written refund policy as plain text. Use this "
            "whenever the customer asks whether something can be refunded, or "
            "when you need to check the rules before promising a refund. Takes "
            "no inputs."
        ),
        "input_schema": {
            "type": "object",
            "properties": {},
        },
    },
]


# ==========================================================================
# 2. TOOL IMPLEMENTATIONS  (the real code that runs)
# ==========================================================================
def get_customer(customer_id: str) -> dict:
    """Return the customer record, or an error message if not found."""
    customer = CUSTOMERS.get(customer_id)
    if customer is None:
        return {"error": f"No customer found with ID '{customer_id}'."}
    return customer


def get_order(order_id: str) -> dict:
    """Return the order record, or an error message if not found."""
    order = ORDERS.get(order_id)
    if order is None:
        return {"error": f"No order found with ID '{order_id}'."}
    return order


def get_refund_policy() -> dict:
    """Return the refund policy text."""
    return {"policy": REFUND_POLICY}


# A simple lookup table so the agent loop can find the right function
# by the tool name the model gives us.
TOOL_FUNCTIONS = {
    "get_customer": get_customer,
    "get_order": get_order,
    "get_refund_policy": get_refund_policy,
}


def run_tool(tool_name: str, tool_input: dict) -> dict:
    """
    Look up the function for `tool_name` and call it with `tool_input`.
    Returns whatever the tool function returns (always a dict here).
    """
    func = TOOL_FUNCTIONS.get(tool_name)
    if func is None:
        return {"error": f"Unknown tool: {tool_name}"}
    # ** unpacks the dict into keyword arguments, e.g.
    # run_tool("get_order", {"order_id": "ORD-5001"})
    #   -> get_order(order_id="ORD-5001")
    return func(**tool_input)
