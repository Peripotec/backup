# app/app.py
from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/admin")
def admin_dashboard():
    return "<h2>Panel de Administración</h2>"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
