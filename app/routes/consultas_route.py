from flask import Blueprint, render_template

consultas_bp = Blueprint('consultas', __name__)

@consultas_bp.route('/consultas')
def contratos():
    return render_template('views/consultas.html')