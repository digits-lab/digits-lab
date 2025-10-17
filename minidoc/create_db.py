import os
import sys

# Add the project root to the Python path
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, project_root)

from minidoc.app import app, db

def create_tables():
    with app.app_context():
        db.create_all()
        print("Database tables created successfully.")

if __name__ == '__main__':
    create_tables()