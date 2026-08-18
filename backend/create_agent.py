from database.connection import SessionLocal
from database.models import User
from security import hash_password


db = SessionLocal()

try:
    agent = User(
        name="Support Agent",
        email="agent@example.com",
        password_hash=hash_password("agent@12345"),
        role="AGENT",
    )

    db.add(agent)
    db.commit()

    print("Agent created successfully")

finally:
    db.close()