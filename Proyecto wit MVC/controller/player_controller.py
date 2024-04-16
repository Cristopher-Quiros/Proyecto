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
        self.view.read_button.clicked.connect(self.read_player)  # Conectar el botón de "Leer" con la función read_player
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
        player_id = self.get_valid_player_id()
        if player_id is not None:  # Verificar si se ingresó un ID de jugador válido
            player = self.model.get_player(player_id)
            if player:
                self.view.show_player_info(player)  # Mostrar la información del jugador en la vista
            else:
                self.view.show_message("No hay ningún jugador con ese ID.")
        else:
            self.view.show_message("Operación cancelada.")

    def get_valid_player_id(self):
        while True:
            player_id = self.view.get_player_id_input()
            if player_id is not None:
                return player_id

    def update_player(self, player_data):
        if isinstance(player_data, dict):  # Verificar si player_data es un diccionario
            player_id = player_data.get('id')
            if player_id:
                if self.model.get_player(player_id):
                    self.model.update_player(player_id, player_data)  # Pasar el ID del jugador y los nuevos datos
                    return True
        return False

    def delete_player(self):
        player_id = self.view.get_player_id_input()
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
            self.show_player_list()  # Llamar al método sin argumentos
        elif option == "Filter by Origin":
            origin = self.get_origin_input()
            self.filter_and_show_players_by_origin(origin)
        elif option == "Filter by Position":
            position = self.get_position_input()
            self.filter_and_show_players_by_position(position)
        elif option == "Filter by Recognition":
            recognition = self.get_recognition_input()
            self.filter_and_show_players_by_recognition(recognition)

    def show_player_list(self):
        players = self.model.get_players()
        if players:
            self.view.show_player_list(players)  # Pasar la lista de jugadores a la vista
        else:
            self.view.show_message("No se encontraron jugadores.")

    def filter_and_show_players_by_origin(self, origin):
        filtered_players = self.model.filter_players_by_origin(origin)
        if filtered_players:
            self.view.show_player_list(filtered_players)
        else:
            self.view.show_message("No hay jugadores con ese lugar de Origen.")

    def filter_and_show_players_by_position(self, position):
        filtered_players = self.model.filter_players_by_position(position)
        if filtered_players:
            self.view.show_player_list(filtered_players)
        else:
            self.view.show_message("No hay jugadores con esa posición en el campo.")

    def filter_and_show_players_by_recognition(self, recognition):
        filtered_players = self.model.filter_players_by_recognition(recognition)
        if filtered_players:
            self.view.show_player_list(filtered_players)
        else:
            self.view.show_message("No hay jugadores con esa cantidad de reconocimientos.")

    def get_origin_input(self):
        return self.view.get_origin_input()

    def get_position_input(self):
        return self.view.get_position_input()

    def get_recognition_input(self):
        return self.view.get_recognition_input()
