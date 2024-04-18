import sys
from PyQt5.QtWidgets import QApplication
from model.player_model import PlayerModel
from view.player_view import PlayerView

class PlayerController:
    def __init__(self):
        self.model = PlayerModel('players_data.json')
        self.app = QApplication(sys.argv)
        self.view = PlayerView('players_data.json')
        self.view.set_controller(self)
        self.view.crud_button.clicked.connect(self.show_crud_menu)
        self.view.show_menu_button.menu().triggered.connect(self.menu_option_triggered)
        self.view.show_menu_button.clicked.connect(self.show_menu)


    def run(self):
        self.view.show()
        sys.exit(self.app.exec_())

    def add_player(self):
        player_data = self.view.get_player_data()
        if player_data is not None:
            players = self.model.get_players()
            if players:
                last_id = max(player['id'] for player in players)
                player_data['id'] = last_id + 1
            else:
                player_data['id'] = 1

            self.model.add_player(player_data)
            self.view.show_message("Jugador añadido exitosamente.")
        else:
            self.view.show_message("Operación cancelada.")

    def read_player(self):
        players_with_ids = self.model.get_players_with_ids()
        selected_id = self.view.show_players_list_for_selection(players_with_ids)

        if selected_id is not None:
            # Consultar y mostrar la información del jugador
            player = self.model.get_player(selected_id)
            if player:
                self.view.show_player_info(player)
            else:
                self.view.show_message("No hay ningún jugador con ese ID.")

    def update_players(self, updated_players):
        success = self.model.update_player(updated_players)
        if success:
            self.model.write_data(self.model.get_players())  # Write updated players to JSON file
            return True
        else:
            return False

    def delete_player(self):
        player_id = self.view.get_valid_player_id()
        success = self.model.delete_player(player_id)
        if success:
            self.view.show_message("Jugador eliminado exitosamente")
        else:
            self.view.show_message("No se encontró ningún jugador con ese ID.")

    def show_menu(self):
        self.view.show_menu_button.menu().exec_(self.view.show_menu_button.mapToGlobal(self.view.show_menu_button.rect().bottomLeft()))

    def show_crud_menu(self):
        menu = self.view.create_menu()  # Obtener el menú CRUD desde la vista
        menu.exec_(self.view.crud_button.mapToGlobal(self.view.crud_button.rect().bottomLeft()))  # Mostrar el menú en la posición adecuada


    def menu_option_triggered(self, action):
        option = action.text()
        if option == "Show Player List":
            self.show_player_list()
        elif option == "Filter by Origin":
            origin = self.view.get_origin_input()
            self.filter_and_show_players_by_origin(origin)
        elif option == "Filter by Position":
            position = self.view.get_position_input()
            self.filter_and_show_players_by_position(position)
        elif option == "Filter by Recognition":
            recognition = self.view.get_recognition_input()
            self.filter_and_show_players_by_recognition(recognition)

    def show_player_list(self):
        players = self.model.get_players()
        if players:
            self.view.show_player_list(players)
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