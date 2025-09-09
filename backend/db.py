import os
import psycopg2
from datetime import datetime

DATABASE_URL = os.environ.get("DATABASE_URL")

def get_connection():
    # Usar PostgreSQL en producción (Railway)
    if DATABASE_URL is not None:
        return psycopg2.connect(DATABASE_URL)

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