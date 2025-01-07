from dotenv import dotenv_values
from flask import Flask, Response, request, jsonify
import mongoengine as me
from model import User, Post
from utils import salt_hash_password, verify_password
from bson.json_util import dumps


config = dotenv_values(".env")
app = Flask(__name__)


def init_mongo_client(app: Flask):
    try:
        me.connect(config["DB_NAME"], host="localhost", port=27017)
        print("Connected to DB successfully.")
    except Exception as exc:
        print("Error connecting to DB: ", exc)

init_mongo_client(app)


@app.route("/")
def hello():
    return {"message": "Welcome to the Flask with MongoDB tutorial!!!"}

@app.route("/users")
def get_users():
    users = [user.to_mongo().to_dict() for user in User.objects]
    users_json = dumps({"Users": users})

    return Response(
            users_json,
            content_type="application/json",
        )

@app.route("/register", methods=["POST"])
def register():

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
    
    # Check if the user already exists
    if User.objects(email=user.email):
        return jsonify({"message": "User already exists."}), 400
    
    # Save the new user
    salt_n_hash = salt_hash_password(user.password)
    user.salt = salt_n_hash["salt"]
    user.password = salt_n_hash["hash"]

    user.save()

    return jsonify({"message": "Saved new user successfully."}), 200


@app.route("/login", methods=["POST"])
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
    
    return jsonify({"message": "Logged in successfully."}), 200