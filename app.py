from app import create_app
from app.extensions import db

app = create_app()

# Проверка подключения к БД (выполняется при запуске)
with app.app_context():
    try:
        engine = db.engine  # Получить SQLAlchemy engine
        with engine.connect() as conn:
            print("Успешное подключение к PostgreSQL!")
            print(engine.url)

    except Exception as e:
        print(f"Ошибка подключения: {e}")

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
