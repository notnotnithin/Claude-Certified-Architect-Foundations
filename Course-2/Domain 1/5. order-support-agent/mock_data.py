"""
mock_data.py
-------------
A tiny in-memory "database" for PyStack Mart, our fictional online store.

NEW IN DEMO 5: orders now come from TWO "systems" that use DIFFERENT formats,
so a normalization hook has something real to fix:

  - Some orders store the delivery date as an ISO string ("2026-06-10").
  - One order comes from a legacy system that stores it as a UNIX timestamp
    (seconds since 1970) and uses a NUMERIC status code instead of text.

A PostToolUse hook will normalize all of these into ONE consistent shape
before the agent ever sees them.

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

# --------------------------------------------------------------------------
# ORDERS keyed by order_id.  Amounts are in Indian Rupees (INR).
#
# Notice the MIXED formats:
#   - ORD-5001 / ORD-5002 : modern system -> status text + ISO date string.
#   - ORD-5004            : legacy system -> numeric status_code + unix_ts.
# The normalization hook (see hooks.py) smooths these into one shape.
# --------------------------------------------------------------------------
ORDERS = {
    "ORD-5001": {
        "order_id": "ORD-5001",
        "customer_id": "CUST-1001",
        "item": "Wireless Mechanical Keyboard",
        "amount_inr": 4500,
        "status": "Delivered",            # text status
        "delivered_on": "2026-06-10",     # ISO date string
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
    # Legacy-system order: numeric status code + unix timestamp.
    # status_code 3 == Delivered;  unix_ts 1781049600 == 2026-06-10 (UTC).
    "ORD-5004": {
        "order_id": "ORD-5004",
        "customer_id": "CUST-1001",
        "item": "Laptop Sleeve",
        "amount_inr": 800,
        "status_code": 3,                 # numeric code, NOT text
        "delivered_unix_ts": 1781049600,  # unix timestamp (= 2026-06-10), NOT ISO
    },
}

# --------------------------------------------------------------------------
# Policies the agent can read.
# --------------------------------------------------------------------------
REFUND_POLICY = (
    "PyStack Mart Refund Policy:\n"
    "1. Refunds are allowed only for orders with status 'Delivered'.\n"
    "2. Orders still 'In Transit' cannot be refunded until delivered.\n"
    "3. Refunds must be requested within 30 days of delivery.\n"
    "4. The full order amount is refunded to the original payment method.\n"
    "5. Refunds of Rs. 500 or less can be processed automatically; refunds\n"
    "   ABOVE Rs. 500 must be escalated to a human agent for approval."
)

SHIPPING_POLICY = (
    "PyStack Mart Shipping Policy:\n"
    "1. Standard delivery takes 3-5 business days within India.\n"
    "2. Orders marked 'In Transit' are on the way and cannot be cancelled.\n"
    "3. Delivery is free for Gold loyalty-tier customers.\n"
    "4. Once delivered, report any damage within 7 days."
)

# Map legacy numeric status codes to text (used by the normalization hook).
STATUS_CODE_TO_TEXT = {
    1: "Placed",
    2: "In Transit",
    3: "Delivered",
    4: "Cancelled",
}
