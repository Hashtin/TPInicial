from flask import Flask, render_template, request, redirect, url_for, Response
import db
import recognizer

app = Flask(__name__,
    template_folder="../frontend/templates",
    static_folder="../frontend/static")

# ====================== RUTAS ======================
@app.route('/')
def index():
    if(not(recognizer.is_active)):
        print("Recognizer inicializado")
        recognizer.init_face_recognizer()
    return render_template('index.html')

# Página temporal que abre la cámara para ingresos
@app.route('/ingreso_camera', methods=['GET', 'POST'])
def ingreso_camera():
    if request.method == 'POST':
        # Aquí se podría integrar recognizer después
        return redirect(url_for('index'))
    return render_template('ingreso_camera.html')

# Página temporal que abre la cámara para egresos
@app.route('/egreso_camera', methods=['GET', 'POST'])
def egreso_camera():
    if request.method == 'POST':
        # Aquí se podría integrar recognizer después
        return redirect(url_for('index'))
    return render_template('egreso_camera.html')

@app.route('/video_feed')
def video_feed():
    accion = request.args.get("accion")
    return Response(recognizer.generar_frames(accion),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route("/registros")
def registros():
    datos = db.obtener_registros_empleados()
    return render_template("registros.html", registros=datos)

# ====================== RUN ======================
if __name__ == "__main__":
    app.run(debug=True)
