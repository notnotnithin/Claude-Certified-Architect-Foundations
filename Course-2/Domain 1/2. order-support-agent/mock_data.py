"""
mock_data.py
-------------
A tiny in-memory "database" for PyStack Mart, our fictional online store.

In a real application these records would live in a real database (Postgres,
DynamoDB, etc.) and you would query them over the network. For this beginner
demo we keep everything in plain Python dictionaries so you can focus on the
agent logic, not on database setup.

NOTE ON NAMES: All example customers use generic names (e.g., "Asha").
"""

# --------------------------------------------------------------------------
# CUSTOMERS keyed by customer_id
# --------------------------------------------------------------------------
CUSTOMERS = {
    "CUST-1001": {
        "customer_id": "CUST-1001",
        "name": "Asha Menon",
        "email": "asha.menon@example.com",
        "city": "Pune",
        "loyalty_tier": "Gold",
    },
    "CUST-1002": {
        "customer_id": "CUST-1002",
        "name": "Rahul Verma",
        "email": "rahul.verma@example.com",
        "city": "Mumbai",
        "loyalty_tier": "Silver",
    },
}

# --------------------------------------------------------------------------
# ORDERS keyed by order_id
# Amounts are in Indian Rupees (INR).
# --------------------------------------------------------------------------
ORDERS = {
    "ORD-5001": {
        "order_id": "ORD-5001",
        "customer_id": "CUST-1001",
        "item": "Wireless Mechanical Keyboard",
        "amount_inr": 4500,
        "status": "Delivered",
        "delivered_on": "2026-06-10",
    },
    "ORD-5002": {
        "order_id": "ORD-5002",
        "customer_id": "CUST-1001",
        "item": "USB-C Charging Cable",
        "amount_inr": 350,
        "status": "Delivered",
        "delivered_on": "2026-06-18",
    },
    "ORD-5003": {
        "order_id": "ORD-5003",
        "customer_id": "CUST-1002",
        "item": "Laptop Stand",
        "amount_inr": 1200,
        "status": "In Transit",
        "delivered_on": None,
    },
}

# --------------------------------------------------------------------------
# A very small "refund policy" the agent can read.
# Keeping this as text makes it easy for the model to reason about it.
# --------------------------------------------------------------------------
REFUND_POLICY = (
    "PyStack Mart Refund Policy:\n"
    "1. Refunds are allowed only for orders with status 'Delivered'.\n"
    "2. Orders still 'In Transit' cannot be refunded until delivered.\n"
    "3. Refunds must be requested within 30 days of delivery.\n"
    "4. The full order amount is refunded to the original payment method."
)

# --------------------------------------------------------------------------
# A small shipping/delivery FAQ the agent can read.
# Added in Demo 1.2 so the "shipping" specialist subagent has something to do.
# --------------------------------------------------------------------------
SHIPPING_POLICY = (
    "PyStack Mart Shipping Policy:\n"
    "1. Standard delivery takes 3-5 business days within India.\n"
    "2. Orders marked 'In Transit' are on the way and cannot be cancelled.\n"
    "3. Delivery is free for Gold loyalty-tier customers.\n"
    "4. Once delivered, report any damage within 7 days."
)
