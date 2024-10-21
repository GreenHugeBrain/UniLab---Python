from app import create_app, db
from models import Student, Subject, Grade

app = create_app()

with app.app_context():
    db.create_all() 
    print("Database created successfully!")
