from flask import Blueprint, jsonify, request
from flask_jwt_extended import create_access_token
from flasgger import swag_from
import mongoengine as me
from app.models.user import User
from app.utils import salt_hash_password, verify_password
from app.db import set_fields
import os

bp = Blueprint('users', __name__, url_prefix = None)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))


@bp.route("/register", methods=["POST"])
@swag_from(os.path.join(BASE_DIR, "docs/register.yml"))
def register():

    user_info = request.get_json(force=True, silent=True, cache=False)

    # Check if the JSON body is valid
    if user_info is None:
        return jsonify({"message": "Invalid JSON body."}), 400
    
    # Check the fields
    email = user_info.get("email")
    password = user_info.get("password")

    if not email or not password:
        return jsonify({"message": "Email and password are required."}), 400
    
    # Check if the user already exists
    if User.objects(email=email):
        return jsonify({"message": "User already exists."}), 400
    
    # Set the fields
    exclude_fields = ["salt"]
    user = User()
    try:
        user = set_fields(user, user_info, exclude_fields)
    except me.errors.FieldDoesNotExist as exc:
        return jsonify({"message": str(exc)}), 400
    
    # Save the new user
    salt_n_hash = salt_hash_password(user.password)
    user.salt = salt_n_hash["salt"]
    user.password = salt_n_hash["hash"]

    try:
        user.save()
    except me.errors.ValidationError as exc:
        return jsonify({"message": str(exc)}), 400

    return jsonify({"message": "Saved new user successfully."}), 201


@bp.route("/login", methods=["POST"])
@swag_from(os.path.join(BASE_DIR, "docs/login.yml"))
def login():

    user_info = request.get_json(force=True, silent=True, cache=False)

    # Check if the JSON body is valid
    if user_info is None:
        return jsonify({"message": "Invalid JSON body."}), 400
    
    # Check the fields
    email = user_info.get("email")
    password = user_info.get("password")

    if not email or not password:
        return jsonify({"message": "email and password are required."}), 400
    
    if len(user_info.keys()) > 2:
        return jsonify({"message": "Only email and password fields are allowed."}), 400
    
    # Check if the required fields are present
    # Technically should work since the prev checks should have caught this
    try:
        user = User(**user_info)
    except me.errors.FieldDoesNotExist:
        return jsonify({"message": "Invalid field name."}), 400
    
    # Check if the user exists
    if not User.objects(email=user.email):
        return jsonify({"message": "User doesn't exist, please register."}), 404
    
    # Check the password
    db_user = User.objects(email=user.email).first()

    # Wrong password
    if not verify_password(user.password, db_user.salt, db_user.password):
        return jsonify({"message": "Incorrect email or password."}), 401
    
    # JWT token
    jwt_token = create_access_token(identity=db_user.email)

    return jsonify({"jwt_token": jwt_token,
                    "message": "Logged in successfully."}), 200