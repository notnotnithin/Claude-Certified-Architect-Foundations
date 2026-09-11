"""
tools.py
---------
The TOOLS our agents can use. Same idea as before: each tool has a SCHEMA
(what the model reads) and a FUNCTION (the code that runs).

NEW IN DEMO 5 — tools that have real CONSEQUENCES, so compliance matters:
  - verify_identity   : check a customer ID matches an order (a prerequisite)
  - process_refund    : actually "pay out" a refund (must be controlled!)
  - escalate_to_human : hand a case to a human agent

These let us show:
  - a PREREQUISITE GATE (no refund before identity is verified), and
  - a THRESHOLD BLOCK (no automatic refund above Rs. 500 -> escalate),
both enforced by HOOKS in hooks.py, not by hoping the model behaves.
"""

from mock_data import (
    CUSTOMERS, ORDERS, REFUND_POLICY, SHIPPING_POLICY,
)


# ==========================================================================
# TOOL SCHEMAS
# ==========================================================================
TOOL_SCHEMAS = [
    {
        "name": "get_customer",
        "description": (
            "Look up a customer's account using their customer ID "
            "(format 'CUST-XXXX'). Returns name, email, city, address, tier."
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "customer_id": {"type": "string"},
            },
            "required": ["customer_id"],
        },
    },
    {
        "name": "get_order",
        "description": (
            "Retrieve a single order using its order ID (format 'ORD-XXXX'). "
            "Returns item, amount in INR, status, and delivery date."
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "order_id": {"type": "string"},
            },
            "required": ["order_id"],
        },
    },
    {
        "name": "get_refund_policy",
        "description": "Return the store's written REFUND policy. No inputs.",
        "input_schema": {"type": "object", "properties": {}},
    },
    {
        "name": "verify_identity",
        "description": (
            "Verify that a customer ID is the owner of a given order. Returns "
            "{'verified': true/false}. You MUST call this and get verified=true "
            "before processing any refund."
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "customer_id": {"type": "string"},
                "order_id": {"type": "string"},
            },
            "required": ["customer_id", "order_id"],
        },
    },
    {
        "name": "process_refund",
        "description": (
            "Process a refund for an order. Provide order_id and amount_inr. "
            "Only call this after the customer's identity has been verified."
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "order_id": {"type": "string"},
                "amount_inr": {"type": "number"},
            },
            "required": ["order_id", "amount_inr"],
        },
    },
    {
        "name": "escalate_to_human",
        "description": (
            "Hand the case to a human agent. Provide a short structured "
            "summary so the human has everything they need."
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "summary": {"type": "string"},
            },
            "required": ["summary"],
        },
    },
]


# ==========================================================================
# TOOL IMPLEMENTATIONS
# ==========================================================================
def get_customer(customer_id: str) -> dict:
    c = CUSTOMERS.get(customer_id)
    return c if c else {"error": f"No customer '{customer_id}'."}


def get_order(order_id: str) -> dict:
    o = ORDERS.get(order_id)
    return o if o else {"error": f"No order '{order_id}'."}


def get_refund_policy() -> dict:
    return {"policy": REFUND_POLICY}


def verify_identity(customer_id: str, order_id: str) -> dict:
    order = ORDERS.get(order_id)
    if order is None:
        return {"verified": False, "reason": f"No order '{order_id}'."}
    verified = (order.get("customer_id") == customer_id)
    return {"verified": verified, "customer_id": customer_id, "order_id": order_id}


def process_refund(order_id: str, amount_inr: float) -> dict:
    # In a real system this would move money. Here we just confirm.
    return {
        "order_id": order_id,
        "refunded_amount_inr": amount_inr,
        "status": "refund processed",
    }


def escalate_to_human(summary: str) -> dict:
    return {"status": "escalated", "handoff_summary": summary}


TOOL_FUNCTIONS = {
    "get_customer": get_customer,
    "get_order": get_order,
    "get_refund_policy": get_refund_policy,
    "verify_identity": verify_identity,
    "process_refund": process_refund,
    "escalate_to_human": escalate_to_human,
}


def run_tool(tool_name: str, tool_input: dict) -> dict:
    func = TOOL_FUNCTIONS.get(tool_name)
    if func is None:
        return {"error": f"Unknown tool: {tool_name}"}
    return func(**tool_input)
