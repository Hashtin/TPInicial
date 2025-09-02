import cv2
import os
import imutils 
import numpy as np

RUTA_DATA = "../dataset"

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
