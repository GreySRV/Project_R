from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity, get_jwt
from sqlalchemy.exc import IntegrityError
from app.services.client import create_client, get_client
from app.services.auth import authenticate
from app.utils.exceptions import APIError
from app.schemas import ClientSchema
from app.extensions import db
from app.models import BlacklistedToken, Client
import bcrypt

auth_bp = Blueprint("auth", __name__)

@auth_bp.route("/register", methods=["POST"])
def register():
    data = request.get_json()

    login = data.get("login")
    password = data.get("password")

    if not login or not password:
        raise APIError("Login and password are required", 400)

    if db.session.query(Client).filter_by(login=login).first():
        raise APIError("Пользователь с таким логином уже существует", 400)

    try:
        client = Client(login=login)
        client.set_password(password)
        db.session.add(client)
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        raise APIError("Пользователь с таким логином уже существует", 400)

    return {"message": "Регистрация успешна"}, 201

@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.get_json()

    login = data.get("login")
    password = data.get("password")

    if not login or not password:
        raise APIError("Login and password required", 400)

    client = db.session.query(Client).filter_by(login=login).first()
    token = authenticate(login, password)
    if not token:
        raise APIError("Invalid credentials", 401)

    return jsonify({
        "access_token": token,
        "client_id": client.id
    })


@auth_bp.route("/me", methods=["GET"])
@jwt_required()
def get_current_user():
    client_id = int(get_jwt_identity())
    client = get_client(client_id)

    if not client:
        raise APIError("User not found", 404)

    schema = ClientSchema()
    return schema.dump(client)

@auth_bp.route("/password", methods=["PUT"])
@jwt_required()
def change_password():
    client_id = int(get_jwt_identity())
    data = request.get_json()

    old_password = data.get("old_password")
    new_password = data.get("new_password")

    if not old_password or not new_password:
        raise APIError("Old and new password are required", 400)

    client = get_client(client_id)
    if not client:
        raise APIError("User not found", 404)

    if not bcrypt.checkpw(old_password.encode(), client.password_hash.encode()):
        raise APIError("Incorrect old password", 401)

    hashed = bcrypt.hashpw(new_password.encode(), bcrypt.gensalt()).decode()
    client.password_hash = hashed
    db.session.commit()

    return {"message": "Password updated successfully"}

@auth_bp.route("/logout", methods=["POST"])
@jwt_required()
def logout():
    jwt_payload = get_jwt()
    jti = jwt_payload["jti"]
    client_id = int(get_jwt_identity())

    # Проверка: если уже в чёрном списке — ничего не делаем
    exists = db.session.query(
        db.exists().where(BlacklistedToken.jti == jti)
    ).scalar()

    if not exists:
        blacklisted = BlacklistedToken(jti=jti, client_id=client_id)
        db.session.add(blacklisted)
        db.session.commit()

    return {"message": "Successfully logged out"}