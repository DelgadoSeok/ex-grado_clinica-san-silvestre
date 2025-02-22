from flask import Blueprint, render_template, session, redirect, url_for, flash

menu_admin_bp = Blueprint("menu_admin", __name__)

@menu_admin_bp.route('/menu_admin')
def contratos():
     return render_template('menu_admin.html')

@menu_admin_bp.route("/menu_admin", methods=["GET"])
def mostrar_menu():
    if "usuario" not in session:
        flash("Por favor, inicia sesión primero", "warning")
        return redirect(url_for("login.mostrar_login"))

    if session.get("rol").lower() != "admin":
        flash("Acceso denegado: No tienes permisos de administrador", "danger")
        return redirect(url_for("menu.mostrar_menu"))  # Redirige al menú normal

    return render_template("menu_admin.html")
