import sys
import cv2
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                             QHBoxLayout, QPushButton, QLabel)
from PyQt5.QtCore import QTimer, Qt
from PyQt5.QtGui import QImage, QPixmap

class InterfazReconocimiento(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Sistema de Reconocimiento Facial")
        self.setGeometry(100, 100, 800, 600)
        
        # Variables para la cámara
        self.captura = None
        self.reconocimiento_activo = False
        
        # Inicializar UI
        self.inicializar_ui()
        
    def inicializar_ui(self):
        # Widget central
        widget_central = QWidget()
        self.setCentralWidget(widget_central)
        
        # Layout principal
        layout_principal = QVBoxLayout()
        widget_central.setLayout(layout_principal)
        
        # Layout para los botones (arriba de la cámara)
        layout_botones = QHBoxLayout()
        
        # Botón para iniciar reconocimiento
        self.boton_iniciar = QPushButton("Inicializar reconocimiento")
        self.boton_iniciar.clicked.connect(self.iniciar_reconocimiento)
        layout_botones.addWidget(self.boton_iniciar)
        
        # Botón para detener reconocimiento
        self.boton_detener = QPushButton("Detener reconocimiento")
        self.boton_detener.clicked.connect(self.detener_reconocimiento)
        self.boton_detener.setEnabled(False)
        layout_botones.addWidget(self.boton_detener)
        
        layout_principal.addLayout(layout_botones)
        
        # Etiqueta para la cámara
        self.etiqueta_camara = QLabel()
        self.etiqueta_camara.setAlignment(Qt.AlignCenter)
        self.etiqueta_camara.setMinimumSize(640, 480)
        self.etiqueta_camara.setText("Cámara no inicializada")
        self.etiqueta_camara.setStyleSheet("border: 1px solid black; background-color: #f0f0f0;")
        layout_principal.addWidget(self.etiqueta_camara)
        
        # Etiqueta para el estado
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
        
    def iniciar_reconocimiento(self):
        # Inicializar cámara si no está inicializada
        if self.captura is None:
            self.inicializar_camara()
            
        self.reconocimiento_activo = True
        self.boton_iniciar.setEnabled(False)
        self.boton_detener.setEnabled(True)
        self.actualizar_estado("Reconocimiento facial activo")
        
    def detener_reconocimiento(self):
        self.reconocimiento_activo = False
        self.boton_iniciar.setEnabled(True)
        self.boton_detener.setEnabled(False)
        self.actualizar_estado("Reconocimiento detenido")
        
    def inicializar_camara(self):
        self.captura = cv2.VideoCapture(0)
        if not self.captura.isOpened():
            self.etiqueta_camara.setText("Error: No se puede acceder a la cámara")
            return
            
        # Iniciar el temporizador para actualizar los frames
        self.temporizador.start(30)
        self.actualizar_estado("Cámara inicializada")
        
    def actualizar_frame(self):
        if self.captura and self.captura.isOpened():
            ret, frame = self.captura.read()
            if ret:
                # Si el reconocimiento está activo, procesar el frame
                if self.reconocimiento_activo:
                    # Aquí iría el código de reconocimiento facial
                    # Por ahora solo mostramos el frame normal
                    pass
                    
                # Convertir el frame de BGR a RGB para mostrarlo en Qt
                frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                h, w, ch = frame_rgb.shape
                bytes_per_line = ch * w
                imagen_qt = QImage(frame_rgb.data, w, h, bytes_per_line, QImage.Format_RGB888)
                self.etiqueta_camara.setPixmap(QPixmap.fromImage(imagen_qt).scaled(
                    640, 480, Qt.KeepAspectRatio, Qt.SmoothTransformation))
                    
    def actualizar_estado(self, mensaje):
        self.etiqueta_estado.setText(f"Estado: {mensaje}")
        
    def closeEvent(self, event):
        if self.captura:
            self.captura.release()
        self.temporizador.stop()
        event.accept()

# Función para inicializar la UI (llamada desde main.py)
def inicializar_ui():
    app = QApplication(sys.argv)
    ventana = InterfazReconocimiento()
    ventana.show()
    sys.exit(app.exec_())