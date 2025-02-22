from flask import Blueprint, render_template, request, jsonify
from services.duenos_service import ver_duenos, registrar_dueno, editar_dueno, descartar_dueno

duenos_bp = Blueprint('duenos', __name__, url_prefix='/duenos')

@duenos_bp.route('/duenos')
def contratos():
     return render_template('duenos.html')

@duenos_bp.route('/', methods=['GET'])
def mostrar_duenos():
    """Muestra la página de gestión de dueños."""
    duenos = ver_duenos()
    return render_template('duenos.html', duenos=duenos)

@duenos_bp.route('/editar', methods=['POST'])
def actualizar_dueno():
    """API para actualizar datos de un dueño."""
    data = request.json
    print("Datos recibidos para edición:", data)  # <-- Agrega esto para depuración

    resultado = editar_dueno(
        data.get("id"),
        data.get("nombres"),
        data.get("apellidos"),
        data.get("ci"),
        data.get("telf"),
        data.get("direccion")
    )
    return jsonify(resultado)


@duenos_bp.route('/registrar', methods=['POST'])
def registrar_nuevo_dueno():
    """API para registrar un nuevo dueño."""
    data = request.json
    resultado = registrar_dueno(
        data.get("nombres"),
        data.get("apellidos"),
        data.get("ci"),
        data.get("telf"),
        data.get("direccion")
    )
    return jsonify(resultado)

@duenos_bp.route('/descartar', methods=['POST'])
def descartar_nuevo_dueno():
    """API para descartar un dueño."""
    data = request.json
    print("Solicitud para descartar dueño:", data)  # Para depuración

    resultado = descartar_dueno(data.get("id"))
    return jsonify(resultado)

@duenos_bp.route('/duenos')
def duenos():
    return render_template('duenos.html') 
