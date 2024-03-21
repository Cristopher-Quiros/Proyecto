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
        players.append(player_data)
        self.write_data(players)

    def get_players(self):
        return self.read_data()

    # Consulta avanzada 1: Mostrar cantidad de jugadores por origen
    def players_by_origin(self, origin):
        players = self.read_data()
        return len([player for player in players if player['origin'] == origin])

    # Consulta avanzada 2: Mostrar jugadores en un rango de edad
    def players_by_age_range(self, min_age, max_age):
        players = self.read_data()
        return [player for player in players if min_age <= player['age'] <= max_age]

    # Consulta avanzada 3: Mostrar cantidad de jugadores por altura y género
    def players_by_height_and_gender(self, height, gender):
        players = self.read_data()
        return len([player for player in players if player['height'] == height and player['gender'] == gender])

    # Consulta avanzada 4: Mostrar jugadores de un club específico
    def players_by_club(self, club):
        players = self.read_data()
        return [player for player in players if player['club'] == club]

    # Consulta avanzada 5: Mostrar cantidad de jugadoras por posición en el campo
    def female_players_by_position(self, position):
        players = self.read_data()
        return len([player for player in players if player['gender'] == 'Femenino' and player['position'] == position])

    # Consulta avanzada 6: Mostrar top 10 jugadores por altura y agilidad
    def top_players_by_height_and_agility(self):
        players = self.read_data()
        top_players = sorted(players, key=lambda x: (x['height'], x['agility']), reverse=True)[:10]
        return top_players

    # Consulta avanzada 7: Mostrar cantidad de jugadores por velocidad en un rango específico
    def players_by_speed_range(self, min_speed, max_speed):
        players = self.read_data()
        return len([player for player in players if min_speed <= player['speed'] <= max_speed])

    # Consulta avanzada 8: Calcular promedio de control de balón para una posición específica
    def average_ball_control_by_position(self, position):
        players = self.read_data()
        players_in_position = [player for player in players if player['position'] == position]
        if players_in_position:
            total_ball_control = sum(player['ball_control'] for player in players_in_position)
            return total_ball_control / len(players_in_position)
        else:
            return 0