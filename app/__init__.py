from flask import Flask
from .config import Development

def  create_app():
    app = Flask(__name__)
    app.config.from_object(Development)

    #registering the routes
    from .views import upload, visualizer

    app.add_url_rule('/', 'upload', upload, methods=['GET', 'POST'])
    app.add_url_rule('/visualizer', 'visualizer', visualizer)



    return app