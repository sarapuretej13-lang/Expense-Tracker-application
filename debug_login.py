"""
Debug script to test login logic directly.
Run: .\venv\Scripts\python debug_login.py
"""
from app import create_app, db
from app.models import User

app = create_app()

with app.app_context():
    print("=== Users in database ===")
    users = User.query.all()
    for u in users:
        print(f"  id={u.id}  username={u.username}  email={u.email}")

    print()
    email = input("Enter the email you registered with: ").strip().lower()
    password = input("Enter the password you used: ").strip()

    user = User.query.filter_by(email=email).first()
    if not user:
        print(f"ERROR: No user found with email '{email}'")
    else:
        print(f"User found: {user.username}")
        result = user.check_password(password)
        print(f"Password check: {'PASS ✓' if result else 'FAIL ✗'}")
        if not result:
            print("The stored hash is:", user.password_hash[:50], "...")
