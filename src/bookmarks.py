from flask import Blueprint, jsonify

bookmarks = Blueprint("bookmarks", __name__, url_prefix="/api/v1/bookmarks")