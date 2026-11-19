# db.py
from extensions import db
from app import app
from models import User

with app.app_context():
    db.create_all()
    print("Database tables created successfully!")


