import time
import cv2
import db

def detectar_usuario():
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("⚠️ No se pudo abrir la cámara.")
        return

    face_cascade = cv2.CascadeClassifier(
        cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
    )

    tiempo_inicio = cv2.getTickCount()
    tiempo_limite = 5  # segundos

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, 1.3, 5)

        # Dibujar rectángulos sobre los rostros detectados
        for (x, y, w, h) in faces:
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

        # Mensaje sobre la imagen
        cv2.putText(frame, "Detectando rostro...", (10,30),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0,255,0), 2)

        cv2.imshow("Cámara", frame)

        # Salir si se presiona 'q'
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

        # Salir si pasa el tiempo límite
        tiempo_actual = (cv2.getTickCount() - tiempo_inicio) / cv2.getTickFrequency()
        if tiempo_actual > tiempo_limite:
            break

    cap.release()
    cv2.destroyAllWindows()

