from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from app_models import db, User, Movie  # db is the SQLAlchemy instance

app = Flask(__name__)

# Configure SQLite database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///movies.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Bind SQLAlchemy to the app
db.init_app(app)

# Create tables within the app context
with app.app_context():
    db.create_all()
    print("Database and tables created successfully!")

# Optional: Define a basic route
@app.route("/")
def home():
    return "Welcome to MoviWebApp!"

if __name__ == "__main__":
    app.run(debug=True)