import time
import cv2
import db

def abrir_camara(nombre, apellido):
    """Abre la cámara con OpenCV, detecta rostro, espera 5s y guarda ingreso."""
    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        print("⚠️ No se pudo abrir la cámara. Verifique que haya una conectada.")
        return
    
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

    deteccion_confirmada = False
    tiempo_inicio = None

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, 1.3, 5)

        # Dibujar rectángulos sobre rostros detectados
        for (x, y, w, h) in faces:
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

        # Mensaje sobre la imagen
        cv2.putText(frame, "Detectando Reconocimiento Facial...", (10,30),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0,255,0), 2)

        cv2.imshow("Cámara", frame)

        # Lógica de confirmación
        if len(faces) > 0:
            if not deteccion_confirmada:
                deteccion_confirmada = True
                tiempo_inicio = time.time()
            elif time.time() - tiempo_inicio >= 5:
                db.registrar_evento(nombre, apellido)
                print(f"Ingreso correcto: {nombre} {apellido}")
                time.sleep(3)  # esperar 3s para mostrar mensaje
                break
        else:
            deteccion_confirmada = False  # Reset si no detecta

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
