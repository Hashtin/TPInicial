import sqlite3

DB_ROUTE = "database/database.db"

def init_db():
    conn = get_connection()
    c = conn.cursor()
    
    # Creamos la tabla empleados, donde asignamos nombres y apellidos y un id para diferenciar.
    c.execute('''CREATE TABLE IF NOT EXISTS empleados
                 (id INTEGER PRIMARY KEY, nombre TEXT, apellido TEXT)''')
    
    # Creamos tabla registros, donde guardaremos ingresos e egresos con timestamp.
    c.execute('''CREATE TABLE IF NOT EXISTS registros
                 (id INTEGER PRIMARY KEY, empleado_id INTEGER, accion TEXT, timestamp TEXT)''')
    
    # Empleados = equipo de trabajo de prueba
    empleados = [
        (0, 'Luis', 'Alcarraz'),
        (1, 'Augusto', 'Fuertes'),
        (2, 'Martin', 'Ojeda'),
        (3, 'Francisco', 'San Martin')
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

def get_connection():
    return sqlite3.connect(DB_ROUTE)

def registrar_evento(nombre, apellido):
    conn = get_connection()
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