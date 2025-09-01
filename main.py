from flask import Flask, render_template, request, redirect, url_for
import cv2
import sqlite3
from datetime import datetime
import time
import threading

app = Flask(__name__)

def init_db():
    conn = sqlite3.connect("database.db")
    c = conn.cursor()
    
    # Creamos la tabla empleados, donde asignamos nombres y apellidos y un id para diferenciar.
    c.execute('''CREATE TABLE IF NOT EXISTS empleados
                 (id INTEGER PRIMARY KEY, nombre TEXT, apellido TEXT)''')
    
    # Creamos tabla registros, donde guardaremos ingresos e egresos con timestamp.
    c.execute('''CREATE TABLE IF NOT EXISTS registros
                 (id INTEGER PRIMARY KEY, empleado_id INTEGER, accion TEXT, timestamp TEXT)''')
    
    # Empleados = equipo de trabajo de prueba
    empleados = [
        (1, 'Luis', 'Alcarraz'),
        (2, 'Augusto', 'Fuertes'),
        (3, 'Martin', 'Ojeda'),
        (4, 'Francisco', 'San Martin')
    ]
    
    # Insertamos los datos
    for emp in empleados:
        c.execute("INSERT OR IGNORE INTO empleados (id, nombre, apellido) VALUES (?,?,?)", emp)
    
    # Registrar ingreso actual para cada uno
    from datetime import datetime
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    for emp in empleados:
        emp_id = emp[0]
    # Comprobar si ya tiene un registro (para no duplicar al reiniciar)
        c.execute("SELECT * FROM registros WHERE empleado_id=? AND accion='Ingreso'", (emp_id,))
        if not c.fetchone():
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            c.execute("INSERT INTO registros (empleado_id, accion, timestamp) VALUES (?,?,?)",
                  (emp_id, "Ingreso", timestamp))
    conn.commit()
    conn.close()
init_db()

# ====================== FUNCIONES ======================

def registrar_evento(nombre, apellido):
    conn = sqlite3.connect("database.db")
    c = conn.cursor()
    # Buscar id del empleado
    c.execute("SELECT id FROM empleados WHERE nombre=? AND apellido=?", (nombre, apellido))
    emp = c.fetchone()
    if emp:
        emp_id = emp[0]
        # Obtener último registro
        c.execute("SELECT accion FROM registros WHERE empleado_id=? ORDER BY id DESC LIMIT 1", (emp_id,))
        last = c.fetchone()
        if last is None or last[0] == "Egreso":
            accion = "Ingreso"
        else:
            accion = "Egreso"
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        c.execute("INSERT INTO registros (empleado_id, accion, timestamp) VALUES (?,?,?)",
                  (emp_id, accion, timestamp))
        conn.commit()
        print(f"{accion} correcto: {nombre} {apellido} a las {timestamp}")
    conn.close()


def abrir_camara(nombre, apellido):
    """Abre la cámara con OpenCV, detecta rostro, espera 5s y guarda ingreso."""
    cap = cv2.VideoCapture(0)
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

    deteccion_confirmada = False
    tiempo_inicio = None

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, 1.3, 5)

        # Dibujar rectángulos sobre rostros detectados
        for (x, y, w, h) in faces:
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

        # Mensaje sobre la imagen
        cv2.putText(frame, "Detectando Reconocimiento Facial...", (10,30),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0,255,0), 2)

        cv2.imshow("Cámara", frame)

        # Lógica de confirmación
        if len(faces) > 0:
            if not deteccion_confirmada:
                deteccion_confirmada = True
                tiempo_inicio = time.time()
            elif time.time() - tiempo_inicio >= 5:
                registrar_evento(nombre, apellido)
                print(f"Ingreso correcto: {nombre} {apellido}")
                time.sleep(3)  # esperar 3s para mostrar mensaje
                break
        else:
            deteccion_confirmada = False  # Reset si no detecta

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

# ====================== RUTAS ======================
@app.route('/')
def index():
    # Obtener registros
    conn = sqlite3.connect("database.db")
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
    thread = threading.Thread(target=abrir_camara, args=(nombre, apellido))
    thread.start()

    # Mientras tanto, volver al menú principal
    return redirect(url_for('index'))

@app.route('/registros')
def registros():
    return render_template('registros.html')

# ====================== RUN ======================
if __name__ == "__main__":
    app.run(debug=True)
