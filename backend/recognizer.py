import cv2
import os
import imutils 
import numpy as np
import db

RUTA_DATA = "../dataset"

face_recognizer = None
is_active = False

#Machine learning
def capturar_rostro(id_empleado):
    ruta_empleado = RUTA_DATA + "/" + str(id_empleado)
    ruta_video = "/videos/" + str(id_empleado) + ".mp4"

    if not os.path.exists(ruta_empleado):
        print('Carpeta creada: ', ruta_empleado)
        os.makedirs(ruta_empleado)
    
    if not os.path.exists(ruta_video):
        print('NO SE ENCONTRO EL VIDEO DEL EMPLEADO')
        return
    
    cap = cv2.VideoCapture(ruta_video)

    faceClassif = cv2.CascadeClassifier(cv2.data.haarcascades+ 'haarcascade_frontalface_default.xml')
    count = 0

    while True: 
        ret, frame = cap.read()
        if ret == False: break
        frame = imutils.resize(frame, width=640)
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        auxFrame = frame.copy()

        faces = faceClassif.detectMultiScale(gray,1.3,5)

        for(x,y,w,h) in faces:
            cv2.rectangle(frame, (x,y), (x + w, +h),(0,255,0),2)
            rostro = auxFrame[y:y+h,x:x+w]
            rostro = cv2.resize(rostro,(150,150),interpolation=cv2.INTER_CUBIC)
            cv2.imwrite(ruta_empleado + '/rostro_{}.jpg'.format(count),rostro)
            count = count + 1
        cv2.imshow('frame',frame)

        k = cv2.waitKey(1)
        if k == 27 or count >= 300:
            break
    cap.release()
    cv2.destroyAllWindows()

def creacion_modelo():
    lista_empleados = os.listdir(RUTA_DATA)

    etiquetas = []
    rostros_data = []

    for id_dir in lista_empleados:
        etiqueta = int(id_dir)
        ruta_empleado = RUTA_DATA + "/" + str(id_dir)
        print("Leyendo las imagenes")

        for nombre_archivo in os.listdir(ruta_empleado):
            print("Rostros: ", id_dir + '/' + nombre_archivo)
            etiquetas.append(etiqueta)
            rostros_data.append(cv2.imread(ruta_empleado + "/" + nombre_archivo,0))
            ##Representativo
            image = cv2.imread(ruta_empleado + "/" + nombre_archivo,0)
            cv2.imshow('image', image)
            cv2.waitKey(10)


    print("numero de etiquetas 0: ", np.count_nonzero(np.array(etiquetas)==0))
    print("numero de etiquetas 1: ", np.count_nonzero(np.array(etiquetas)==1))
    print("numero de etiquetas 2: ", np.count_nonzero(np.array(etiquetas)==2))
    print("numero de etiquetas 3: ", np.count_nonzero(np.array(etiquetas)==3))
    
    entrenamiento_eigen_face(rostros_data,etiquetas)

def entrenamiento_eigen_face(rostros_data,etiquetas):
    face_recognizer = cv2.face.EigenFaceRecognizer_create()
    print("Entrenando...")
    face_recognizer.train(rostros_data, np.array(etiquetas))
    face_recognizer.write("modeloEigenFaces.xml")
    print("Modelo almacenado")

# Face Recognizer iniciador
def init_face_recognizer():
    global face_recognizer
    global is_active
    face_recognizer = cv2.face.EigenFaceRecognizer_create()
    face_recognizer.read('modeloEigenFaces.xml')
    is_active = True


# Stream de video en vivo
def generar_frames(accion):
    global face_recognizer
    face_cascade = cv2.CascadeClassifier(
        cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
    )

    cap = cv2.VideoCapture(0)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
    
    start_time = cv2.getTickCount()
    tiempo_limite = 60  # segundos

    detected = False
    texto = "Identificando..."
    color = (245, 73, 39)
    
    try:
        while True:
            ret, frame = cap.read()
            if not ret:
                break
            
            
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            auxFrame = gray.copy()
            faces = face_cascade.detectMultiScale(gray, 1.3, 5)

            for (x, y, w, h) in faces:
                rostro = auxFrame[y:y+h,x:x+w]
                rostro = cv2.resize(rostro,(150,150),interpolation=cv2.INTER_CUBIC)
                result = face_recognizer.predict(rostro) ##predice etiqueta

                cv2.putText(frame, texto,(x,y - 10),1,1.3,color,2,cv2.LINE_AA) ## visualiza prediccion
                
                if(not(detected) and result[1] < 6000):
                    detected = True
                    id_empleado = int(result[0])
                    empleado = db.get_empleado(id_empleado)

                    if((accion == 'Egreso' and db.egreso_empleado(id_empleado)) or
                        (accion == 'Ingreso' and db.ingreso_empleado(id_empleado))):
                        texto = f"{empleado[0]} {empleado[1]}, {accion} registrado"
                        color = (11,103,48)
                    else:
                        texto = f"{empleado[0]} {empleado[1]}, {accion} fallido"
                        color = (255,0,0)
                    
            ret, buffer = cv2.imencode('.jpg', frame)
            frame_bytes = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')

            # Limitar tiempo de la cámara
            tiempo_actual = (cv2.getTickCount() - start_time) / cv2.getTickFrequency()
            if tiempo_actual > tiempo_limite:
                break
    finally:
        cap.release()