from flask import Flask, render_template
from werkzeug.exceptions import RequestEntityTooLarge
from .config import Config

def  create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    #registering the routes
    from .views import index, visualizer, describe

    app.add_url_rule('/', 'index', index, methods=['GET', 'POST'])
    app.add_url_rule('/visualizer', 'visualizer', visualizer)
    app.add_url_rule('/describe', 'describe', describe)

    @app.errorhandler(RequestEntityTooLarge)
    def handle_file_too_large(e):
        return render_template('upload.html', error=f"File is too large. Maximum size allowed is {Config.MAX_CONTENT_LENGTH / 1024 / 1024} MB."), 413


    return app