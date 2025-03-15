from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import string
import random

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username=db.Column(db.String(80), nullable=False, unique=True)
    email=db.Column(db.String(120), nullable=False, unique=True)
    password=db.Column(db.Text(), nullable=False)
    created_at=db.Column(db.DateTime, default=datetime.now())
    updated_at=db.Column(db.DateTime, onupdate=datetime.now())
    bookmarks=db.relationship("Bookmark", backref="user", lazy=True)
    
    def __repr__(self) -> str:
        return f"User >>> {self.username}"

class Bookmark(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.Text, nullable=True)
    url = db.Column(db.Text, nullable=False)
    short_url = db.Column(db.String(6), nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id") )
    created_at = db.Column(db.DateTime, default = datetime.now())
    updated_at = db.Column(db.DateTime, onupdate = datetime.now())
    visits = db.Column(db.Integer, default=0)
    
    def generate_short_characters(self):
        characters = string.digits + string.ascii_letters
        SHORT_URL_LENGTH = 6
        
        while True:
            picked_chars = "".join(random.choices(characters, k = SHORT_URL_LENGTH))
            
            if not self.query.filter_by(short_url=picked_chars).first():
                return picked_chars
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        if not self.short_url:
            self.short_url = self.generate_short_characters()
            
    def __repr__(self) -> str:
        return f"Bookmark >>> {self.url}"

