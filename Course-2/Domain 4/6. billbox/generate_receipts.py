"""
generate_receipts.py
====================================================================
A small helper that creates a folder of ~100 sample receipts, so we have a
realistic "bulk" pile to batch-process without shipping 100 files by hand.

This does NOT call the API. It just writes plain-text receipts to the
receipts_bulk/ folder. Run it once before submit_batch.py.

HOW TO RUN (from the project root, in cmd):

    python generate_receipts.py
"""

import os
import random

ROOT = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(ROOT, "receipts_bulk")

MERCHANTS = [
    ("FreshMart Supermarket", "grocery"),
    ("Spice Garden Restaurant", "restaurant"),
    ("QuickMart Grocers", "grocery"),
    ("Cafe Sunrise", "restaurant"),
    ("Green Valley Kirana", "grocery"),
    ("Tandoor House", "restaurant"),
    ("City Power Ltd", "utility"),
    ("Pune Water Works", "utility"),
]

AREAS = ["FC Road", "MG Road", "Baner", "Kothrud", "Aundh", "Camp", "Viman Nagar"]

GROCERY_ITEMS = [
    ("Toor Dal 1kg", 145), ("Basmati Rice 5kg", 480), ("Amul Butter 500g", 275),
    ("Sugar 1kg", 55), ("Sunflower Oil 1L", 165), ("Tea 500g", 240),
    ("Wheat Flour 5kg", 250), ("Salt 1kg", 28), ("Milk 1L", 66), ("Bread", 45),
]
RESTAURANT_ITEMS = [
    ("Paneer Butter Masala", 320), ("Garlic Naan", 70), ("Butter Roti", 45),
    ("Jeera Rice", 180), ("Masala Chaas", 60), ("Gulab Jamun", 90),
    ("Veg Biryani", 260), ("Dal Tadka", 190),
]


def make_grocery(merchant, area, n):
    items = random.sample(GROCERY_ITEMS, random.randint(3, 6))
    lines = [f"{name:22} Rs. {price:.2f}" for name, price in items]
    subtotal = sum(p for _, p in items)
    gst = round(subtotal * 0.05, 2)
    total = round(subtotal + gst, 2)
    return f"""{merchant}
{area}, Pune
GSTIN: 27ABCDE{1000 + n}F1Z5
Date: {random.randint(1,28):02d}/10/2026

{chr(10).join(lines)}
Subtotal: Rs. {subtotal:.2f}
GST (5%): Rs. {gst:.2f}
Total: Rs. {total:.2f}
"""


def make_restaurant(merchant, area, n):
    items = random.sample(RESTAURANT_ITEMS, random.randint(3, 5))
    lines = [f"{name:22} {price}" for name, price in items]
    subtotal = sum(p for _, p in items)
    total = round(subtotal * 1.05, 2)
    return f"""{merchant} - {area}, Pune
GST: 27PQRXS{2000 + n}K1Z3
Date: {random.randint(1,28):02d} Oct 2026

{chr(10).join(lines)}
Food Total: {subtotal}
Grand Total: {total}
"""


def make_utility(merchant, area, n):
    units = random.randint(100, 400)
    energy = units * 6
    total = energy + 130 + round(energy * 0.1)
    return f"""{merchant}
Consumer: Asha Kulkarni
Address: {area}, Pune
Date: {random.randint(1,28):02d}/10/2026

Units Consumed: {units} kWh
Energy Charges: Rs {energy}.00
Fixed Charges: Rs 130.00
Amount Payable: Rs {total}.00
"""


def main(count=100):
    os.makedirs(OUT, exist_ok=True)
    for n in range(1, count + 1):
        merchant, kind = random.choice(MERCHANTS)
        area = random.choice(AREAS)
        if kind == "grocery":
            text = make_grocery(merchant, area, n)
        elif kind == "restaurant":
            text = make_restaurant(merchant, area, n)
        else:
            text = make_utility(merchant, area, n)
        with open(os.path.join(OUT, f"receipt_{n:03d}.txt"), "w", encoding="utf-8") as f:
            f.write(text)
    print(f"Created {count} receipts in receipts_bulk/")


if __name__ == "__main__":
    main()
