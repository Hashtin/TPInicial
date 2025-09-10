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
        "SELECT accion FROM registros WHERE empleado_id= %s order by date desc limit 1",
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

# db.py - Funciones adicionales para análisis (en prueba)
def obtener_datos_analisis_productividad():
    """
    Obtiene todos los datos necesarios para el dashboard de análisis productivo
    """
    conn = get_connection()
    try:
        query = """
        SELECT 
            p.id as producto_id,
            p.nombre as producto_nombre,
            pr.fecha,
            pr.eficacia,
            pr.eficiencia, 
            pr.efectividad,
            pr.ganancia_bruta,
            pr.cantidad_producida,
            pr.materia_prima_utilizada,
            DATE_TRUNC('month', pr.fecha) as mes
        FROM producciones pr
        JOIN productos p ON pr.id_producto = p.id
        ORDER BY pr.fecha
        """
        
        with conn.cursor() as cursor:
            cursor.execute(query)
            resultados = cursor.fetchall()
            
        # Convertir a lista de diccionarios
        datos = []
        for row in resultados:
            datos.append({
                'producto_id': row[0],
                'producto_nombre': row[1],
                'fecha': row[2],
                'eficacia': float(row[3]) if row[3] else 0,
                'eficiencia': float(row[4]) if row[4] else 0,
                'efectividad': float(row[5]) if row[5] else 0,
                'ganancia_bruta': float(row[6]) if row[6] else 0,
                'cantidad_producida': float(row[7]) if row[7] else 0,
                'materia_prima_utilizada': float(row[8]) if row[8] else 0,
                'mes': row[9]
            })
            
        return datos
        
    except Exception as e:
        print(f"Error en obtener_datos_analisis_productividad: {e}")
        return []
    finally:
        conn.close()

def obtener_metricas_generales():
    """
    Obtiene métricas generales para el resumen del dashboard
    """
    conn = get_connection()
    try:
        query = """
        SELECT 
            COUNT(DISTINCT id_producto) as total_productos,
            COUNT(*) as total_producciones,
            SUM(ganancia_bruta) as ganancia_total,
            AVG(efectividad) as efectividad_promedio,
            AVG(eficiencia) as eficiencia_promedio,
            SUM(cantidad_producida) as produccion_total
        FROM producciones
        """
        
        with conn.cursor() as cursor:
            cursor.execute(query)
            resultado = cursor.fetchone()
            
        return {
            'total_productos': resultado[0],
            'total_producciones': resultado[1],
            'ganancia_total': float(resultado[2]) if resultado[2] else 0,
            'efectividad_promedio': float(resultado[3]) if resultado[3] else 0,
            'eficiencia_promedio': float(resultado[4]) if resultado[4] else 0,
            'produccion_total': float(resultado[5]) if resultado[5] else 0
        }
        
    except Exception as e:
        print(f"Error en obtener_metricas_generales: {e}")
        return {}
    finally:
        conn.close()