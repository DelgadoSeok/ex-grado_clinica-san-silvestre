from flask import Blueprint, request, render_template, redirect, url_for, flash, session
from services.login_service import verificar_credenciales

login_bp = Blueprint("login", __name__)

@login_bp.route("/login", methods=["GET"])
def mostrar_login():
    return render_template("login.html")

@login_bp.route("/login", methods=["POST"])
def procesar_login():
    usuario = request.form.get("usuario")
    contrasena = request.form.get("contrasena")

    if not usuario or not contrasena:
        flash("Usuario y contraseña son requeridos", "danger")
        return redirect(url_for("login.mostrar_login"))

    usuario_db = verificar_credenciales(usuario, contrasena)

    if usuario_db:
        session["usuario"] = usuario_db["usuario"]
        session["rol"] = usuario_db["rol"]  # Guardar el rol en la sesión

        flash("Inicio de sesión exitoso", "success")

        # Redirigir según el rol del usuario
        if usuario_db["rol"].lower() == "admin":
            return redirect(url_for("menu_admin.mostrar_menu"))  # Redirige a menu_admin
        else:
            return redirect(url_for("menu.mostrar_menu"))  # Redirige a menu normal
    else:
        flash("Credenciales incorrectas", "danger")
        return redirect(url_for("login.mostrar_login"))
