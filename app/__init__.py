from flask import Flask, render_template
from werkzeug.exceptions import RequestEntityTooLarge
from .config import Development

def  create_app():
    app = Flask(__name__)
    app.config.from_object(Development)

    #registering the routes
    from .views import index, visualizer

    app.add_url_rule('/', 'index', index, methods=['GET', 'POST'])
    app.add_url_rule('/visualizer', 'visualizer', visualizer)

    @app.errorhandler(RequestEntityTooLarge)
    def handle_file_too_large(e):
        return render_template('upload.html', error="File is too large. Maximum size allowed is 5 MB."), 413


    return app