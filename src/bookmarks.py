from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
import validators 
from src.database import db, Bookmark
from src.constants.http_status_codes import (
    HTTP_400_BAD_REQUEST, 
    HTTP_409_CONFLICT,
    HTTP_201_CREATED,
    HTTP_200_OK,
    HTTP_404_NOT_FOUND,
    HTTP_204_NO_CONTENT 
)
from sqlalchemy import exists

bookmarks = Blueprint("bookmarks", __name__, url_prefix="/api/v1/bookmarks")

@bookmarks.route("/", methods=["POST", "GET"])
@jwt_required()
def handle_bookmarks():
    current_user_id = get_jwt_identity()
    
    if request.method == "POST":
        
        body = request.get_json().get("body", "")
        url = request.get_json().get("url", "")

        if url and not validators.url(url):
            return jsonify({
                "error" : "Please enter a valid url !"
            }), HTTP_400_BAD_REQUEST
        
        if url and Bookmark.query.filter_by(url=url).first():
            return jsonify({
                "error" : "This url already exists !"
            }), HTTP_409_CONFLICT
        
        # new method - exits 
        if db.session.query(exists().where(Bookmark.url == url)).scalar():
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


@bookmarks.delete("/<int:id>")
@jwt_required()
def delete_bookmark(id):
    current_user_id = get_jwt_identity()
    
    bookmark_to_delete = Bookmark.query.filter_by(user_id=current_user_id, id=id).first()
    
    if not bookmark_to_delete:
        return jsonify({"message" : "Item not found !"}), HTTP_404_NOT_FOUND
    
    db.session.delete(bookmark_to_delete)
    db.session.commit()
    
    return jsonify({
        "message" : "Bookmark deleted successfully."
    }) , HTTP_204_NO_CONTENT


@bookmarks.put("/<int:id>")
@bookmarks.patch("/<int:id>")
@jwt_required()
def edit_bookmark(id):
    current_user_id = get_jwt_identity()
    
    bookmark_to_edit = Bookmark.query.filter_by(user_id=current_user_id, id=id).first()

    if not bookmark_to_edit:
        return jsonify({"message" : "Item not found !"}), HTTP_404_NOT_FOUND
    
    url = request.get_json().get("url", "")
    body = request.get_json().get("body", "")

    if not validators.url(url):
        return jsonify({
            "error" : "Please enter a valid url !"
        }), HTTP_400_BAD_REQUEST
    
    if url:
        bookmark_to_edit.url = url 
    
    if bookmark_to_edit:    
        bookmark_to_edit.body = body
    
    db.session.commit() 

    return jsonify({
        "id" : bookmark_to_edit.id,
        "body" : bookmark_to_edit.body,
        "url" : bookmark_to_edit.url,
        "short_url" : bookmark_to_edit.short_url,
        "visit" : bookmark_to_edit.visits,
        "created_at" : bookmark_to_edit.created_at,
        "updated_at" : bookmark_to_edit.updated_at
    }), HTTP_200_OK


@bookmarks.get("/stats")
@jwt_required()
def get_stats():
    current_user_id = get_jwt_identity()

    data = []

    items = Bookmark.query.filter_by(user_id = current_user_id).all()

    for item in items:
        new_link = {
            "id" : item.id,
            "url" : item.url,
            "short_url" : item.short_url,
            "visits" : item.visits,
        }

        data.append(new_link)
    
    return jsonify({
        "data" : data
    }), HTTP_200_OK


