import os
import psycopg2
from dotenv import load_dotenv
from datetime import datetime
import numpy as np

load_dotenv()

DATABASE_URL = os.environ.get("DATABASE_URL")

def get_connection():
    # Usar PostgreSQL en producción (Railway)
    if DATABASE_URL is not None:
        return psycopg2.connect(DATABASE_URL)

def ultima_accion_empleado(id):
    conn = get_connection()
    control = conn.cursor()

    control.execute(
        "SELECT accion FROM registros WHERE empleado_id= %s",
        (id,)
    )
    last = control.fetchone()

    conn.close()
    return last

def ingreso_empleado(id):

    ultima = ultima_accion_empleado(id)
    accion = None

    if ultima is not None and ultima[0] == "Ingreso":
        accion = "Egreso"
    if ultima is not None and ultima[0] == "Egreso":
        accion = "Ingreso"
    if ultima is None:
        accion = "Ingreso"

    if accion is not None:
        conn = get_connection()
        control = conn.cursor()
    
        control.execute(
            "INSERT INTO registros (empleado_id, accion) VALUES (%s, %s)",
            (id, accion)
        )
        conn.commit()

        conn.close()
        return True
    return False

def registrar_embedding(id_empleado, embedding_lista):
    """
    Reemplaza el embedding actual de un empleado
    Recibe: embedding_lista (lista de Python desde la API)
    """
    conn = get_connection()
    control = conn.cursor()
    
    try:
        # Convertir la lista a array numpy y luego a bytes
        embedding_array = np.array(embedding_lista, dtype=np.float32)
        embedding_bytes = embedding_array.tobytes()
        
        # UPDATE para reemplazar el embedding existente
        control.execute(
            "UPDATE empleados SET embedding = %s WHERE id = %s",
            (embedding_bytes, id_empleado)  # ← Guardar los bytes
        )
        
        conn.commit()
        return True
        
    except Exception as e:
        print(f"Error al actualizar embedding: {e}")
        return False
        
    finally:
        conn.close()

def get_empleado(id):

    conn = get_connection()
    control = conn.cursor()

    control.execute("Select nombre, apellido from empleados where id= %s",(id,))

    empleado = control.fetchone()
    conn.close()
    return empleado

def obtener_todos_empleados_embeddings():
    conn = get_connection()
    c = conn.cursor()
    
    c.execute("SELECT id, embedding FROM empleados WHERE embedding IS NOT NULL")
    empleados = []
    
    for fila in c.fetchall():
        id_emp, embedding_bytes = fila
        # Convertir bytes a lista para JSON
        if embedding_bytes:
            embedding_array = np.frombuffer(embedding_bytes, dtype=np.float32)
            embedding_lista = embedding_array.tolist()
        else:
            embedding_lista = None
        
        empleados.append({
            'id': id_emp,
            'embedding': embedding_lista
        })
    
    conn.close()
    return empleados

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