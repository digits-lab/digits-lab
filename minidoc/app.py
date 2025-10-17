import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

# Get the absolute path of the project directory
project_dir = os.path.abspath(os.path.dirname(__file__))

# Create the Flask app
app = Flask(__name__, template_folder=os.path.join(project_dir, 'frontend/templates'), static_folder=os.path.join(project_dir, 'frontend/static'))

# Configure the database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(project_dir, '../database/minidoc.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'your_secret_key'  # Replace with a real secret key

# Initialize the database
db = SQLAlchemy(app)

import routes

if __name__ == '__main__':
    app.run(debug=True)