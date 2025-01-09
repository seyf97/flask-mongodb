from flask import Flask, jsonify
from flask_jwt_extended import JWTManager
from app.routes import articles, users
from app.errors import errors
from app.db import init_db
from flasgger import Swagger


def create_app():
    app = Flask(__name__)
    app.config.from_object('config.DevConfig')

    # For JWT auth
    JWTManager(app)

    # Initialize database connection
    init_db(app)

    swagger_template = {
    "swagger": "2.0",
    "info": {
        "title": "Blog API",
        "description": "API documentation for the Blog backend API.",
        "version": "1.0.0"
    },
    "securityDefinitions": {
        "Bearer": {
            "type": "apiKey",
            "name": "Authorization",
            "in": "header",
            "description": "Enter the token with the `Bearer` prefix, e.g., 'Bearer abcde12345'."
        }
    }
}

    Swagger(app, template=swagger_template)


    # Register Blueprints
    app.register_blueprint(articles.bp)
    app.register_blueprint(users.bp)
    app.register_blueprint(errors)

    return app