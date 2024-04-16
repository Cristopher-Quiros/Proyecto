import sys
from PyQt5.QtWidgets import QApplication
from controller.player_controller import PlayerController

if __name__ == '__main__':
    app = QApplication(sys.argv)
    controller = PlayerController()
    controller.run()

    # Ejecutar el bucle de eventos personalizado
    while controller.is_running:
        try:
            app.processEvents()
        except KeyboardInterrupt:  # Capturar la excepción generada por cancelar un diálogo de entrada
            print("Operación cancelada por el usuario.")

    sys.exit()
