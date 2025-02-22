# Iniciar Proyecto

## 1. Configuración del entorno virtual

Abrir la consola dentro de la carpeta del proyecto y ejecutar:

### Crear el entorno virtual:
```sh
python -m venv venv
```

### Activar el entorno virtual:
- **En Windows (CMD o PowerShell):**  
  ```sh
  venv\Scripts\activate
  ```
- **En Git Bash o sistemas basados en Unix (Linux/macOS):**  
  ```sh
  source venv/Scripts/activate
  ```

Si hay un error al ejecutar `activate`, habilitar la ejecución de scripts en PowerShell con:
```sh
Set-ExecutionPolicy Unrestricted -Scope Process
```

## 2. Instalación de dependencias

Dentro del entorno virtual, instalar Flask y verificar la instalación:
```sh
pip install flask
pip list
python -c "import flask; print(flask.__version__)"
```

### Librerías recomendadas:
```sh
pip install mysql-connector-python python-dotenv flask Flask-SQLAlchemy
pip install reportlab

```

## 3. Ejecutar el proyecto

Navegar a la carpeta `ExamenGrado/app` y ejecutar:
```sh
flask run
```
o
```sh
python app/app.py
```

## 4. Librerías utilizadas
- Flask
- Flask-SQLAlchemy
- MySQL Connector
- Python-Dotenv

## 5. Recomendaciones
- Usar un entorno virtual para instalar las librerías necesarias y evitar conflictos de dependencias.