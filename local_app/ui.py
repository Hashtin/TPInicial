import sys
import cv2
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                             QHBoxLayout, QPushButton, QLabel, QInputDialog)
from PyQt5.QtCore import QTimer, Qt
from PyQt5.QtGui import QImage, QPixmap

class InterfazReconocimiento(QMainWindow):
    def __init__(self, recognizer):
        super().__init__()
        self.setWindowTitle("Sistema de Reconocimiento Facial")
        self.setGeometry(100, 100, 800, 600)

        # Variables
        self.captura = None
        self.reconocimiento_activo = False
        self.recognizer = recognizer  # Instancia de ReconocedorFacial

        self.empleado_actual = None         # Empleado actualmente reconocido

        # Inicializar UI
        self.inicializar_ui()

    def inicializar_ui(self):
        widget_central = QWidget()
        self.setCentralWidget(widget_central)
        layout_principal = QVBoxLayout()
        widget_central.setLayout(layout_principal)

        layout_botones = QHBoxLayout()

        # Botones existentes
        self.boton_iniciar = QPushButton("Inicializar reconocimiento")
        self.boton_iniciar.clicked.connect(self.iniciar_reconocimiento)
        layout_botones.addWidget(self.boton_iniciar)

        self.boton_detener = QPushButton("Detener reconocimiento")
        self.boton_detener.clicked.connect(self.detener_reconocimiento)
        self.boton_detener.setEnabled(False)
        layout_botones.addWidget(self.boton_detener)

        # Nuevo botón: registrar empleado
        self.boton_registrar = QPushButton("Registrar nueva imagen")
        self.boton_registrar.clicked.connect(self.registrar_empleado)
        layout_botones.addWidget(self.boton_registrar)

        # Nuevo botón: actualizar DB del back
        self.boton_actualizar_back = QPushButton("Actualizar empleados")
        self.boton_actualizar_back.clicked.connect(self.actualizar_back)
        layout_botones.addWidget(self.boton_actualizar_back)

        layout_principal.addLayout(layout_botones)

        # Etiqueta de cámara
        self.etiqueta_camara = QLabel()
        self.etiqueta_camara.setAlignment(Qt.AlignCenter)
        self.etiqueta_camara.setMinimumSize(640, 480)
        self.etiqueta_camara.setText("Cámara no inicializada")
        self.etiqueta_camara.setStyleSheet("border: 1px solid black; background-color: #f0f0f0;")
        layout_principal.addWidget(self.etiqueta_camara)

        # Etiqueta de estado
        self.etiqueta_estado = QLabel("Estado: Listo para inicializar")
        self.etiqueta_estado.setAlignment(Qt.AlignCenter)
        self.etiqueta_estado.setStyleSheet("""
            padding: 8px; 
            background-color: #000000; 
            border: 1px solid #c0c0c0;
            color: #FFFFFF;           
            font-weight: bold;        
            font-size: 14px;          
            font-family: Arial;       
        """)
        layout_principal.addWidget(self.etiqueta_estado)

        # Timer para actualizar la cámara
        self.temporizador = QTimer()
        self.temporizador.timeout.connect(self.actualizar_frame)

    # ---------- Métodos para iniciar/detener reconocimiento ----------
    def iniciar_reconocimiento(self):
        if self.captura is None or not self.captura.isOpened():
            self.inicializar_camara()

        self.boton_iniciar.setEnabled(False)
        self.boton_detener.setEnabled(True)

    def detener_reconocimiento(self):
        if self.captura:
            self.temporizador.stop()
            self.captura.release()
            self.captura = None
            self.etiqueta_camara.setText("Cámara detenida")
            self.etiqueta_camara.setPixmap(QPixmap())  # limpiar imagen
            self.actualizar_estado("Cámara apagada")

        self.boton_iniciar.setEnabled(True)
        self.boton_detener.setEnabled(False)

    def inicializar_camara(self):
        self.captura = cv2.VideoCapture(0)
        if not self.captura.isOpened():
            self.etiqueta_camara.setText("Error: No se puede acceder a la cámara")
            return
        self.temporizador.start(30)
        self.actualizar_estado("Cámara inicializada")

    # ---------- Actualizar frame de la cámara ----------
    def actualizar_frame(self):
        if self.captura and self.captura.isOpened():
            ret, frame = self.captura.read()
            if not ret:
                return

            # --- Detección rápida de rostro con Haar Cascade ---
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            face_cascade = cv2.CascadeClassifier(
                cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
            )
            faces = face_cascade.detectMultiScale(gray, 1.3, 5)

            if len(faces) == 0 and self.empleado_actual != None:
                # No hay rostro en pantalla
                self.empleado_actual = None
                
            elif self.empleado_actual == None and len(faces) > 0:
                if getattr(self, "empleado_actual", None) is None:
                    embedding, _ = self.recognizer.extraer_embedding(frame)
                    if embedding is not None:
                        empleado, confianza = self.recognizer.reconocer_empleado(embedding)
                        if empleado is not None:
                            self.empleado_actual = empleado
                            self.actualizar_estado(f"Empleado {self.empleado_actual} reconocido, registrando")
                        else:
                            self.actualizar_estado("Rostro detectado (no reconocido)")
                    else:
                        self.actualizar_estado("Rostro detectado (no válido)")
            elif self.empleado_actual != None:
                # Ya hay empleado reconocido, mantenemos estado
                self.actualizar_estado(f"Empleado {self.empleado_actual} reconocido, registrando")
            else:
                self.actualizar_estado("No se detecta ningun rostro")

            # --- Mostrar frame en la UI ---
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            h, w, ch = frame_rgb.shape
            bytes_per_line = ch * w
            imagen_qt = QImage(frame_rgb.data, w, h, bytes_per_line, QImage.Format_RGB888)
            self.etiqueta_camara.setPixmap(QPixmap.fromImage(imagen_qt).scaled(
                640, 480, Qt.KeepAspectRatio, Qt.SmoothTransformation))

    # ---------- Función para registrar empleado ----------
    def registrar_empleado(self):
        if self.captura and self.captura.isOpened():
            ret, frame = self.captura.read()
            if ret:
                # Pedir ID mediante cuadro de diálogo
                id_empleado, ok = QInputDialog.getInt(self, "Registrar empleado", "Ingrese ID del nuevo empleado:")
                if ok:
                    success = self.recognizer.registrar_empleado_local(id_empleado, frame)
                    if success:
                        self.actualizar_estado(f"Empleado {id_empleado} registrado localmente")
                    else:
                        self.actualizar_estado("No se detectó rostro, intente de nuevo")
        else:
            self.actualizar_estado("Cámara no inicializada")

    # ---------- Placeholder para actualizar DB del back ----------
    def actualizar_back(self):
        self.actualizar_estado("Funcionalidad de actualización desde back no implementada")

    # ---------- Actualizar estado ----------
    def actualizar_estado(self, mensaje):
        self.etiqueta_estado.setText(f"Estado: {mensaje}")

    # ---------- Cerrar ventana ----------
    def closeEvent(self, event):
        if self.captura:
            self.captura.release()
        self.temporizador.stop()
        event.accept()

# ---------- Función para inicializar la UI ----------
def inicializar_ui(recognizer):
    app = QApplication(sys.argv)
    ventana = InterfazReconocimiento(recognizer)
    ventana.show()
    sys.exit(app.exec_())
