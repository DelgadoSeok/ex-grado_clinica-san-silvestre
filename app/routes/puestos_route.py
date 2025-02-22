from flask import Blueprint, render_template, request, jsonify
from services.asociaciones_service import obtener_id_asociacion
from services.duenos_service import obtener_id_dueno
from services.inquilinos_service import obtener_id_inquilino
from services.gremios_service import obtener_id_gremio
from services.puestos_service import registrar_puesto,  editar_puesto, obtener_id_puesto_estado, obtener_puestos
from services.sectores_service import obtener_id_sector
puestos_bp = Blueprint('puestos', __name__, url_prefix='/puestos')

@puestos_bp.route('/', methods=['GET'])
def mostrar_puestos():
    puestos = obtener_puestos()
    return render_template('puestos.html', puestos=puestos)

@puestos_bp.route('/listar', methods=['GET'])
def listar_puestos():
    puestos = obtener_puestos()
    print(puestos)
    puestos_data = [
        {
        'id': puesto[0] if len(puesto) > 0 else None, 
        'numero': puesto[1] if len(puesto) > 1 else None,
        'asociacion': puesto[2] if len(puesto) > 2 else None,
        'gremio': puesto[3] if len(puesto) > 3 else None,
        'sector': puesto[4] if len(puesto) > 4 else None,
        'estado': puesto[5] if len(puesto) > 5 else None,
        'dueno': puesto[6] if len(puesto) > 6 else None,
        'inquilino': puesto[7] if len(puesto) > 7 else None
        }
        for puesto in puestos
    ]
    return jsonify({'puestos': puestos_data})

@puestos_bp.route('/registrar', methods=['POST'])
def registrar_nuevo_puesto():
    """API para registrar un nuevo puesto."""
    data = request.json
    resultado = registrar_puesto(
        int(data.get('numero')),
        data.get('asociacion'),
        data.get('gremio'),
        data.get('sector'),
        1,
        data.get('dueno'),
        data.get('inquilino') if data.get('inquilino') else None,
        
    )
    return jsonify(resultado)


@puestos_bp.route('/editar/<int:id>', methods=['POST'])
def actualizar_puesto(id):
    """API para actualizar datos de un puesto."""
    data = request.json

    parametros = {
        'numero': data.get('numero'),
        'asociacion_id': obtener_id_asociacion(data.get('asociacion')),
        'gremio_id': obtener_id_gremio(data.get('gremio')),
        'sector_id': obtener_id_sector(data.get('sector')),
        'puesto_estado_id': obtener_id_puesto_estado(data.get('puesto_estado')),
        'dueno_id': obtener_id_dueno(data.get('dueno')),
        'inquilino_id': obtener_id_inquilino(data.get('inquilino')) if data.get('inquilino') else None
    }

    resultado = editar_puesto(id, parametros)
    
    return jsonify(resultado)

@puestos_bp.route('/datos_selects', methods=['GET'])
def obtener_datos_selects():
    """API para obtener los datos de asociaciones, gremios, sectores, dueños e inquilinos."""
    # Obtener las listas de datos desde las funciones correspondientes
    asociaciones = obtener_id_asociacion()
    gremios = obtener_id_gremio()
    sectores = obtener_id_sector()
    duenos = obtener_id_dueno()
    inquilinos = obtener_id_inquilino()
    
    # Crear un diccionario con los datos a devolver
    data = {
        'asociaciones': asociaciones,
        'gremios': gremios,
        'sectores': sectores,
        'dueños': duenos,
        'inquilinos': inquilinos
    }

    return jsonify(data)

