from flask import Blueprint, render_template, request, redirect, flash, session, url_for
from app.services.client import get_client, get_client_by_login, create_client
from app.services.object import get_all_objects, get_object_by_id
import bcrypt

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
        login = request.form["login"]
        password = request.form["password"]

        client = get_client_by_login(login)
        if client and bcrypt.checkpw(password.encode(), client.password_hash.encode()):
            session["client_id"] = client.id
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
    return render_template("object_detail.html", obj=obj)
