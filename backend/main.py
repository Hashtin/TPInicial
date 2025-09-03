from flask import Flask, render_template, request, redirect, url_for, Response
import db
import recognizer

app = Flask(__name__,
    template_folder="../frontend/templates",
    static_folder="../frontend/static")

# ====================== RUTAS ======================
@app.route('/')
def index():
    recognizer.reset()
    if(not(recognizer.is_active)):
        print("Recognizer inicializado")
        recognizer.init_face_recognizer()
    return render_template('index.html')

# Página temporal que abre la cámara para ingresos
@app.route('/ingreso_camera', methods=['GET', 'POST'])
def ingreso_camera():
    if request.method == 'POST':
        recognizer.reset()
        return redirect(url_for('index'))
    return render_template('ingreso_camera.html')

# Página temporal que abre la cámara para egresos
@app.route('/egreso_camera', methods=['GET', 'POST'])
def egreso_camera():
    if request.method == 'POST':
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

@app.route('/confirmar', methods=['POST'])
def confirmar():
    accion = request.args.get("accion")  
    detected = recognizer.detected
    mensaje = "ERROR: No se logró reconocer el empleado"
    if detected:
        if accion == "Ingreso" and db.ingreso_empleado(recognizer.id_empleado):
            empleado = db.get_empleado(recognizer.id_empleado)
            mensaje = f"INGRESO REGISTRADO: {empleado[0]} {empleado[1]}" 
            recognizer.reset()
            return render_template("resultado.html", mensaje=mensaje)
        
        elif accion == "Egreso" and db.egreso_empleado(recognizer.id_empleado):
            empleado = db.get_empleado(recognizer.id_empleado)
            mensaje = f"EGRESO REGISTRADO: {empleado[0]} {empleado[1]}" 
            recognizer.reset()
            return render_template("resultado.html", mensaje=mensaje)
        
        else:
            empleado = db.get_empleado(recognizer.id_empleado)
            mensaje = f"ERROR: {empleado[0]} {empleado[1]}, ya realizó la accion = {accion}"
            recognizer.reset() 
            return render_template("resultado.html", mensaje=mensaje)
            
    return render_template("resultado.html", mensaje=mensaje)

@app.route('/volver', methods=['POST'])
def volver():
    recognizer.reset()
    return redirect(url_for('index'))  # redirige de vuelta a inicio, por ejemplo

# ====================== RUN ======================
if __name__ == "__main__":
    app.run(debug=True)
