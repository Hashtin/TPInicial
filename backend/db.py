from datetime import datetime
import sqlite3

DB_ROUTE = "database/database.db"

def init_db():
    conn = get_connection()
    c = conn.cursor()

    # Creamos la tabla empleados, donde asignamos nombres y apellidos y un id para diferenciar.
    c.execute('''CREATE TABLE IF NOT EXISTS empleados
                 (id INTEGER PRIMARY KEY, nombre TEXT, apellido TEXT)''')
    
    # Creamos tabla registros, donde guardaremos ingresos e egresos con timestamp.
    c.execute("CREATE TABLE IF NOT EXISTS registros (id INTEGER PRIMARY KEY,empleado_id INTEGER,accion TEXT,date TIMESTAMP, FOREIGN KEY (empleado_id) REFERENCES empleados(id));")
    
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
    timestamp = datetime.now()

    for emp in empleados:
        emp_id = emp[0]
    # Comprobar si ya tiene un registro (para no duplicar al reiniciar)
        c.execute("SELECT * FROM registros WHERE empleado_id=? AND accion='Ingreso'", (emp_id,))
        if not c.fetchone():
            timestamp = datetime.now()
            c.execute("INSERT INTO registros (empleado_id, accion, date) VALUES (?,?,?)",
                  (emp_id, "Ingreso", timestamp))
    conn.commit()
    conn.close()

def get_connection():
    return sqlite3.connect(DB_ROUTE)

def ultima_accion_empleado(id):
    conn = get_connection()
    control = conn.cursor()

    control.execute(
        "SELECT accion FROM registros WHERE empleado_id=? ORDER BY id DESC LIMIT 1",
        (id,)
    )
    last = control.fetchone()

    conn.close()
    return last

def ingreso_empleado(id):
    ultima = ultima_accion_empleado(id)

    if ultima is not None and ultima[0] == "Ingreso":
        return False
    else:
        conn = get_connection()
        control = conn.cursor()

        timestamp = datetime.now()
        accion = "Ingreso"

        control.execute(
            "INSERT INTO registros (empleado_id, accion, date) VALUES (?,?,?)",
            (id, accion, timestamp)
        )
        conn.commit()

        conn.close()
        return True

def egreso_empleado(id):

    ultima = ultima_accion_empleado(id)

    if ultima is not None and ultima[0] == "Egreso":
        return False
    
    conn = get_connection()
    control = conn.cursor()

    timestamp = datetime.now()
    accion = "Egreso"

    control.execute(
        "INSERT INTO registros (empleado_id, accion, date) VALUES (?,?,?)",
        (id, accion, timestamp)
    )
    conn.commit()

    conn.close()
    return True

def get_empleado(id):

    conn = get_connection()
    control = conn.cursor()

    control.execute("Select nombre, apellido from empleados where id=?",(id,))

    empleado = control.fetchone()
    conn.close()
    return empleado

def obtener_registros():
    # Conectar a la base de datos db
    conn = get_connection()
    c = conn.cursor()
    
    # Traer todos los registros de la tabla registros
    c.execute("SELECT id, empleado_id, accion, date FROM registros ORDER BY date DESC")
    registros = c.fetchall()
    conn.close()
    
    return registros 

def obtener_registros_empleados():
    # Conectar a la base de datos db
    conn = get_connection()
    c = conn.cursor()
    
    # Traer todos los registros de la tabla registros
    c.execute("SELECT r.id, e.nombre, e.apellido, r.accion, r.date FROM registros r, empleados e where r.empleado_id = e.id ORDER BY date DESC")
    registros = c.fetchall()
    conn.close()
    
    return registros 