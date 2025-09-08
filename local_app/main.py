import api_cliente
import db_controlador
import ui

def main():
    ##Recupera empleados del back para usar en el reconocimiento facial
    empleados = api_cliente.get_empleados()
    db_controlador.actualizar_empleados(empleados)
    
    ui.inicializar_ui()

if __name__ == "__main__":
    main()
