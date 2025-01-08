from flask import Blueprint, jsonify

errors = Blueprint("errors", __name__)

# We don't wanna see html pages for 404 errors
@errors.app_errorhandler(404)
def page_not_found(e):
    return jsonify({"message": "The requested URL was not found on the server."}), 404
