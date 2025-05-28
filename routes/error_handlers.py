from flask import render_template

def register_error_handlers(app):

    @app.errorhandler(404)
    def page_not_found(e):
        """Handle 404 errors with a custom message."""
        return render_template('404.html', message=getattr(e, 'description', 'Page not found.')), 404

    @app.errorhandler(500)
    def internal_error(e):
        """Handle unexpected internal server errors gracefully."""
        return render_template('500.html', message="An internal server error occurred."), 500