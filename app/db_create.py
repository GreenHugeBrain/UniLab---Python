import os
from app import db

def create_db():
    # Check if the database file exists
    db_path = os.path.join(os.getcwd(), 'instance', 'students.db')
    if not os.path.exists(db_path):
        print("Database does not exist. Creating a new one.")
        db.create_all()
    else:
        print("Database already exists. No need to create.")
