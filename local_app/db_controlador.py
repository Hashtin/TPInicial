import sqlite3
import numpy as np

DB_ROUTE = "local_app/database/database.db"

def init_db():
    conn = get_connection()
    c = conn.cursor()

    c.execute("DROP TABLE IF EXISTS empleados_embeddings ")
    c.execute("CREATE TABLE IF NOT EXISTS empleados_embeddings (id_empleado INTEGER PRIMARY KEY, embedding BLOB)")

    conn.commit()
    conn.close()

def actualizar_empleados(empleados):
    if not empleados:
        print("Lista de empleados vacía, no se actualiza la base de datos")
        return

    conn = get_connection()
    c = conn.cursor()

    for emp in empleados:
        # Convertir lista de vuelta a bytes para SQLite
        if emp['embedding']:
            embedding_array = np.array(emp['embedding'], dtype=np.float32)
            embedding_bytes = embedding_array.tobytes()
        else:
            embedding_bytes = None

        # Insertar o actualizar en DB local
        c.execute("""
            INSERT OR REPLACE INTO empleados_embeddings (id_empleado, embedding)
            VALUES (?, ?)
        """, (emp['id'], embedding_bytes))
    
    conn.commit()
    conn.close()

def obtener_todos_empleados():
    conn = get_connection()
    c = conn.cursor()
    
    c.execute("SELECT id_empleado, embedding FROM empleados_embeddings ")
    filas = c.fetchall()

    empleados = []
    for fila in filas:
        id_empleado, embedding_blob = fila
        embedding = np.frombuffer(embedding_blob, dtype=np.float32)  # reconstruye array
        empleados.append({
            "id": id_empleado,
            "embedding": embedding
        })

    conn.close()
    
    return empleados 

def registrar_embedding_local(id_empleado, embedding: np.ndarray):
    """
    Guarda o actualiza un embedding de empleado en SQLite
    """
    conn = get_connection()
    c = conn.cursor()
    
    # Convertir embedding a BLOB
    blob = embedding.astype(np.float32).tobytes()
    
    # Insertar o reemplazar
    c.execute("INSERT OR REPLACE INTO empleados_embeddings (id_empleado, embedding) VALUES (?, ?)", (id_empleado, blob))
    
    conn.commit()
    conn.close()

def get_connection():
    return sqlite3.connect(DB_ROUTE)