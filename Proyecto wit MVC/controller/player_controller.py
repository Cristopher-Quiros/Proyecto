import json
from model.player_model import PlayerModel
from view.player_view import PlayerView

class PlayerController:
    def __init__(self):
        self.model = PlayerModel('players.json')
        self.view = PlayerView('players.json')

    def run(self):
        while True:
            choice = self.view.show_menu()
            if choice == '1':
                self.add_player()
            elif choice == '2':
                self.read_player()
            elif choice == '3':
                self.update_player()
            elif choice == '4':
                self.delete_player()
            elif choice == '5':
                self.show_filtered_player_list()
            elif choice == '6':
                self.show_player_statistics()
            elif choice == '7':
                self.perform_advanced_queries()
            elif choice == '8':
                break
            else:
                self.view.show_message("Opción inválida, intente de nuevo.")

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

    def show_filtered_player_list(self):
        while True:
            choice = self.view.get_list_option()
            if choice == '1':
                origin = self.view.get_origin_input()
                filtered_players = self.model.players_by_origin(origin)
                self.view.show_player_list(filtered_players)
                break
            elif choice == '2':
                position = self.view.get_position_input()
                filtered_players = self.model.female_players_by_position(position)
                self.view.show_player_list(filtered_players)
                break
            elif choice == '3':
                recognition = self.view.get_recognition_input()
                filtered_players = self.model.players_by_recognition(recognition)
                self.view.show_player_list(filtered_players)
                break
            else:
                self.view.show_message("Opción inválida, intente de nuevo.")