# Подключение к базе через алхимию
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import os

load_dotenv("home/srv/Lab/RW/.env")  # Загрузка пути 

DATABASE_URL = os.getenv("DATABASE_URL")
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Проверка подключения
with engine.connect() as conn:
    print("Успешное подключение к PostgreSQL!")

# РАЗДЕЛЕНИЕ БЛОКА

# Проверка правильной базы (рудимент)
from app.database import engine
print(engine.url) 

# РАЗДЕЛЕНИЕ БЛОКА

# Тестовые данные
from app.database import SessionLocal, engine
from app.models import Client, Genre, Object

def create_test_data():
    db = SessionLocal()
    
    try:
        # Тестовый жанр
        genre = Genre(name="Fantasy", description="Magical worlds")
        db.add(genre)
        
        # Тестовый объект
        obj = Object(
            name="The Lord of the Rings",
            year=1954,
            description="Epic fantasy novel",
            genre=genre
        )
        db.add(obj)
        
        db.commit()
        print("Тестовые данные созданы!")
    except Exception as e:
        db.rollback()
        print(f"Ошибка: {e}")
    finally:
        db.close()

create_test_data()

# РАЗДЕЛЕНИЕ БЛОКА

# Тестовый клиент
from app.database import SessionLocal
from app.models import Client

def create_test_user():
    db = SessionLocal()
    try:
        # Создаем объект пользователя
        test_user = Client(
            login="test_user",
        )
        
        # Устанавливаем хеш пароля
        test_user.set_password("passTester17")
        
        db.add(test_user)
        db.commit()
        print(f"Пользователь {test_user.login} создан! ID: {test_user.id}")
        
        # Проверяем пароль
        print("Проверка пароля:", test_user.check_password("test_password123"))
        
        return test_user
    except Exception as e:
        db.rollback()
        print(f"Ошибка: {e}")
        raise
    finally:
        db.close()

# Вызываем функцию
test_user = create_test_user()
