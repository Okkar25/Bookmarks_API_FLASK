from flask import Flask, jsonify, redirect, request
import os
from src.database import db, Bookmark
from src.auth import auth, revoked_tokens
from src.bookmarks import bookmarks
from flask_jwt_extended import JWTManager
from src.constants.http_status_codes import (
    HTTP_404_NOT_FOUND,
    HTTP_500_INTERNAL_SERVER_ERROR
)
from flasgger import Swagger, swag_from
# swag_from enable us create yaml file to describe our spec 
from src.config.swagger import swagger_config, template
from dotenv import load_dotenv

def create_app(test_config=None):
    
    load_dotenv()
    
    app = Flask(__name__, instance_relative_config=True)
    
    if test_config is None:
        app.config.from_mapping(
            SECRET_KEY=os.environ.get("SECRET_KEY", "default_secret_key"), 
            SQLALCHEMY_DATABASE_URI=os.environ.get("SQLALCHEMY_DB_URI"),
            SQLALCHEMY_TRACK_MODIFICATIONS=False,
            JWT_SECRET_KEY=os.environ.get('JWT_SECRET_KEY', "default_jwt_secret_key"),
            
            SWAGGER = {
                "title" : "Bookmarks API",
                "uiversion" : 3
            }
        )
    
    else:
        app.config.from_mapping(test_config)


    # db connect
    db.app = app
    db.init_app(app)
    
    # initialized JWT
    jwt = JWTManager(app)
    
    # blueprints
    app.register_blueprint(auth)
    app.register_blueprint(bookmarks)
    
    #Swagger
    Swagger(app, config=swagger_config, template=template)
    
    @app.get("/api/v1/<short_url>")
    @swag_from("./docs/short_url.yaml")
    def redirect_to_url(short_url):
        bookmark = Bookmark.query.filter_by(short_url=short_url).first_or_404()
        
        if bookmark:
            bookmark.visits += 1 
            db.session.commit()
            
            # Check if it's from Swagger or Postman using a query parameter (or User-Agent)
            if request.headers.get('Accept') == 'application/json':
                # Return JSON response with original URL
                return jsonify({
                    "original_url": bookmark.url,
                    "short_url": short_url,
                    "message": "Redirect manually to the original URL."
                }), 200

            # Perform the redirect if it's not Swagger/Postman
            return redirect(bookmark.url)
 
 
    # Add a callback to check if a token is revoked
    @jwt.token_in_blocklist_loader
    def check_if_token_revoked(jwt_header, jwt_payload):
        jti = jwt_payload["jti"]
        return jti in revoked_tokens

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

