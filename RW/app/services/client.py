from app.models import Client
from app.extensions import db

def get_client(client_id: int) -> Client:
    """Получить клиента по ID."""
    return db.session.get(Client, client_id)

def get_client_by_login(login: str) -> Client | None:
    """Получить клиента по логину."""
    return db.session.query(Client).filter_by(login=login).first()

def create_client(login: str, password: str) -> Client:
    """Создать нового клиента."""
    client = Client(login=login)
    client.set_password(password)
    db.session.add(client)
    db.session.commit()
    return client

def delete_client(client_id: int) -> None:
    """Удалить клиента."""
    client = get_client(client_id)
    if client:
        db.session.delete(client)
        db.session.commit()