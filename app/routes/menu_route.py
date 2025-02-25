from flask import Blueprint, render_template, session, redirect, url_for, flash

menu_bp = Blueprint("menu", __name__)

@menu_bp.route("/menu", methods=["GET"])
def mostrar_menu():
    if "usuario" not in session:
        flash("Por favor, inicia sesión primero", "warning")
        return redirect(url_for("login.mostrar_login"))
    
    rol = session.get("rol").lower()

    # Aquí pasamos el rol a la plantilla, para que el menú se construya dinámicamente
    # Tomar en cuenta que es mejor colocar el nombre completo al rol, para evitar volver a escribir y que directamente me muestre el rol como nombre
    if rol == "admin":
        return render_template("shared/menu.html", rol="admin")  # Si es admin, pasamos 'admin' a la plantilla
    elif rol == "secretaria":
        return render_template("shared/menu.html", rol="secretaria")  # Si es secretario, pasamos 'secretario'
    else:
        flash("Acceso denegado: No tienes permisos de administrador o secretaria", "danger")
        return redirect(url_for("login.mostrar_login"))
