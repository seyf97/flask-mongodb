from dotenv import dotenv_values
from flask import Flask
from mongoengine import connect
from model import User, Post
from utils import bson_to_json

config = dotenv_values(".env")
app = Flask(__name__)


def init_mongo_client(app: Flask):
    try:
        connect(config["DB_NAME"], host="localhost", port=27017)
        print("Connected to DB successfully.")
    except Exception as exc:
        print("Error connecting to DB: ", exc)

init_mongo_client(app)


@app.route("/")
def hello():
    return {"message": "Welcome to the Flask with MongoDB tutorial!!!"}

@app.route("/users")
def get_users():
    users = User.objects()
    return bson_to_json(users)