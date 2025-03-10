from flask import Flask, jsonify
import os
from src.database import db
from src.auth import auth, revoked_tokens
from src.bookmarks import bookmarks
from flask_jwt_extended import JWTManager
from src.constants.http_status_codes import (
    HTTP_404_NOT_FOUND,
    HTTP_500_INTERNAL_SERVER_ERROR
)

def create_app(test_config=None):
    
    app = Flask(__name__, instance_relative_config=True)
    
    if test_config is None:
        app.config.from_mapping(
            SECRET_KEY=os.environ.get("SECRET_KEY"), 
            SQLALCHEMY_DATABASE_URI=os.environ.get("SQLALCHEMY_DB_URI") 
        )
    
    else:
        app.config.from_mapping(test_config)

    
    # db connect
    db.app = app
    db.init_app(app)
    
    # initialized JWT
    jwt = JWTManager(app)
    
    # Add a callback to check if a token is revoked
    @jwt.token_in_blocklist_loader
    def check_if_token_revoked(jwt_header, jwt_payload):
        jti = jwt_payload["jti"]
        return jti in revoked_tokens
    
    # blueprints
    app.register_blueprint(auth)
    app.register_blueprint(bookmarks)
    
    @app.errorhandler(HTTP_404_NOT_FOUND)
    def handle_404(e):
        return jsonify({"error" : "Not Found"}), HTTP_404_NOT_FOUND
    
    @app.errorhandler(HTTP_500_INTERNAL_SERVER_ERROR)
    def handle_500(e):
        return (
            jsonify(
                {
                    "error" : "Something went wrong on server. We are currently working on it. PLease try again in a few moments."
                }
            )
        )
        

    return app

