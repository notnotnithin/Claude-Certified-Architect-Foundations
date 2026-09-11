"""
mock_data.py
-------------
A tiny in-memory "database" for PyStack Mart, our fictional online store.

NEW IN DEMO 6: customer CUST-1001 has SEVERAL orders in DIFFERENT states, so a
vague request like "sort out my recent orders" can't be planned up front — the
agent must LOOK first, then decide what to do based on what it finds.

  - ORD-5001 : Delivered, recent          -> refund window may be open
  - ORD-5002 : Delivered, long ago        -> refund window likely closed
  - ORD-5005 : In Transit                 -> a delivery/shipping concern
  - ORD-5006 : Delivered but DAMAGED flag  -> needs a damage/return path

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
        # which orders belong to this customer (used by adaptive lookup)
        "order_ids": ["ORD-5001", "ORD-5002", "ORD-5005", "ORD-5006"],
    },
    "CUST-1002": {
        "customer_id": "CUST-1002",
        "name": "Rahul Verma",
        "email": "rahul.verma@example.com",
        "city": "Mumbai",
        "address": "45 Linking Road, Mumbai, 400050",
        "loyalty_tier": "Silver",
        "order_ids": ["ORD-5003"],
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
        "delivered_on": "2026-06-10",   # recent -> within 30-day window
        "damaged": False,
    },
    "ORD-5002": {
        "order_id": "ORD-5002",
        "customer_id": "CUST-1001",
        "item": "USB-C Charging Cable",
        "amount_inr": 350,
        "status": "Delivered",
        "delivered_on": "2026-04-01",   # long ago -> window likely closed
        "damaged": False,
    },
    "ORD-5003": {
        "order_id": "ORD-5003",
        "customer_id": "CUST-1002",
        "item": "Laptop Stand",
        "amount_inr": 1200,
        "status": "In Transit",
        "delivered_on": None,
        "damaged": False,
    },
    "ORD-5005": {
        "order_id": "ORD-5005",
        "customer_id": "CUST-1001",
        "item": "Webcam 1080p",
        "amount_inr": 2200,
        "status": "In Transit",
        "delivered_on": None,
        "damaged": False,
    },
    "ORD-5006": {
        "order_id": "ORD-5006",
        "customer_id": "CUST-1001",
        "item": "Desk Lamp",
        "amount_inr": 900,
        "status": "Delivered",
        "delivered_on": "2026-06-20",
        "damaged": True,                # flagged damaged -> needs a return path
    },
}

REFUND_POLICY = (
    "PyStack Mart Refund Policy:\n"
    "1. Refunds are allowed only for orders with status 'Delivered'.\n"
    "2. Orders still 'In Transit' cannot be refunded until delivered.\n"
    "3. Refunds must be requested within 30 days of delivery.\n"
    "4. The full order amount is refunded to the original payment method."
)

SHIPPING_POLICY = (
    "PyStack Mart Shipping Policy:\n"
    "1. Standard delivery takes 3-5 business days within India.\n"
    "2. Orders marked 'In Transit' are on the way and cannot be cancelled.\n"
    "3. Delivery is free for Gold loyalty-tier customers.\n"
    "4. Once delivered, report any damage within 7 days."
)
