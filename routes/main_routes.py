from flask import render_template
from flask import current_app as app

def register_main_routes(app):
    @app.route("/")
    def home():
        """Display the welcome page of the MovieWeb App."""
        return render_template("index.html")
