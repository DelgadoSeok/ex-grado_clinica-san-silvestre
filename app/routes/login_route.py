from flask import Blueprint, request, render_template, redirect, url_for, flash, session
from services.login_service import verificar_credenciales

login_bp = Blueprint("login", __name__)

@login_bp.route("/login", methods=["GET"])
def mostrar_login():
    return render_template("shared/login.html")

@login_bp.route("/login", methods=["POST"])
def procesar_login():
    usuario = request.form.get("usuario")
    contrasena = request.form.get("contrasena")

    if not usuario or not contrasena:
        flash("Usuario y contraseña son requeridos", "danger")
        return redirect(url_for("login.mostrar_login"))

    usuario_db = verificar_credenciales(usuario, contrasena)

    if usuario_db:
        session["usuario"] = usuario_db["nombre_usuario"]
        session["rol"] = usuario_db["rol"].lower()     # Guardar el rol en la sesión

        flash("Inicio de sesión exitoso", "success")

        flash("Inicio de sesión exitoso", "success")
        return redirect(url_for("menu.mostrar_menu")) 
    else:
        flash("Credenciales incorrectas", "danger")
        return redirect(url_for("login.mostrar_login"))
