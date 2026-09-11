"""
tools.py
---------
The TOOLS our agent can use. Same idea as before: each tool has a SCHEMA
(what the model reads) and a FUNCTION (the code that runs).

NEW IN DEMO 6 — a "map the situation" tool:
  - list_customer_orders : returns all of a customer's order IDs + a brief
                           status for each.
This is what makes ADAPTIVE planning possible: the agent calls this FIRST to
see what exists, THEN decides what to investigate next based on what it finds.
"""

from mock_data import CUSTOMERS, ORDERS, REFUND_POLICY, SHIPPING_POLICY


TOOL_SCHEMAS = [
    {
        "name": "list_customer_orders",
        "description": (
            "List all orders for a customer ID (format 'CUST-XXXX'). Returns a "
            "brief entry per order: order_id, item, status, delivered_on, and a "
            "'damaged' flag. Use this FIRST when a request is vague (e.g. 'sort "
            "out my orders') so you can SEE what exists before deciding what to "
            "do next."
        ),
        "input_schema": {
            "type": "object",
            "properties": {"customer_id": {"type": "string"}},
            "required": ["customer_id"],
        },
    },
    {
        "name": "get_order",
        "description": (
            "Retrieve full details of one order by its order ID ('ORD-XXXX'): "
            "item, amount in INR, status, delivery date, and damaged flag. Use "
            "this to dig into a specific order after you've seen the list."
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
    {
        "name": "get_shipping_policy",
        "description": "Return the store's written SHIPPING policy. No inputs.",
        "input_schema": {"type": "object", "properties": {}},
    },
]


def list_customer_orders(customer_id: str) -> dict:
    customer = CUSTOMERS.get(customer_id)
    if customer is None:
        return {"error": f"No customer '{customer_id}'."}
    brief = []
    for oid in customer.get("order_ids", []):
        o = ORDERS.get(oid, {})
        brief.append({
            "order_id": oid,
            "item": o.get("item"),
            "status": o.get("status"),
            "delivered_on": o.get("delivered_on"),
            "damaged": o.get("damaged", False),
        })
    return {"customer_id": customer_id, "orders": brief}


def get_order(order_id: str) -> dict:
    o = ORDERS.get(order_id)
    return o if o else {"error": f"No order '{order_id}'."}


def get_refund_policy() -> dict:
    return {"policy": REFUND_POLICY}


def get_shipping_policy() -> dict:
    return {"policy": SHIPPING_POLICY}


TOOL_FUNCTIONS = {
    "list_customer_orders": list_customer_orders,
    "get_order": get_order,
    "get_refund_policy": get_refund_policy,
    "get_shipping_policy": get_shipping_policy,
}


def run_tool(tool_name: str, tool_input: dict) -> dict:
    func = TOOL_FUNCTIONS.get(tool_name)
    if func is None:
        return {"error": f"Unknown tool: {tool_name}"}
    return func(**tool_input)
