"""
Seed script — populates the database with a demo user + 40 realistic expenses.
Run: .\venv\Scripts\python seed_data.py
"""

from app import create_app, db
from app.models import User, Expense
from datetime import date, timedelta
import random

app = create_app()

DEMO_EMAIL    = "demo@example.com"
DEMO_PASSWORD = "demo1234"
DEMO_USERNAME = "DemoUser"

# 40 realistic expenses spread across the last 3 months (amounts in Indian Rupees)
EXPENSES = [
    # Food & Dining
    ("Grocery Shopping",        1850.00, "Food & Dining",        -2),
    ("McDonald's Lunch",         320.00, "Food & Dining",        -4),
    ("Pizza Night",              780.00, "Food & Dining",        -7),
    ("Coffee & Snacks",          220.00, "Food & Dining",       -10),
    ("Weekly Groceries",        2400.00, "Food & Dining",       -14),
    ("Sushi Dinner",            1350.00, "Food & Dining",       -20),
    ("Bakery Items",             430.00, "Food & Dining",       -25),
    ("Fruit & Vegetables",       620.00, "Food & Dining",       -35),
    ("KFC Takeout",              510.00, "Food & Dining",       -42),
    ("Monthly Groceries",       3200.00, "Food & Dining",       -50),

    # Transport
    ("Uber Ride",                480.00, "Transport",            -3),
    ("Monthly Bus Pass",        1500.00, "Transport",           -30),
    ("Petrol Fill-up",          1900.00, "Transport",           -15),
    ("Taxi to Airport",         1100.00, "Transport",           -60),
    ("Parking Fee",              250.00, "Transport",            -8),

    # Bills & Utilities
    ("Electricity Bill",        2400.00, "Bills & Utilities",   -28),
    ("Internet Bill",           1499.00, "Bills & Utilities",   -28),
    ("Water Bill",               900.00, "Bills & Utilities",   -58),
    ("Phone Bill",               699.00, "Bills & Utilities",   -58),
    ("Gas Bill",                 850.00, "Bills & Utilities",   -88),

    # Entertainment
    ("Netflix Subscription",     649.00, "Entertainment",        -1),
    ("Movie Tickets",            800.00, "Entertainment",       -12),
    ("Spotify Premium",          119.00, "Entertainment",       -31),
    ("Video Game",              2499.00, "Entertainment",       -45),
    ("Concert Tickets",         3500.00, "Entertainment",       -55),

    # Shopping
    ("New Shoes",               3299.00, "Shopping",            -6),
    ("Amazon Order",            1540.00, "Shopping",            -18),
    ("Clothing",                4200.00, "Shopping",            -33),
    ("Home Decor",              2100.00, "Shopping",            -48),
    ("Books",                    950.00, "Shopping",            -70),

    # Health & Medical
    ("Doctor Visit",            1500.00, "Health & Medical",    -9),
    ("Pharmacy",                 780.00, "Health & Medical",    -22),
    ("Gym Membership",          1200.00, "Health & Medical",    -30),
    ("Vitamins & Supplements",   650.00, "Health & Medical",    -65),

    # Education
    ("Online Course",            999.00, "Education",           -16),
    ("Textbooks",               1800.00, "Education",           -50),

    # Personal Care
    ("Haircut",                  400.00, "Personal Care",       -11),
    ("Skincare Products",       1650.00, "Personal Care",       -40),

    # Travel
    ("Hotel Stay",              5500.00, "Travel",              -75),
    ("Flight Ticket",           7800.00, "Travel",              -80),
]

def seed():
    with app.app_context():
        # ── Remove existing demo user if present ──────────────────────
        existing = User.query.filter_by(email=DEMO_EMAIL).first()
        if existing:
            db.session.delete(existing)
            db.session.commit()
            print("Removed previous demo user.")

        # ── Create demo user ──────────────────────────────────────────
        user = User(username=DEMO_USERNAME, email=DEMO_EMAIL)
        user.set_password(DEMO_PASSWORD)
        db.session.add(user)
        db.session.commit()
        print(f"Created user: {DEMO_EMAIL} / {DEMO_PASSWORD}")

        # ── Add expenses ──────────────────────────────────────────────
        today = date.today()
        for title, amount, category, day_offset in EXPENSES:
            exp = Expense(
                title=title,
                amount=amount,
                category=category,
                date=today + timedelta(days=day_offset),
                user_id=user.id,
            )
            db.session.add(exp)

        db.session.commit()
        print(f"Added {len(EXPENSES)} expenses.")
        print()
        print("=" * 45)
        print("  Login credentials")
        print("=" * 45)
        print(f"  Email   : {DEMO_EMAIL}")
        print(f"  Password: {DEMO_PASSWORD}")
        print("=" * 45)
        print("  Run the app:  .\\venv\\Scripts\\python run.py")
        print("  Open:         http://127.0.0.1:5000")
        print("=" * 45)

if __name__ == "__main__":
    seed()
