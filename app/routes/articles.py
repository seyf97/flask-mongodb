from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
import mongoengine as me
import datetime
from app.models.article import Article
from app.models.user import User
from app.db import set_fields

bp = Blueprint('articles', __name__, url_prefix = "/articles")


@bp.route("/")
@jwt_required()
def get_articles():
    user_email = get_jwt_identity()

    # Get the user
    db_user = User.objects(email=user_email).first()
    if not db_user:
        return jsonify({"message": "User not found."}), 404
    
    # Get query params for pagination
    page = request.args.get("page", default=1, type=int)
    limit = request.args.get("limit", default=10, type=int)

    if page < 1:
        return jsonify({"message": "Page has to be a positive integer."}), 404
    
    if limit < 1:
        return jsonify({"message": "Limit has to be a positive integer."}), 404

    start = (page - 1)*limit

    articles = Article.objects[start:(start + limit)].order_by("title")
    
    article_list = [article.to_dict() for article in articles]

    total_articles = Article.objects.count()
    num_articles = len(article_list)


    return jsonify({
        "page": page,
        "limit": limit,
        "num_articles": num_articles,
        "total_articles": total_articles,
        "articles": article_list
    }), 200



@bp.route("/", methods=["POST"])
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



@bp.route("/<string:blogpost_id>")
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



@bp.route("/<string:blogpost_id>", methods=["DELETE"])
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



@bp.route("/<string:blogpost_id>", methods=["PUT"])
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
    
    # Check if the user is the author:
    if str(article.author.pk) != str(db_user.pk):
        return jsonify({"message": "Only authors can edit articles."}), 405

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

    
