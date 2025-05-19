from flask_jwt_extended import create_access_token
from app.models import Client
from app.extensions import db

def authenticate(login: str, password: str) -> str | None:
    """Аутентификация пользователя. Возвращает JWT-токен."""
    client = db.session.query(Client).filter_by(login=login).first()
    if client and client.check_password(password):
        return create_access_token(identity=str(client.id))
    return None