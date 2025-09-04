# Sistema de Registro de Ingresos y Egresos con OpenCV y Flask

Este proyecto es un sistema básico de control de asistencia para empleados, desarrollado con **Python**, **Flask** y **OpenCV**. Permite registrar el ingreso y egreso de los empleados mediante un formulario web y la captura de su rostro, guardando los eventos con timestamp en una base de datos SQLite.

---

## 🛠 Funcionalidades

- Registro de empleados en la base de datos.
- Interfaz web para ingresar nombre y apellido.
- Activación de la cámara con OpenCV para detección de rostro.
- Espera de 5 segundos tras la detección para confirmar el ingreso/egreso.
- Registro automático en la base de datos (`database.db`) con:
  - Nombre y apellido del empleado.
  - Acción: Ingreso o Egreso (alternando según el último registro).
  - Timestamp del evento.
- Tabla de registros visible en la web.
- Preparado para integrar reconocimiento facial avanzado.

---

## 📂 Estructura del proyecto   
TPINICIAL/  
├─ backend/  
│└─ db.py   
│└─ main.py  
│└─ recognizer.py  
├─ database/  
│└─ database.bd  
├─ frontend/   
│ └─ static/  
│ │ └─ style.css  
│ └─ templates/   
│ │└─ index.html  
│ │└─ registros.html  
├─ haarcascade_frontalface_default.xml  
├─ Readme.md

## ⚙️ Requisitos

- Python 3.8 o superior
- Librerías de Python:
  - Flask
  - OpenCV (`opencv-contrib-python`)
  - SQLite3 (incluido en Python)
- Extensión recomendada para VSCode:
  - SQLite (para visualizar la base de datos)

Instalación de librerías:

```bash
pip install flask opencv-contrib-python imutils
