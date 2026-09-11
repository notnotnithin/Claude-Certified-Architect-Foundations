"""
tools.py
---------
The TOOLS our agents can use. Same idea as before: each tool has a SCHEMA
(what the model reads to choose a tool) and a FUNCTION (the code that runs).

Tools are grouped by SPECIALIST ROLE. In Demo 4 we have THREE groups, so a
multi-concern request (status + refund + address change) can be split across
three specialists:

  - ORDER   tools -> get_order                       (order status)
  - POLICY  tools -> get_refund_policy,
                     get_shipping_policy              (the rules)
  - ACCOUNT tools -> get_customer, update_address     (the customer's account)
"""

from mock_data import CUSTOMERS, ORDERS, REFUND_POLICY, SHIPPING_POLICY


# ==========================================================================
# TOOL SCHEMAS, grouped by specialist role
# ==========================================================================
ORDER_TOOL_SCHEMAS = [
    {
        "name": "get_order",
        "description": (
            "Retrieve a single order using its order ID (format: 'ORD-XXXX'). "
            "Returns item, amount in INR, status ('Delivered' or 'In Transit'), "
            "and delivery date. Use this for any question about a specific "
            "order or its status."
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

ACCOUNT_TOOL_SCHEMAS = [
    {
        "name": "get_customer",
        "description": (
            "Look up a customer's account record using their customer ID "
            "(format: 'CUST-XXXX'). Returns name, email, city, address, and "
            "loyalty tier. Use this to verify who the customer is or to read "
            "their current account details."
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
        "name": "update_address",
        "description": (
            "Update the shipping address on a customer's account. Provide the "
            "customer ID and the new full address. Returns the updated record. "
            "Use this when the customer asks to change or correct their address."
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "customer_id": {
                    "type": "string",
                    "description": "The customer ID, e.g. 'CUST-1001'.",
                },
                "new_address": {
                    "type": "string",
                    "description": "The new full address to save.",
                },
            },
            "required": ["customer_id", "new_address"],
        },
    },
]


# ==========================================================================
# TOOL IMPLEMENTATIONS  (the real code that runs)
# ==========================================================================
def get_order(order_id: str) -> dict:
    order = ORDERS.get(order_id)
    if order is None:
        return {"error": f"No order found with ID '{order_id}'."}
    return order


def get_refund_policy() -> dict:
    return {"policy": REFUND_POLICY}


def get_shipping_policy() -> dict:
    return {"policy": SHIPPING_POLICY}


def get_customer(customer_id: str) -> dict:
    customer = CUSTOMERS.get(customer_id)
    if customer is None:
        return {"error": f"No customer found with ID '{customer_id}'."}
    return customer


def update_address(customer_id: str, new_address: str) -> dict:
    customer = CUSTOMERS.get(customer_id)
    if customer is None:
        return {"error": f"No customer found with ID '{customer_id}'."}
    old = customer["address"]
    customer["address"] = new_address   # update the in-memory record
    return {
        "customer_id": customer_id,
        "old_address": old,
        "new_address": new_address,
        "status": "address updated",
    }


# One lookup table so the agent loop can find a function by tool name.
TOOL_FUNCTIONS = {
    "get_order": get_order,
    "get_refund_policy": get_refund_policy,
    "get_shipping_policy": get_shipping_policy,
    "get_customer": get_customer,
    "update_address": update_address,
}


def run_tool(tool_name: str, tool_input: dict) -> dict:
    """Look up the function for `tool_name` and call it with `tool_input`."""
    func = TOOL_FUNCTIONS.get(tool_name)
    if func is None:
        return {"error": f"Unknown tool: {tool_name}"}
    return func(**tool_input)
