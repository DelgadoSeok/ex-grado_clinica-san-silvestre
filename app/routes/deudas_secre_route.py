from flask import Blueprint, render_template

deudas_secre_bp = Blueprint('deudas_secre', __name__)

@deudas_secre_bp.route('/deudas_secre')
def contratos():
    return render_template('views/deudas_secre.html')
