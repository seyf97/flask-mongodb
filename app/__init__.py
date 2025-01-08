from flask import Flask, jsonify
from flask_jwt_extended import JWTManager
from app.routes import articles, users
from app.errors import errors
from app.db import init_db


def create_app():
    app = Flask(__name__)
    app.config.from_object('config.DevConfig')

    # For JWT auth
    JWTManager(app)

    # Initialize database connection
    init_db(app)

    # Register Blueprints
    app.register_blueprint(articles.bp)
    app.register_blueprint(users.bp)
    app.register_blueprint(errors)

    return app