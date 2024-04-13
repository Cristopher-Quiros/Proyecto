import json  # Importa el módulo json para trabajar con datos JSON

class PlayerModel:  # Define la clase PlayerModel
    def __init__(self, data_file):
        self._data_file = data_file  # Inicializa el atributo _data_file con el nombre del archivo de datos

    # Lee los datos del archivo JSON y los carga en una lista
    def read_data(self):
        try:
            with open(self._data_file, 'r') as file:
                return json.load(file)  # Carga los datos del archivo JSON y los retorna
        except FileNotFoundError:
            return []  # Retorna una lista vacía si el archivo no existe

    def write_data(self, data):
        with open(self._data_file, 'w') as file:
            json.dump(data, file, indent=4)  # Escribe los datos en el archivo JSON con formato indentado

    # Agrega un nuevo jugador a la lista de jugadores si no existe ya en la lista
    def add_player(self, player_data):
        players = self.read_data()  # Obtiene la lista actual de jugadores
        player_ids = [player['id'] for player in players]  # Obtiene una lista de todos los IDs de los jugadores existentes
        if player_data['id'] in player_ids:  # Comprueba si el ID del nuevo jugador ya existe
            print("¡Error! El jugador ya existe.")  # Imprime un mensaje de error
            return False  # Devuelve False para indicar que no se pudo agregar el jugador
        elif any(player == player_data for player in players):  # Comprueba si hay algún jugador existente con la misma información
            print("¡Error! Ya existe un jugador con la misma información.")  # Imprime un mensaje de error
            return False  # Devuelve False para indicar que no se pudo agregar el jugador
        else:
            players.append(player_data)  # Agrega el nuevo jugador a la lista de jugadores
            self.write_data(players)  # Escribe la lista actualizada de jugadores en el archivo
            return True  # Devuelve True para indicar que el jugador se agregó correctamente

    # Devuelve todos los jugadores
    def get_players(self):
        return self.read_data()  # Devuelve la lista de jugadores

    # Devuelve un jugador específico según su player_id
    def get_player(self, player_id):
        players = self.read_data()  # Obtiene la lista actual de jugadores
        for player in players:
            if player['id'] == player_id:  # Comparación sin conversión a cadena
                return player  # Devuelve el jugador encontrado
        return None  # Devuelve None si no se encuentra el jugador

    # Actualiza la información de un jugador existente según su player_id
    def update_player(self, player_id, player_data):
        players = self.read_data()  # Obtiene la lista actual de jugadores
        for player in players:
            if player['id'] == player_id:  # Comprueba si el ID del jugador coincide
                player.update(player_data)  # Actualiza la información del jugador
                self.write_data(players)  # Escribe la lista actualizada de jugadores en el archivo
                return True  # Devuelve True para indicar que el jugador se actualizó correctamente
        print("No se encontró ningún jugador con ese ID.")  # Imprime un mensaje de error si no se encuentra el jugador
        return False  # Devuelve False para indicar que no se pudo actualizar el jugador

    # Elimina un jugador existente según su player_id
    def delete_player(self, player_id):
        players = self.read_data()  # Obtiene la lista actual de jugadores
        updated_players = [player for player in players if player['id'] != player_id]  # Crea una nueva lista sin el jugador a eliminar
        if len(updated_players) < len(players):  # Comprueba si se eliminó algún jugador
            self.write_data(updated_players)  # Escribe la lista actualizada de jugadores en el archivo
            return True  # Devuelve True para indicar que el jugador se eliminó correctamente
        print("No se encontró ningún jugador con ese ID.")  # Imprime un mensaje de error si no se encuentra el jugador
        return False  # Devuelve False para indicar que no se pudo eliminar el jugador

    # Verifica si un jugador ya existe en la lista
    def player_exists(self, player_data):
        players = self.read_data()  # Obtiene la lista actual de jugadores
        player_ids = [player['id'] for player in players]  # Obtiene una lista de todos los IDs de los jugadores existentes
        if player_data in player_ids:  # Comprueba si el ID del jugador ya existe
            print("¡Error! El jugador ya existe.")  # Imprime un mensaje de error
            return True  # Devuelve True para indicar que el jugador ya existe
        else:
            return False  # Devuelve False para indicar que el jugador no existe

    # Devuelve una lista de jugadores con la misma origin
    def players_by_origin(self, origin):
        players = self.read_data()  # Obtiene la lista actual de jugadores
        return [player for player in players if player['origin'] == origin]  # Filtra los jugadores con la misma origen

    # Devuelve una lista de jugadores con la misma position
    def players_by_position(self, position):
        players = self.read_data()  # Obtiene la lista actual de jugadores
        return [player for player in players if player['position'] == position]  # Filtra los jugadores con la misma posición

    # Devuelve una lista de jugadores con los mismos achievements
    def players_by_recognition(self, recognition):
        players = self.read_data()  # Obtiene la lista actual de jugadores
        return [player for player in players if player['achievements'] == recognition]  # Filtra los jugadores con los mismos logros

    def get_player_stats_by_id(self, player_id):
        # Obtiene las estadísticas de un jugador por su ID
        player = self.get_player(player_id)  # Obtiene la información del jugador por su ID
        if player:
            return {key: value for key, value in player.items() if
                    key not in ['id', 'name', 'date_of_birth', 'origin', 'gender', 'height', 'weight', 'position',
                                'club', 'achievements']}  # Retorna las estadísticas del jugador
        else:
            return None  # Retorna None si el jugador no se encuentra

    def compare_players_stats_by_position(self, position):
        # Compara las estadísticas de los jugadores que juegan en la misma posición
        players = self.players_by_position(position)  # Obtiene la lista de jugadores que juegan en la misma posición
        stats_comparison = {}  # Inicializa un diccionario para almacenar las estadísticas de comparación
        for player in players:
            stats_comparison[player['name']] = {key: value for key, value in player.items() if
                                                key not in ['id', 'name', 'date_of_birth', 'origin', 'gender', 'height',
                                                            'weight', 'position', 'club',
                                                            'achievements']}  # Agrega las estadísticas del jugador al diccionario
        return stats_comparison  # Retorna el diccionario de comparación de estadísticas

    def get_player_statistics(self, player_id):
        players = self.read_data()  # Obtiene la lista actual de jugadores
        for player in players:
            if player['id'] == player_id:  # Comprueba si el ID del jugador coincide
                player_stats = {key: value for key, value in player.items() if key not in ['id', 'name']}  # Obtiene las estadísticas del jugador
                return player_stats  # Devuelve las estadísticas del jugador si se encuentra
        return None  # Devuelve None si no se encuentra el jugador
