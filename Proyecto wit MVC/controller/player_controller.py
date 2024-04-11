import json  # Importa el módulo json para trabajar con datos JSON
from model.player_model import PlayerModel  # Importa la clase PlayerModel del módulo player_model
from view.player_view import PlayerView  # Importa la clase PlayerView del módulo player_view

class PlayerController:  # Define la clase PlayerController
    def __init__(self):
        self.model = PlayerModel('players.json')  # Inicializa el modelo con el archivo 'players.json'
        self.view = PlayerView('players.json')  # Inicializa la vista con el archivo 'players.json'

    def run(self):
        while True:
            choice = self.view.show_menu()  # Muestra el menú y obtiene la opción seleccionada por el usuario
            if choice == '1':
                self.add_player()  # Llama al método para agregar un jugador
            elif choice == '2':
                self.read_player()  # Llama al método para leer la información de un jugador
            elif choice == '3':
                self.update_player()  # Llama al método para actualizar la información de un jugador
            elif choice == '4':
                self.delete_player()  # Llama al método para eliminar un jugador
            elif choice == '5':
                self.show_filtered_player_list()  # Llama al método para mostrar una lista filtrada de jugadores
            elif choice == '6':
                self.show_player_statistics()  # Llama al método para mostrar estadísticas de jugadores
            elif choice == '7':
                self.perform_advanced_queries()  # Llama al método para realizar consultas avanzadas
            elif choice == '8':
                break  # Sale del bucle while si se elige la opción '8'
            else:
                self.view.show_message("Opción inválida, intente de nuevo.")  # Muestra un mensaje de error para opciones inválidas

    def add_player(self):
        player_data = self.view.get_player_data()  # Obtiene los datos del jugador desde la vista
        if not self.model.player_exists(player_data['id']):  # Verifica si el jugador ya existe en la base de datos
            self.model.add_player(player_data)  # Agrega el jugador al modelo
            self.view.show_message("Jugador agregado exitosamente")  # Muestra un mensaje de éxito
        else:
            self.view.show_message("El jugador ya existe en la base de datos.")  # Muestra un mensaje de error si el jugador ya existe

    def read_player(self):
        player_id = self.view.get_player_id()  # Obtiene el ID del jugador desde la vista
        player = self.model.get_player(player_id)  # Obtiene la información del jugador desde el modelo
        if player:
            self.view.show_player_info(player)  # Muestra la información del jugador
        else:
            self.view.show_message("No se encontró ningún jugador con ese ID.")  # Muestra un mensaje de error si el jugador no se encuentra

    def update_player(self):
        player_id = self.view.get_player_id()  # Obtiene el ID del jugador desde la vista
        if self.model.player_exists(player_id):  # Verifica si el jugador existe en la base de datos
            player_data = self.view.get_player_data()  # Obtiene los nuevos datos del jugador desde la vista
            success = self.model.update_player(player_id, player_data)  # Actualiza la información del jugador en el modelo
            if success:
                self.view.show_message("Jugador actualizado exitosamente")  # Muestra un mensaje de éxito
            else:
                self.view.show_message("Hubo un problema al actualizar el jugador.")  # Muestra un mensaje de error si hay algún problema
        else:
            self.view.show_message("No se encontró ningún jugador con ese ID.")  # Muestra un mensaje de error si el jugador no se encuentra

    def delete_player(self):
        player_id = self.view.get_player_id()  # Obtiene el ID del jugador desde la vista
        success = self.model.delete_player(player_id)  # Elimina el jugador del modelo
        if success:
            self.view.show_message("Jugador eliminado exitosamente")  # Muestra un mensaje de éxito
        else:
            self.view.show_message("No se encontró ningún jugador con ese ID.")  # Muestra un mensaje de error si el jugador no se encuentra

    def show_filtered_player_list(self):
        while True:
            choice = self.view.get_list_option()  # Obtiene la opción seleccionada por el usuario desde la vista
            if choice == '1':
                origin = self.view.get_origin_input()  # Obtiene la origen deseada desde la vista
                filtered_players = self.model.players_by_origin(origin)  # Filtra los jugadores por origen
                self.view.show_player_list(filtered_players)  # Muestra la lista filtrada de jugadores
                break  # Sale del bucle while
            elif choice == '2':
                position = self.view.get_position_input()  # Obtiene la posición deseada desde la vista
                filtered_players = self.model.female_players_by_position(position)  # Filtra los jugadores por posición
                self.view.show_player_list(filtered_players)  # Muestra la lista filtrada de jugadores
                break  # Sale del bucle while
            elif choice == '3':
                recognition = self.view.get_recognition_input()  # Obtiene el logro deseado desde la vista
                filtered_players = self.model.players_by_recognition(recognition)  # Filtra los jugadores por logro
                self.view.show_player_list(filtered_players)  # Muestra la lista filtrada de jugadores
                break  # Sale del bucle while
            else:
                self.view.show_message("Opción inválida, intente de nuevo.")  # Muestra un mensaje de error para opciones inválidas
