import json

class PlayerModel:
    def __init__(self, data_file):
        self._data_file = data_file

    def read_data(self):
        try:
            with open(self._data_file, 'r') as file:
                return json.load(file)
        except FileNotFoundError:
            return []

    def write_data(self, data):
        with open(self._data_file, 'w') as file:
            json.dump(data, file, indent=4)

    def add_player(self, player_data):
        players = self.read_data()
        player_ids = [player['id'] for player in players]
        if player_data['id'] in player_ids:
            print("¡Error! El jugador ya existe.")
            return False
        elif any(player == player_data for player in players):
            print("¡Error! Ya existe un jugador con la misma información.")
            return False
        else:
            players.append(player_data)
            self.write_data(players)
            return True

    def get_players(self):
        return self.read_data()

    def get_player(self, player_id):
        players = self.read_data()
        for player in players:
            if player['id'] == player_id:
                return player
        return None

    def update_player(self, player_id, player_data):
        players = self.read_data()
        for player in players:
            if player['id'] == player_id:
                player.update(player_data)
                self.write_data(players)
                return True
        print("No se encontró ningún jugador con ese ID.")
        return False

    def delete_player(self, player_id):
        players = self.read_data()
        updated_players = [player for player in players if player['id'] != player_id]
        if len(updated_players) < len(players):
            self.write_data(updated_players)
            return True
        print("No se encontró ningún jugador con ese ID.")
        return False

    def player_exists(self, player_data):
        players = self.read_data()
        player_ids = [player['id'] for player in players]
        if player_data in player_ids:
            print("¡Error! El jugador ya existe.")
            return True
        else:
            return False

    def players_by_origin(self, origin):
        players = self.read_data()
        return [player for player in players if player['origin'] == origin]

    def players_by_position(self, position):
        players = self.read_data()
        return [player for player in players if player['position'] == position]

    def players_by_recognition(self, recognition):
        players = self.read_data()
        return [player for player in players if player['achievements'] == recognition]