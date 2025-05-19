from flask import Blueprint, render_template, request, redirect, flash, session, url_for
from app.services.client import get_client, get_client_by_login, create_client
from app.services.object import get_all_objects, get_object_by_id
from app.services.collection import ( 
    get_collections_by_user, 
    create_collection, 
    add_object_to_collection, 
    get_collection_ids_with_object, 
    get_collection_by_id, 
    get_objects_in_collection, 
    remove_object_from_collection
)
from app.services.rating import (
    get_average_rating,
    get_user_rating,
    rate_object
)
import bcrypt
import os

frontend = Blueprint("frontend", __name__)

@frontend.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        login = request.form.get("login")
        password = request.form.get("password")

        if get_client_by_login(login):
            flash("Пользователь с таким логином уже существует")
            return render_template("register.html")

        try:
            create_client(login, password)
            flash("Вы успешно зарегистрированы!")
            return redirect(url_for("frontend.login"))
        except Exception:
            flash("Ошибка при регистрации")

    return render_template("register.html")

@frontend.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        login_input = request.form["login"]
        password = request.form["password"]

        import requests
        API_URL = os.getenv("API_URL", "http://localhost:5000")

        response = requests.post(f"{API_URL}/auth/login", json={
            "login": login_input,
            "password": password
        })

        if response.status_code == 200:
            data = response.json()
            session["token"] = data["access_token"]
            session["client_id"] = data["client_id"]
            session["login"] = login_input
            session.pop("guest", None)
            flash("Успешный вход!")
            return redirect(url_for("frontend.objects"))
        else:
            flash("Неверный логин или пароль")

    return render_template("login.html")

@frontend.route("/guest")
def guest():
    session.clear()
    session["guest"] = True
    flash("Вы продолжаете как гость.")
    return redirect(url_for("frontend.objects"))

@frontend.route("/logout")
def logout():
    session.clear()
    flash("Вы вышли из режима мудреца шести путей")
    return redirect(url_for("frontend.login"))

@frontend.route("/", endpoint="home")
def redirect_to_objects():
    return redirect(url_for("frontend.objects"))

@frontend.route("/objects", endpoint="objects")
def objects():
    try:
        objects = get_all_objects()
    except Exception:
        flash("Ошибка загрузки объектов")
        objects = []
    return render_template("objects.html", objects=objects)

@frontend.route("/object/<int:object_id>")
def object_detail(object_id):
    obj = get_object_by_id(object_id)
    if not obj:
        flash("Объект не найден")
        return redirect(url_for("frontend.objects"))

    user_collections = []
    existing_collection_ids = []
    user_rating = None
    avg_rating = get_average_rating(object_id)

    if "client_id" in session:
        client_id = session["client_id"]
        user_collections = get_collections_by_user(client_id)
        existing_collection_ids = get_collection_ids_with_object(client_id, object_id)
        user_rating = get_user_rating(client_id, object_id)

    return render_template(
        "object_detail.html",
        obj=obj,
        user_collections=user_collections,
        existing_collection_ids=existing_collection_ids,
        user_rating=user_rating,
        avg_rating=avg_rating
    )


@frontend.route("/collections/add", methods=["POST"])
def add_to_collection():
    if "client_id" not in session:
        flash("Только для смешариков")
        return redirect(url_for("frontend.login"))

    client_id = session["client_id"]
    object_id = request.form.get("object_id")
    collection_id = request.form.get("collection_id")
    new_collection_name = request.form.get("new_collection_name")

    if not object_id:
        flash("Объект не указан")
        return redirect(url_for("frontend.objects"))

    if collection_id:
        # Добавляем в существующую коллекцию
        add_object_to_collection(collection_id, object_id)
        flash("Добавлено в коллекцию")
    elif new_collection_name:
        # Создаём новую коллекцию и добавляем
        new_col = create_collection(client_id, new_collection_name)
        add_object_to_collection(new_col.id, object_id)
        flash("Создана новая коллекция и добавлен объект")
    else:
        flash("Не выбрана коллекция")
    
    return redirect(url_for("frontend.object_detail", object_id=object_id))

@frontend.route("/collections")
def user_collections():
    if "client_id" not in session:
        flash("Требуется авторизация")
        return redirect(url_for("frontend.login"))

    client_id = session["client_id"]
    collections = get_collections_by_user(client_id)

    return render_template("collections.html", collections=collections)

@frontend.route("/collection/<int:collection_id>")
def collection_detail(collection_id):
    if "client_id" not in session:
        flash("Требуется авторизация")
        return redirect(url_for("frontend.login"))

    collection = get_collection_by_id(collection_id)
    if not collection or collection.client_id != session["client_id"]:
        flash("Коллекция не найдена или недоступна")
        return redirect(url_for("frontend.user_collections"))

    objects = get_objects_in_collection(collection_id)
    return render_template("collection_detail.html", collection=collection, objects=objects)

@frontend.route("/collection/<int:collection_id>/remove", methods=["POST"])
def remove_from_collection(collection_id):
    if "client_id" not in session:
        flash("Требуется авторизация")
        return redirect(url_for("frontend.login"))

    object_id = request.form.get("object_id")
    collection = get_collection_by_id(collection_id)

    if not collection or collection.client_id != session["client_id"]:
        flash("Коллекция не найдена или недоступна")
        return redirect(url_for("frontend.user_collections"))

    remove_object_from_collection(collection_id, object_id)
    flash("Объект удалён из коллекции")
    return redirect(url_for("frontend.collection_detail", collection_id=collection_id))

@frontend.route("/rate", methods=["POST"])
def rate():
    if "client_id" not in session:
        flash("Требуется авторизация для оценки")
        return redirect(url_for("frontend.login"))

    client_id = session["client_id"]
    object_id = request.form.get("object_id")
    score = int(request.form.get("score", 0))

    if score < 1 or score > 10:
        flash("Оценка должна быть от 1 до 10")
        return redirect(url_for("frontend.object_detail", object_id=object_id))

    rate_object(client_id, object_id, score)
    flash("Оценка сохранена")
    return redirect(url_for("frontend.object_detail", object_id=object_id))

@frontend.route("/account")
def account():
    if not session.get("client_id") or not session.get("token"):
        flash("Требуется вход в систему")
        return redirect(url_for("frontend.login"))

    login = session.get("login", "пользователь")

    return render_template("account.html", login=login)


@frontend.route("/change-password", methods=["POST"])
def change_password():
    if "token" not in session:
        flash("Авторизуйтесь для смены пароля")
        return redirect(url_for("frontend.login"))

    old_password = request.form.get("old_password")
    new_password = request.form.get("new_password")

    if not old_password or not new_password:
        flash("Заполните все поля")
        return redirect(url_for("frontend.account"))

    import requests
    API_URL = os.getenv("API_URL", "http://localhost:5000")
    headers = {
        "Authorization": f"Bearer {session['token']}",
        "Content-Type": "application/json"
    }

    response = requests.put(f"{API_URL}/auth/password", headers=headers, json={
        "old_password": old_password,
        "new_password": new_password
    })

    if response.status_code == 200:
        flash("Пароль успешно изменён")
    else:
        try:
            msg = response.json().get("message", "Ошибка")
        except:
            msg = "Не удалось изменить пароль"
        flash(msg)

    return redirect(url_for("frontend.account"))
