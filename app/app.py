from flask import Flask, render_template, request, redirect, url_for
import yaml
import os

app = Flask(__name__)

# Función para cargar equipos desde los archivos YAML
def cargar_equipos():
    equipos = []
    carpeta_equipos = "app/data/equipos"
    if os.path.exists(carpeta_equipos):
        for archivo in os.listdir(carpeta_equipos):
            if archivo.endswith(".yaml"):
                with open(os.path.join(carpeta_equipos, archivo), "r") as file:
                    data = yaml.safe_load(file)
                    if data:
                        equipos.append(data)
    return equipos

# Ruta para guardar un equipo en un archivo YAML individual
def guardar_equipo(equipo):
    sysname = equipo["sysname"].replace(":", "-").replace("/", "-")
    file_path = f"app/data/equipos/{sysname}.yaml"
    with open(file_path, "w") as file:
        yaml.dump(equipo, file)

# Página principal
@app.route("/")
def index():
    return redirect(url_for("equipos"))

# Página de gestión de equipos
@app.route("/equipos")
def equipos():
    equipos = cargar_equipos()
    return render_template("equipos.html", equipos=equipos)

# Agregar un nuevo equipo
@app.route("/agregar_equipo", methods=["POST"])
def agregar_equipo():
    nuevo_equipo = {
        "sysname": request.form["sysname"],
        "nombre": request.form["nombre"],
        "ip": request.form["ip"],
        "marca": request.form["marca"],
        "modelo": request.form["modelo"],
        "localidad": request.form["localidad"],
        "protocolo": request.form["protocolo"],
        "puerto": request.form["puerto"],
        "script": request.form["script"]
    }
    guardar_equipo(nuevo_equipo)
    return redirect(url_for("equipos"))

# Eliminar un equipo (con comentario obligatorio)
@app.route("/eliminar_equipo/<sysname>", methods=["POST"])
def eliminar_equipo(sysname):
    motivo = request.form["motivo"]
    if not motivo:
        return "Debe especificar un motivo para eliminar el equipo", 400
    archivo = f"app/data/equipos/{sysname}.yaml"
    if os.path.exists(archivo):
        os.remove(archivo)
    return redirect(url_for("equipos"))

# ✅ Endpoint corregido para "Administración"
@app.route("/admin_dashboard")
def admin_dashboard():
    return "<h1>Página de Administración en Construcción</h1>"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
