from flask import Flask, render_template, request, redirect, url_for, Response
import db

app = Flask(__name__,
    template_folder="../frontend/templates",
    static_folder="../frontend/static")

# ====================== RUTAS ======================
@app.route('/')
def index():
    return render_template('index.html')

@app.route("/registros")
def registros():
    datos = db.obtener_registros_empleados()
    return render_template("registros.html", registros=datos)

@app.route('/volver', methods=['POST'])
def volver():
    return redirect(url_for('index'))  # redirige de vuelta a inicio, por ejemplo

# ====================== RUN ======================
if __name__ == "__main__":
    app.run(debug=True)
