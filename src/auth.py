from flask import Blueprint, jsonify, request
from werkzeug.security import generate_password_hash, check_password_hash
from src.constants.http_status_codes import (
    HTTP_400_BAD_REQUEST, 
    HTTP_409_CONFLICT, 
    HTTP_201_CREATED, 
    HTTP_401_UNAUTHORIZED, 
    HTTP_200_OK
)
import re
import validators
from src.database import db, User
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    jwt_required,
    get_jwt_identity,
    get_jti,
    get_jwt
)

auth = Blueprint("auth", __name__, url_prefix="/api/v1/auth")

# @auth.route("/register", methods=["POST", "GET"])
@auth.post("/register")
def register():
    username = request.json["username"] # request.form.get()
    email = request.json["email"]
    password = request.json["password"]
    # email = request.json.get("email", "")
    # password = request.json.get("password", "")
    
    # data validation 
    if len(password) < 6:
        return (
            jsonify({"error" : "Password must be longer than 6 characters."}), 
            HTTP_400_BAD_REQUEST
        )
    
    if not re.search(r'[A-Za-z]', password) or not re.search(r'[0-9]', password) or not re.search(r'[@$!%*?&#^]', password):
         return (
            jsonify({"error" : "Password must contain at least one alphabet, a number and a special character."}), 
            HTTP_400_BAD_REQUEST
        )
    
    if len(username) < 3:
         return (
            jsonify({"error" : "Username must be longer than 3 characters."}), 
            HTTP_400_BAD_REQUEST
        )
    
    if not username.isalnum() or " " in username:
        return (
            jsonify({"error" : "Username should be alphanumeric with no spaces."}), 
            HTTP_400_BAD_REQUEST
        )
    
    # use validators package
    if not validators.email(email):
        return (
            jsonify({"error" : "You must enter a valid email address."}), 
            HTTP_400_BAD_REQUEST
        )
    
    if User.query.filter_by(username=username).first() is not None:
        return jsonify({"error" : "This username is already taken. Please choose a different one."}), HTTP_409_CONFLICT
    
    if User.query.filter_by(email=email).first() is not None:
        return jsonify({"error" : "This email is already taken. Please choose a different one."}), HTTP_409_CONFLICT
    
    pwd_hash = generate_password_hash(password)
    
    user = User(username=username, email=email, password=pwd_hash)
    db.session.add(user)
    db.session.commit()
    
    return(
        jsonify(
            {"message" : "User created", "user" : {"username" : username , "email" : email}}
        ),
        HTTP_201_CREATED
    )

@auth.post("login")
def login():
    email = request.json.get("email", "")
    password = request.json.get("password", "")
    
    user = User.query.filter_by(email=email).first()
        
    if user:
        is_correct_pwd = check_password_hash(user.password, password)
        
        if is_correct_pwd:
            # identity needs to be string # str(user.id) # get_jwt_identity()
            access = create_access_token(identity=str(user.id))
            refresh = create_refresh_token(identity=str(user.id))
            
            return (
                jsonify(
                    {
                        "user" : {
                            "refresh" : refresh,
                            "access" : access,
                            "email" : user.email,
                            "username" : user.username
                        }
                    }
                ),
                HTTP_200_OK
            )
    
    
    return jsonify({"error" : "Wrong Credentials"}), HTTP_401_UNAUTHORIZED

@auth.get("/user")
@jwt_required()
def user():
    user_id = get_jwt_identity()
    user = User.query.filter_by(id=user_id).first()
    
    if user:
        return (
            jsonify(
                {
                    "username" : user.username,
                    "email" : user.email
                }
            ),
            HTTP_200_OK
        )
    
    return jsonify({"error" : "User not found"}), HTTP_400_BAD_REQUEST

