from flask import Blueprint
from .auth import auth_bp
from .objects import object_bp
from .genres import genre_bp
from .collections import collection_bp
from .ratings import rating_bp

def register_routes(app):
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(object_bp, url_prefix='/objects')
    app.register_blueprint(genre_bp, url_prefix='/genres')
    app.register_blueprint(collection_bp, url_prefix='/collections')
    app.register_blueprint(rating_bp, url_prefix='/ratings')
