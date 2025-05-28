from flask import Flask
from models.app_models import db
from datamanager.sqlite_data_manager import SQLiteDataManager
from routes import register_routes
import os


def create_app():
    app = Flask(__name__)
    app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")
    app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL")
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)

    with app.app_context():
        db.create_all()
        app.data_manager = SQLiteDataManager(app.config['SQLALCHEMY_DATABASE_URI'])
        register_routes(app)

    return app

app = create_app()

if __name__ == "__main__":
    app.run(debug=True)