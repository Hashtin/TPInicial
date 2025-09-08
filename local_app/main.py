import api_cliente
import db_controlador
import ui
from recognizer import ReconocedorFacial

def main():
    # Crear db y tabla por primera vez
    db_controlador.init_db()

    # Recupera empleados del back para usar en el reconocimiento facial
    empleados = api_cliente.get_empleados()
    db_controlador.actualizar_empleados(empleados)

    # Crear instancia del recognizer
    recognizer = ReconocedorFacial()

    # Inicializar la UI pasando el recognizer
    ui.inicializar_ui(recognizer)

if __name__ == "__main__":
    main()
