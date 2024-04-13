# Controlador

import sys
from PyQt5.QtWidgets import QApplication
from model.player_model import PlayerModel
from view.player_view import PlayerView

class PlayerController:
    def __init__(self):
        self.model = PlayerModel('players_data.json')
        self.app = QApplication(sys.argv)
        self.view = PlayerView('players_data.json')
        self.view.set_controller(self)  # Asignar el controlador a la vista
        self.view.add_button.clicked.connect(self.add_player)
        self.view.read_button.clicked.connect(self.read_player)
        self.view.update_button.clicked.connect(self.update_player)
        self.view.delete_button.clicked.connect(self.delete_player)
        self.view.show_menu_button.menu().triggered.connect(self.menu_option_triggered)  # Conectar la señal del menú
        self.view.show_menu_button.clicked.connect(self.show_menu)  # Mostrar el menú

    def run(self):
        self.view.show()
        sys.exit(self.app.exec_())

    def add_player(self):
        player_data = self.view.get_player_data()
        if not self.model.player_exists(player_data['id']):
            self.model.add_player(player_data)
            self.view.show_message("Jugador agregado exitosamente")
        else:
            self.view.show_message("El jugador ya existe en la base de datos.")

    def read_player(self):
        player_id = self.view.get_player_id()
        player = self.model.get_player(player_id)
        if player:
            self.view.show_player_info(player)
        else:
            self.view.show_message("No se encontró ningún jugador con ese ID.")

    def update_player(self):
        player_id = self.view.get_player_id()
        if self.model.player_exists(player_id):
            player_data = self.view.get_player_data()
            success = self.model.update_player(player_id, player_data)
            if success:
                self.view.show_message("Jugador actualizado exitosamente")
            else:
                self.view.show_message("Hubo un problema al actualizar el jugador.")
        else:
            self.view.show_message("No se encontró ningún jugador con ese ID.")

    def delete_player(self):
        player_id = self.view.get_player_id()
        success = self.model.delete_player(player_id)
        if success:
            self.view.show_message("Jugador eliminado exitosamente")
        else:
            self.view.show_message("No se encontró ningún jugador con ese ID.")

    def show_menu(self):
        self.view.show_menu_button.menu().exec_(self.view.show_menu_button.mapToGlobal(self.view.show_menu_button.rect().bottomLeft()))

    def menu_option_triggered(self, action):
        option = action.text()
        if option == "Show Player List":
            self.show_player_list()
        elif option == "Filter by Origin":
            self.filter_and_show_players_by_origin()
        elif option == "Filter by Position":
            self.filter_and_show_players_by_position()
        elif option == "Filter by Recognition":
            self.filter_and_show_players_by_recognition()

    def show_player_list(self):
        players = self.model.get_players()
        if players:
            self.view.show_player_list(players)  # Pasar la lista de jugadores a la vista
        else:
            self.view.show_message("No players found.")

    def filter_players_by_origin(self, origin):
        return self.model.filter_players_by_origin(origin)

    def filter_players_by_position(self, position):
        return self.model.filter_players_by_position(position)

    def filter_players_by_recognition(self, recognition):
        return self.model.filter_players_by_recognition(recognition)


