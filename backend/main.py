from flask import Flask, render_template, request, redirect, url_for, Response
from datetime import datetime
import db
import cv2
import recognizer

app = Flask(__name__,
    template_folder="../frontend/templates",
    static_folder="../frontend/static")

# ====================== RUTAS ======================
@app.route('/')
def index():
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

# Stream de video en vivo
def generar_frames():
    face_cascade = cv2.CascadeClassifier(
        cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
    )
    cap = cv2.VideoCapture(0)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
    
    start_time = cv2.getTickCount()
    tiempo_limite = 5  # segundos

    try:
        while True:
            ret, frame = cap.read()
            if not ret:
                break

            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            faces = face_cascade.detectMultiScale(gray, 1.3, 5)
            for (x, y, w, h) in faces:
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

            ret, buffer = cv2.imencode('.jpg', frame)
            frame_bytes = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')

            # Limitar tiempo de la cámara
            tiempo_actual = (cv2.getTickCount() - start_time) / cv2.getTickFrequency()
            if tiempo_actual > tiempo_limite:
                break
    finally:
        cap.release()

@app.route('/video_feed')
def video_feed():
    return Response(generar_frames(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

def obtener_registros():
    # Conectar a la base de datos db
    conn = db.get_connection()
    c = conn.cursor()
    
    # Traer todos los registros de la tabla registros
    c.execute("SELECT id, empleado_id, accion, date FROM registros")
    registros = c.fetchall()
    conn.close()
    
    return registros 

@app.route("/registros")
def registros():
    datos = obtener_registros()
    return render_template("registros.html", registros=datos)


# ====================== RUN ======================
if __name__ == "__main__":
    app.run(debug=True)
