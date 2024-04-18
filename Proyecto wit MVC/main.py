import sys
from PyQt5.QtWidgets import QApplication
from controller.player_controller import PlayerController

if __name__ == '__main__':
    app = QApplication(sys.argv)
    controller = PlayerController()
    controller.run()

