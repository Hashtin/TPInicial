import cv2
import os
import imutils 

def capturar_rostro():
    id_empleado = 0
    ruta_data = "../dataset"
    ruta_empleado = ruta_data + "/" + str(id_empleado)
    ruta_video = ruta_data + "/videos/" + str(id_empleado) + ".mp4"

    if not os.path.exists(ruta_empleado):
        print('Carpeta creada: ', ruta_empleado)
        os.makedirs(ruta_empleado)
    
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
