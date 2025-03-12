from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
import validators 
from src.database import db, Bookmark
from src.constants.http_status_codes import (
    HTTP_400_BAD_REQUEST, 
    HTTP_409_CONFLICT,
    HTTP_201_CREATED,
    HTTP_200_OK,
    HTTP_404_NOT_FOUND
)

bookmarks = Blueprint("bookmarks", __name__, url_prefix="/api/v1/bookmarks")

@bookmarks.route("/", methods=["POST", "GET"])
@jwt_required
def handle_bookmarks():
    current_user_id = get_jwt_identity()
    
    if request.method == "POST":
        
        body = request.get_json.get("body", "")
        url = request.get_json.get("url", "")

        if not validators.url(url):
            return jsonify({
                "error" : "Please enter a valid url !"
            }), HTTP_400_BAD_REQUEST
        
        if Bookmark.query.filter_by(body=body).first():
            return jsonify({
                "error" : "This url already exists !"
            }), HTTP_409_CONFLICT
        
        bookmark = Bookmark(body=body, url=url, user_id=current_user_id)
        db.session.add(bookmark)
        db.session.commit()

        return jsonify({
            "id" : bookmark.id,
            "body" : bookmark.body,
            "url" : bookmark.url,
            "short_url" : bookmark.short_url,
            "visit" : bookmark.visits,
            "created_at" : bookmark.created_at,
            "updated_at" : bookmark.updated_at
        }), HTTP_201_CREATED
    
    else:
        page = request.args.get("page", 1, type=int)
        per_page = request.args.get("per_page", 5, type=int)
        
        bookmarks = Bookmark.query.filter_by(user_id=current_user_id).paginate(page=page, per_page=per_page)

        data = []
        
        for bookmark in bookmarks.items:
            data.append({
                "id" : bookmark.id,
                "body" : bookmark.body,
                "url" : bookmark.url,
                "short_url" : bookmark.short_url,
                "visit" : bookmark.visits,
                "created_at" : bookmark.created_at,
                "updated_at" : bookmark.updated_at
            })
        
        meta = {
            "page" : bookmarks.page,
            "pages" : bookmarks.pages,
            "total_count" : bookmarks.total,
            "prev_page" : bookmarks.prev_num,
            "next_page" : bookmarks.next_num,
            "has_prev" : bookmarks.has_prev, 
            "has_next" : bookmarks.has_next, 
        }
        
        return jsonify({
            "data" : data,
            "meta" : meta
        }), HTTP_200_OK


@bookmarks.get("/<int:id>")
@jwt_required()
def get_bookmark(id):
    current_user_id = get_jwt_identity()
    
    bookmark = Bookmark.query.filter_by(user_id=current_user_id, id=id).first()
    
    if not bookmark:
        return jsonify({"message" : "Item not found !"}), HTTP_404_NOT_FOUND
    
    return jsonify({
        "id" : bookmark.id,
        "body" : bookmark.body,
        "url" : bookmark.url,
        "short_url" : bookmark.short_url,
        "visit" : bookmark.visits,
        "created_at" : bookmark.created_at,
        "updated_at" : bookmark.updated_at
    }), HTTP_200_OK


