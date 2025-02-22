from flask import Blueprint, render_template, session, redirect, url_for, flash

menu_bp = Blueprint("menu", __name__)

@menu_bp.route("/menu", methods=["GET"])
def mostrar_menu():
    if "usuario" not in session:
        flash("Por favor, inicia sesión primero", "warning")
        return redirect(url_for("login.mostrar_login"))

    return render_template("menu.html")  # Asegúrate de que este archivo existe en templates/
