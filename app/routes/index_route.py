from flask import Blueprint, render_template

index_bp = Blueprint('index', __name__)

# @app.route('/')
# def index():

#     # cursos = ['php', 'python', 'java', 'kotlin', 'dart', 'js']
#     # data = {
#     #     'titulo': 'index2025',
#     #     'bienvenida': 'saludos',
#     #     'cursos': cursos,
#     #     'numero_cursos': len(cursos)
#     # }

#     #return "Hello, world"
#     # retornar un template (archivo html dentro de /template)
#     return render_template('index.html')

@index_bp.route('/')
def index():
    return render_template('partials/login.html') # aqui estamos redireccionando directamente a login, si tuvieramos una pagina de inicio iria index