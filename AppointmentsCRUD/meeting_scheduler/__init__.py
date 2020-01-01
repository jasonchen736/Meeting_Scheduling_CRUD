from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from meeting_scheduler.errors import register_error_handlers
from meeting_scheduler.extensions import db
from meeting_scheduler.routes import add_urls


def create_app():
    app = Flask(__name__)
    app.config.from_object('config.Config')

    db.init_app(app)
    register_error_handlers(app)
    add_urls(app)

    return app


app = create_app()
