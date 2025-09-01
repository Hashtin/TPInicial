from flask import Flask, render_template, request, redirect, url_for
from datetime import datetime
import threading
import db
import recognizer

app = Flask(__name__,
    template_folder="../frontend/templates",
    static_folder="../frontend/static")

## Inicializa base de datos 
db.init_db()

# ====================== RUTAS ======================
@app.route('/')
def index():
    # Obtener registros
    conn = db.get_connection()
    c = conn.cursor()
    c.execute('''SELECT empleados.nombre, empleados.apellido, registros.accion, registros.timestamp
                 FROM registros
                 JOIN empleados ON registros.empleado_id = empleados.id
                 ORDER BY registros.id DESC''')
    data = c.fetchall()
    conn.close()
    return render_template('index.html', registros=data)

@app.route('/ingreso', methods=['POST'])
def ingreso():
    nombre = request.form['nombre']
    apellido = request.form['apellido']

    # Abrir cámara en hilo aparte para no bloquear Flask
    thread = threading.Thread(target=recognizer.abrir_camara, args=(nombre, apellido))
    thread.start()

    # Mientras tanto, volver al menú principal
    return redirect(url_for('index'))

@app.route('/registros')
def registros():
    return render_template('registros.html')

# ====================== RUN ======================
if __name__ == "__main__":
    app.run(debug=True)
