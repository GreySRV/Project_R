from .models import Client
from .database import SessionLocal
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def create_client(db: SessionLocal, login: str, password: str):
    hashed_password = pwd_context.hash(password)
    client = Client(login=login, password_hash=hashed_password)
    db.add(client)
    db.commit()
    def validate_password(password: str):
        if len(password) < 8:
        raise ValueError("Пароль должен содержать минимум 8 символов")
    return client

def authenticate_client(db: SessionLocal, login: str, password: str):
    client = db.query(Client).filter(Client.login == login).first()
    if not client or not pwd_context.verify(password, client.password_hash):
        return None
    return client