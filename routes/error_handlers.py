from flask import render_template

def register_error_handlers(app):
    """
    Registers global error handlers on the Flask app.
    Handles HTTP 404 and 500 errors with custom templates.
    """
    @app.errorhandler(404)
    def page_not_found(e):
        return render_template('404.html', message=getattr(e, 'description', 'Page not found.')), 404

    @app.errorhandler(500)
    def internal_error(e):
        return render_template('500.html', message="An internal server error occurred."), 500