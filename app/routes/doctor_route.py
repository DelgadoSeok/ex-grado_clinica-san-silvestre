from datetime import datetime
from flask import Blueprint, render_template, request, jsonify
from services.doctor_service import *

doctor_bp = Blueprint('doctor', __name__, url_prefix='/doctor')

# @doctor_bp.route('/')
# def doctor():
#      return render_template('views/doctor.html')

@doctor_bp.route('/', methods=['GET'])
def doctor():
    doctores = ver_doctores()
    especialidades = ver_especialidades()

    return render_template('views/doctor.html', doctores=doctores, especialidades=especialidades)

@doctor_bp.route('/registrar', methods=['POST'])
def registrar_nuevo_doctor():
    data = request.json
    print(data)
    resultado = registrar_persona(data)
    registrar_doctor(data, resultado['persona_id'])
    registrar_historial_doctor(resultado['persona_id'], datetime.now().date(), 'I')

    # registrar los números de teléfono
    telefonos = data.get('telefonos', [])
    for telefono in telefonos:
        registrar_telefono(resultado['persona_id'], telefono)

    # registrar especialidad/es de doctor
    especialidades = data.get('especialidades', [])
        # si no hay ninguna especialidad, el bucle no se ejecutará, por lo que no registrará nada
    for especialidad in especialidades:
        registrar_doctor_especialidad(resultado['persona_id'], especialidad)


    return jsonify(resultado)

# @duenos_bp.route('/editar', methods=['POST'])
# def actualizar_dueno():
#     """API para actualizar datos de un dueño."""
#     data = request.json
#     print("Datos recibidos para edición:", data)  # <-- Agrega esto para depuración

#     resultado = editar_dueno(
#         data.get("id"),
#         data.get("nombres"),
#         data.get("apellidos"),
#         data.get("ci"),
#         data.get("telf"),
#         data.get("direccion")
#     )
#     return jsonify(resultado)


# @duenos_bp.route('/registrar', methods=['POST'])
# def registrar_nuevo_dueno():
#     """API para registrar un nuevo dueño."""
#     data = request.json
#     resultado = registrar_dueno(
#         data.get("nombres"),
#         data.get("apellidos"),
#         data.get("ci"),
#         data.get("telf"),
#         data.get("direccion")
#     )
#     return jsonify(resultado)

# @duenos_bp.route('/descartar', methods=['POST'])
# def descartar_nuevo_dueno():
#     """API para descartar un dueño."""
#     data = request.json
#     print("Solicitud para descartar dueño:", data)  # Para depuración

#     resultado = descartar_dueno(data.get("id"))
#     return jsonify(resultado)

# @duenos_bp.route('/duenos')
# def duenos():
#     return render_template('views/duenos.html') 
