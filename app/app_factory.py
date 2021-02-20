from flask import Flask

from app import settings
from app.views import alert


def get_app():

    app = Flask(__name__)
    app.config.from_object(settings)

    app.register_blueprint(alert.bp)

    return app
