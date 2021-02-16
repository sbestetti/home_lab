from flask import Flask

from app import settings


def get_app():

    app = Flask(__name__)
    app.config.from_object(settings)

    @app.route("/healthz")
    def healthz():
        return "OK", 200

    return app