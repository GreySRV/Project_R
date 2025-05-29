from flask import Flask
from .config import Config
from .extensions import db, ma, jwt
from .routes import register_routes
from flask_jwt_extended import JWTManager
from app.models import BlacklistedToken
from flask_jwt_extended import get_jwt
from app.extensions import db
from app.routes.frontend import frontend
from flask_migrate import Migrate
import os

migrate = Migrate()

def create_app():
    app = Flask(
        __name__,
        template_folder="../templates",  # Указываем путь вручную
        static_folder="../static"
    )
    app.config.from_object(Config)

    db.init_app(app)
    migrate.init_app(app, db)
    ma.init_app(app)
    jwt.init_app(app)

    @jwt.token_in_blocklist_loader
    def check_if_token_revoked(jwt_header, jwt_payload):
        jti = jwt_payload["jti"]
        return db.session.query(
            db.exists().where(BlacklistedToken.jti == jti)
        ).scalar()

    app.secret_key = os.getenv("SECRET_KEY", "dev-secret")  # нужен для flash и session
    register_routes(app)  # Регистрирация маршрутов
    app.register_blueprint(frontend)
    
    return app
