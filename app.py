from flask import Flask, request, jsonify
from flask_jwt_extended import JWTManager, create_access_token, get_jwt_identity, jwt_required
import mongoengine as me
import datetime
from dotenv import dotenv_values
from model import User, Article
from utils import salt_hash_password, verify_password, set_fields


config = dotenv_values(".env")
app = Flask(__name__)

app.config['SECRET_KEY'] = "Screw you guys, i'm going home. I'm sorry I thought this was America. I didn't hear no bell." 
app.config["JWT_SECRET_KEY"] = '2d0d57c165e26cc4f75a128a398a2a3f'
app.config['JWT_TOKEN_LOCATION'] = ['headers']
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = datetime.timedelta(seconds=3600)
app.config["JWT_ERROR_MESSAGE_KEY"] = "message"  # I just don't like the default "msg" key


jwt = JWTManager(app)


# We don't wanna see html pages for 404 errors
@app.errorhandler(404)
def page_not_found(e):
    return jsonify({"message": "The requested URL was not found on the server."}), 404

# Initialize the mongo client for testing 
def init_mongo_client(app: Flask):
    try:
        me.connect(config["DB_NAME"], host="localhost", port=27017)
        print("Connected to DB successfully.")
    except Exception as exc:
        print("Error connecting to DB: ", exc)

init_mongo_client(app)


@app.route("/")
def home():
    return {"message": "Welcome to the Flask with MongoDB tutorial!!!"}


@app.route("/users")
@jwt_required()
def get_users():

    users = [user.to_dict() for user in User.objects]
    # users = [user.to_dict() for user in User.objects]

    return jsonify(users), 200


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

@app.route("/login", methods=["POST"])
def login():

    article_info = request.get_json(force=True, silent=True, cache=False)

    # Check if the JSON body is valid
    if article_info is None:
        return jsonify({"message": "Invalid JSON body."}), 400
    
    # Check the fields
    email = article_info.get("email")
    password = article_info.get("password")

    if not email or not password:
        return jsonify({"message": "email and password are required."}), 400
    
    if len(article_info.keys()) > 2:
        return jsonify({"message": "Only email and password fields are allowed."}), 400
    
    # Check if the required fields are present
    # Technically should work since the prev checks should have caught this
    try:
        user = User(**article_info)
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


@app.route("/articles")
@jwt_required()
def get_articles():
    user_email = get_jwt_identity()

    # Get the user
    db_user = User.objects(email=user_email).first()
    if not db_user:
        return jsonify({"message": "User not found."}), 404
    
    print(Article.objects.count())
    
    articles = [article.to_dict() for article in Article.objects]
        
    return jsonify({"Articles": articles}), 200


@app.route("/article/<string:blogpost_id>")
@jwt_required()
def get_article(blogpost_id: str):
    user_email = get_jwt_identity()

    # Get the user
    db_user = User.objects(email=user_email).first()
    if not db_user:
        return jsonify({"message": "User not found."}), 404
    
    # Get the article
    try:
        article = Article.objects(pk=blogpost_id).first()
        print(article)
    except me.errors.ValidationError as exc:
        print(exc)
        return jsonify({"message": f"Invalid Article ID. {exc}"}), 400

    # Valid Article ID but doesn't exist
    if not article:
        return jsonify({"message": "Article not found."}), 404
    
        
    return jsonify({"Article": article.to_dict()}), 200


@app.route("/articles", methods=["POST"])
@jwt_required()
def post_article():
    article_info = request.get_json(force=True, silent=True, cache=False)

    # Check if the JSON body is valid
    if article_info is None:
        return jsonify({"message": "Invalid JSON body."}), 400

    user_email = get_jwt_identity()

    # Get the user
    db_user = User.objects(email=user_email).first()
    if not db_user:
        return jsonify({"message": "User not found."}), 404
    
    article = Article(**article_info)
    article.author = db_user
    article.last_edited = None

    try:
        article.save()
    except me.errors.ValidationError as exc:
        return jsonify({"message": str(exc)}), 400

    return jsonify({"message": "Posted article successfully."}), 201



@app.route("/articles/<string:blogpost_id>", methods=["DELETE"])
@jwt_required()
def delete_article(blogpost_id: str):
    user_email = get_jwt_identity()

    # Get the user
    db_user = User.objects(email=user_email).first()
    if not db_user:
        return jsonify({"message": "User not found."}), 404
    
    # Get the article
    try:
        article = Article.objects(pk=blogpost_id).first()
        print(article)
    except me.errors.ValidationError as exc:
        print(exc)
        return jsonify({"message": f"Invalid Article ID. {exc}"}), 400

    # Valid Article ID but doesn't exist
    if not article:
        return jsonify({"message": "Article not found."}), 404
    
    # Delete the article
    article.delete()

    return jsonify({"message": f"Article {blogpost_id} deleted successfully."}), 200



@app.route("/articles/<string:blogpost_id>", methods=["PUT"])
@jwt_required()
def update_article(blogpost_id: str):

    # Check if the JSON body is valid
    article_info = request.get_json(force=True, silent=True, cache=False)
    if article_info is None:
        return jsonify({"message": "Invalid JSON body."}), 400

    user_email = get_jwt_identity()

    # Get the user
    db_user = User.objects(email=user_email).first()
    if not db_user:
        return jsonify({"message": "User not found."}), 404
    
    # Get the article
    try:
        article = Article.objects(pk=blogpost_id).first()
        print(article)
    except me.errors.ValidationError as exc:
        print(exc)
        return jsonify({"message": f"Invalid Article ID. {exc}"}), 400

    # Valid Article ID but doesn't exist
    if not article:
        return jsonify({"message": "Article not found."}), 404

    # Update article
    exclude_fields = ["last_edited", "created_at", "author"]
    try:
        article = set_fields(article, article_info, exclude_fields)
    except me.errors.FieldDoesNotExist as exc:
        return jsonify({"message": str(exc)}), 400

    # Update the last edited time
    article.last_edited = datetime.datetime.now(datetime.UTC)

    # Save article
    try:
        article.save()
    except me.errors.ValidationError as exc:
        return jsonify({"message": str(exc)}), 400

    return jsonify({"message": "Article updated successfully"}), 200

    
