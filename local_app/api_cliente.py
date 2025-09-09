import requests

backend_url = "https://tpinicial.onrender.com/api"

def registrar_embedding_back(id_empleado, embedding):
    """
    Envía el embedding a la API del backend
    """
    try:
        # Convertir el embedding numpy array a lista para JSON
        embedding_lista = embedding.tolist()
        
        # Preparar los datos para enviar
        datos = {
            'empleado_id': id_empleado,
            'embedding': embedding_lista
        }
        
        # Hacer la petición POST al backend
        respuesta = requests.post(
            f"{backend_url}/registrar-embedding",
            json=datos,
            timeout=10
        )
        
        # Verificar si la petición fue exitosa
        respuesta.raise_for_status()
        
        return respuesta.json()['success']
    
    except requests.exceptions.RequestException as e:
        print(f"Error al enviar embedding al backend: {e}")
        return False

def get_empleados():
    try:
        respuesta = requests.get(f"{backend_url}/empleados-embedding", timeout=10)
        respuesta.raise_for_status()
        return respuesta.json()  # Devuelve lista de empleados con embeddings
    except requests.exceptions.RequestException as e:
        print(f"Error al obtener empleados: {e}")
        return []