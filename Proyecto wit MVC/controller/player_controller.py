import json # noqa
import datetime # noqa

from model.player_model import PlayerModel
from view.player_view import PlayerView

class PlayerController:
    def __init__(self):
        self.model = PlayerModel('players.json')
        self.view = PlayerView()

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
                self.show_player_list()
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

    def show_player_list(self):
        players = self.model.get_players()
        self.view.show_player_list(players)

    def show_player_statistics(self):
        # Implementa la lógica para mostrar estadísticas de los jugadores
        pass

    def perform_advanced_queries(self):
        while True:
            choice = self.view.show_advanced_queries_menu()
            if choice == '1':
                self.show_players_by_origin()
            elif choice == '2':
                self.show_players_in_age_range()
            elif choice == '3':
                self.show_players_by_height_and_gender()
            elif choice == '4':
                self.show_players_by_club()
            elif choice == '5':
                self.show_female_players_by_position()
            elif choice == '6':
                self.show_top_players_by_height_and_agility()
            elif choice == '7':
                self.show_players_by_speed_range()
            elif choice == '8':
                self.show_average_ball_control_by_position()
            elif choice == '9':
                break
            else:
                self.view.show_message("Opción inválida, intente de nuevo.")

    def show_players_by_origin(self):
        origin = input("Ingrese el origen para la consulta: ")
        count = self.model.players_by_origin(origin)
        self.view.show_players_by_origin(count)

    def show_players_in_age_range(self):
        min_age = int(input("Ingrese la edad mínima del rango: "))
        max_age = int(input("Ingrese la edad máxima del rango: "))
        players = self.model.players_by_age_range(min_age, max_age)
        self.view.show_players_in_age_range(players)

    def show_players_by_height_and_gender(self):
        height = float(input("Ingrese la altura para la consulta: "))
        gender = input("Ingrese el género para la consulta: ")
        count = self.model.players_by_height_and_gender(height, gender)
        self.view.show_players_by_height_and_gender(count)

    def show_players_by_club(self):
        club = input("Ingrese el club para la consulta: ")
        players = self.model.players_by_club(club)
        self.view.show_players_by_club(players)

    def show_female_players_by_position(self):
        position = input("Ingrese la posición en el campo para la consulta: ")
        count = self.model.female_players_by_position(position)
        self.view.show_female_players_by_position(count)

    def show_top_players_by_height_and_agility(self):
        top_players = self.model.top_players_by_height_and_agility()
        self.view.show_top_players_by_height_and_agility(top_players)

    def show_players_by_speed_range(self):
        min_speed = int(input("Ingrese la velocidad mínima para la consulta: "))
        max_speed = int(input("Ingrese la velocidad máxima para la consulta: "))
        count = self.model.players_by_speed_range(min_speed, max_speed)
        self.view.show_players_by_speed_range(count)

    def show_average_ball_control_by_position(self):
        position = input("Ingrese la posición en el campo para la consulta: ")
        average_ball_control = self.model.average_ball_control_by_position(position)
        self.view.show_average_ball_control_by_position(average_ball_control)
