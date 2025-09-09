import numpy as np
import db_controlador
from insightface.app import FaceAnalysis
import api_cliente

class ReconocedorFacial:
    def __init__(self):
        self.empleados = None
        self.embeddings = None
        self.cargar_empleados_db()
        
        # Inicializar InsightFace
        self.app = FaceAnalysis(name='buffalo_l')
        self.app.prepare(ctx_id=0, det_size=(640, 640))
    
    def cargar_empleados_db(self):
        """Carga todos los empleados y sus embeddings desde la DB"""
        self.empleados = db_controlador.obtener_todos_empleados()
        if self.empleados:
            self.embeddings = np.array([emp['embedding'] for emp in self.empleados])
    
    def registrar_empleado_local(self, id_empleado, frame):
        """
        Extrae el embedding de un frame y lo guarda en la DB local.
        
        Args:
            id_empleado (int): ID del empleado
            frame (np.array): imagen en formato BGR (OpenCV)
        
        Returns:
            bool: True si se registró correctamente, False si no se detectó rostro
        """
        embedding, _ = self.extraer_embedding(frame)
        empleado = self.reconocer_empleado(embedding)
        print(f"Empleado reconocido?: {empleado}")
        if embedding is not None and empleado[0] is None:
            # Registrar en SQLite usando db_controlador
            resultado = api_cliente.registrar_embedding_back(id_empleado, embedding)
            print(f"resultado back: {resultado}")
            if resultado:
                db_controlador.registrar_embedding_local(id_empleado, embedding)
                # Actualizar la cache interna de empleados y embeddings
                self.actualizar_empleados()
                print("Empleado registrado exitosamente")
                return True
        print("Empleado ya existente o no reconocido")
        return False

    def extraer_embedding(self, frame):
        """Extrae el embedding facial de un frame usando InsightFace"""
        # InsightFace trabaja directamente con BGR (OpenCV format)
        caras = self.app.get(frame)
        
        if len(caras) > 0:
            # Tomar la cara con mayor confianza de detección
            cara = max(caras, key=lambda x: x.det_score)
            embedding = cara.normed_embedding
            bbox = cara.bbox.astype(int)
            
            # Convertir bbox a formato (x, y, w, h)
            x, y, x2, y2 = bbox
            ubicacion = (x, y, x2 - x, y2 - y)
            
            return embedding, ubicacion
        
        return None, None
    
    def reconocer_empleado(self, embedding_actual):
        """Approach de dos pasos: pre-filtro vectorizado + verificación precisa"""
        if not self.empleados or self.embeddings is None:
            return None, 0.0
        
        # 1. PRE-FILTRO: Encontrar los 5 más similares (vectorizado)
        distancias = np.linalg.norm(self.embeddings - embedding_actual, axis=1)
        indices_top = np.argsort(distancias)[:5]  # Top 5 más cercanos
        
        # 2. VERIFICACIÓN PRECISA: Calcular similitud coseno para los candidatos
        mejor_empleado = None
        mejor_similitud = 0.0
        
        for idx in indices_top:
            empleado = self.empleados[idx]
            
            # Calcular similitud coseno (InsightFace usa embeddings normalizados)
            similitud = np.dot(embedding_actual, empleado["embedding"])
            
            if similitud > mejor_similitud:
                mejor_similitud = similitud
                mejor_empleado = empleado

        if mejor_similitud > 0.6:  # Umbral de confianza
            return mejor_empleado['id'], mejor_similitud
        
        return None, 0.0
    
    def procesar_frame(self, frame):
        """Procesa un frame y devuelve el resultado del reconocimiento"""
        embedding, ubicacion_rostro = self.extraer_embedding(frame)
        
        if embedding is None:
            return {"rostro_detectado": False}
        
        empleado, confianza = self.reconocer_empleado(embedding)
        
        resultado = {
            "rostro_detectado": True,
            "empleado": empleado,
            "confianza": confianza,
            "ubicacion_rostro": ubicacion_rostro
        }
        
        return resultado
    
    def actualizar_empleados(self):
        """Actualiza la lista de empleados desde la DB"""
        self.cargar_empleados_db()