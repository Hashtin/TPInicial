from flask import Flask, jsonify, request
from flask_cors import CORS
import db
import os 
import pandas_analizador

app = Flask(__name__)

CORS(app)

# ====================== RUTAS API ======================
@app.route('/api/')
def api_index():
    return jsonify({"message": "API funcionando correctamente"})

@app.route("/api/registros")
def api_registros():
    datos = db.obtener_registros_empleados()
    return jsonify(datos)

@app.route("/api/empleados-embedding")
def obtener_empleados_embeddings():
    datos = db.obtener_todos_empleados_embeddings()
    return jsonify(datos)

@app.route('/api/registrar-ingreso', methods=['POST'])
def registrar_ingreso():
    data = request.get_json()
    empleado_id = data['empleado_id']
    resultado = db.ingreso_empleado(empleado_id)
    accion = None
    nombre = None
    apellido = None

    if resultado:
        accion = db.ultima_accion_empleado(empleado_id)
        empleado = db.get_empleado(empleado_id)
        nombre = empleado[0]
        apellido = empleado[1]
    return jsonify({'success': resultado , 'nombre': nombre, 'apellido': apellido, 'accion': accion})

@app.route('/api//registrar-embedding', methods=['POST'])
def registrar_embedding():
    data = request.get_json()
    empleado_id = data['empleado_id']
    embedding = data['embedding']

    resultado = db.registrar_embedding(empleado_id, embedding)

    return jsonify({'success': resultado})

#Prueba Analisis productivo
@app.route('/api/analisis/productividad')
def analisis_productividad():
    try:
        # Obtener datos crudos desde la base de datos
        datos_crudos = db.obtener_datos_analisis_productividad()
        metricas_generales = db.obtener_metricas_generales()
        if not datos_crudos or not metricas_generales:
            return jsonify({'error': 'No hay datos de producción'}), 404
        
        resultados = pandas_analizador.analisis_productivo(datos_crudos, metricas_generales)
        return jsonify(resultados)
        
    except Exception as e:
        print(f"Error en analisis_productividad: {str(e)}")
        return jsonify({'error': 'Error interno del servidor'}), 500

# ====================== RUN ======================
if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=os.getenv("PORT", 5000))