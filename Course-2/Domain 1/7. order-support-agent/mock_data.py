"""
mock_data.py
-------------
A tiny in-memory "database" for PyStack Mart, our fictional online store.

In Demo 7 the key idea is TIME: we run the agent, stop, and come back later.
Between visits, data can CHANGE (an order that was 'In Transit' becomes
'Delivered'). So this file also exposes a tiny helper to simulate that change,
which lets us show why a resumed session must be told what changed.

NOTE ON NAMES: All example customers use generic names (e.g., "Asha").
"""

CUSTOMERS = {
    "CUST-1001": {
        "customer_id": "CUST-1001",
        "name": "Asha Menon",
        "email": "asha.menon@example.com",
        "city": "Pune",
        "address": "12 MG Road, Pune, 411001",
        "loyalty_tier": "Gold",
    },
    "CUST-1002": {
        "customer_id": "CUST-1002",
        "name": "Rahul Verma",
        "email": "rahul.verma@example.com",
        "city": "Mumbai",
        "address": "45 Linking Road, Mumbai, 400050",
        "loyalty_tier": "Silver",
    },
}

# Amounts are in Indian Rupees (INR). "today" for this demo is ~2026-06-28.
ORDERS = {
    "ORD-5001": {
        "order_id": "ORD-5001",
        "customer_id": "CUST-1001",
        "item": "Wireless Mechanical Keyboard",
        "amount_inr": 4500,
        "status": "Delivered",
        "delivered_on": "2026-06-10",
    },
    "ORD-5005": {
        "order_id": "ORD-5005",
        "customer_id": "CUST-1001",
        "item": "Webcam 1080p",
        "amount_inr": 2200,
        "status": "In Transit",       # <- this one will "change" between visits
        "delivered_on": None,
    },
}

REFUND_POLICY = (
    "PyStack Mart Refund Policy:\n"
    "1. Refunds are allowed only for orders with status 'Delivered'.\n"
    "2. Orders still 'In Transit' cannot be refunded until delivered.\n"
    "3. Refunds must be requested within 30 days of delivery.\n"
    "4. The full order amount is refunded to the original payment method."
)


def mark_order_delivered(order_id: str, delivered_on: str) -> None:
    """
    Simulate the outside world changing while a session was paused:
    an 'In Transit' order becomes 'Delivered'. We use this in the resume
    demo to show why a resumed session must be informed of the change.
    """
    o = ORDERS.get(order_id)
    if o:
        o["status"] = "Delivered"
        o["delivered_on"] = delivered_on
