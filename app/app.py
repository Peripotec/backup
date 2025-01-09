# app/app.py
from flask import Flask, render_template, request, redirect, url_for
import yaml

app = Flask(__name__)

# Ruta para cargar los equipos desde el archivo YAML
def cargar_equipos():
    try:
        with open("app/data/equipos.yaml", "r") as file:
            data = yaml.safe_load(file)
            return data.get("equipos", [])
    except FileNotFoundError:
        return []

# Ruta para guardar los equipos en el archivo YAML
def guardar_equipos(equipos):
    with open("app/data/equipos.yaml", "w") as file:
        yaml.dump({"equipos": equipos}, file)

# Página principal con redirección a la gestión de equipos
@app.route("/")
def index():
    return redirect(url_for("equipos"))

# Página principal con el formulario y lista de equipos
@app.route("/equipos")
def equipos():
    equipos = cargar_equipos()
    return render_template("equipos.html", equipos=equipos)

# Agregar un equipo al archivo YAML
@app.route("/agregar_equipo", methods=["POST"])
def agregar_equipo():
    equipos = cargar_equipos()
    nuevo_equipo = {
        "nombre": request.form["nombre"],
        "ip": request.form["ip"],
        "marca": request.form["marca"],
        "modelo": request.form["modelo"]
    }
    equipos.append(nuevo_equipo)
    guardar_equipos(equipos)
    return redirect(url_for("equipos"))

# Eliminar un equipo
@app.route("/eliminar_equipo/<int:index>")
def eliminar_equipo(index):
    equipos = cargar_equipos()
    if 0 <= index < len(equipos):
        del equipos[index]
        guardar_equipos(equipos)
    return redirect(url_for("equipos"))

# NUEVO: Definir una ruta de administración para evitar errores
@app.route("/admin_dashboard")
def admin_dashboard():
    return "<h1>Panel de Administración en Construcción</h1>"

# Punto de entrada del servidor Flask
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
