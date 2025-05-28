from flask import render_template
from flask import current_app as app

def register_main_routes(app):
    @app.route("/")
    def home():
        """Render the welcome page of the MovieWeb App.
        This route serves as the landing page and provides
        a brief introduction or navigation to other parts of the app.
        Returns:
            Response: Rendered template for the home page."""
        return render_template("index.html")
