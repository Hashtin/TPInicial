from flask import Flask, jsonify, request
from flask_cors import CORS
import db

app = Flask(__name__)
CORS(app)  # Permite requests desde frontend en Vercel

# ====================== RUTAS API ======================
@app.route('/api/')
def api_index():
    return jsonify({"message": "API funcionando correctamente"})

@app.route("/api/registros")
def api_registros():
    datos = db.obtener_registros_empleados()
    return jsonify(datos)

@app.route('/api/registrar-ingreso', methods=['POST'])
def registrar_ingreso():
    data = request.get_json()
    empleado_id = data['empleado_id']
    resultado = db.ingreso_empleado(empleado_id)
    return jsonify({'success': resultado})

@app.route('/api/registrar-egreso', methods=['POST'])  
def registrar_egreso():
    data = request.get_json()
    empleado_id = data['empleado_id']
    resultado = db.egreso_empleado(empleado_id)
    return jsonify({'success': resultado})

# ====================== RUN ======================
if __name__ == "__main__":
    app.run(debug=True)