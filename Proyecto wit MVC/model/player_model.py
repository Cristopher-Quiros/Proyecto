import datetime
import json

class PlayerModel:
    def __init__(self, data_file):
        self.data_file = data_file

    def read_data(self, name='players_data.json'):
        try:
            with open(name, 'r+') as file:
                data = json.load(file)
                return data
        except FileNotFoundError:
            return []
        except json.JSONDecodeError:
            return []

    def write_data(self, data, name='players_data.json'):
        print("Writing data to file...")
        with open(name, 'w+') as file:
            json.dump(data, file, indent=4)
        print("Data written to file successfully.")

    def add_player(self, player_data):
        players = self.read_data()
        players.append(player_data)
        self.write_data(players)

    def get_player(self, player_id):
        players = self.read_data()
        for player in players:
            if player['id'] == player_id:
                return player
        return None

    def update_player(self, updated_players):
        print("Updating player data...")
        players = self.read_data()

        for updated_player in updated_players:
            updated_player_id = updated_player.get('id')  # Obtener el ID del jugador actualizado
            if updated_player_id is not None:
                for i, player in enumerate(players):
                    if player['id'] == updated_player_id:
                        # Actualizar los campos del jugador con los datos actualizados
                        for key, value in updated_player.items():
                            if key in player:
                                player[key] = value
                        break

        if players:
            print("Player data updated successfully.")
            return True
        else:
            print("Error: players list is empty.")
            return False

    def delete_player(self, player_id):
        players = self.read_data()
        for player in players:
            if player['id'] == player_id:
                players.remove(player)
                self.write_data(players)
                return True
        return False

    def get_players(self):
        players = self.read_data()
        if not players:
            print("No hay información de jugadores disponible.")
        return players

    # Agrega más métodos aquí según sea necesario para otras operaciones CRUD

    def filter_players_by_origin(self, origin):
        players = self.read_data()
        return [player for player in players if player.get('origin') == origin]

    def filter_players_by_position(self, position):
        players = self.read_data()
        return [player for player in players if player.get('position') == position]

    def filter_players_by_recognition(self, recognition):
        players = self.read_data()
        return [player for player in players if player.get('achievements') == recognition]

    def count_players_by_origin(self, origin):
        players = self.read_data()
        count = sum(1 for player in players if player['origin'] == origin)
        return f"Number of players from {origin}: {count}"

    def players_in_age_range(self, min_age, max_age):
        current_year = datetime.datetime.now().year
        players = self.read_data()
        return [player for player in players if
                min_age <= current_year - int(player['date_of_birth'].split('-')[0]) <= max_age]

    def count_players_by_height_and_gender(self, height, gender):
        players = self.read_data()
        count = sum(1 for player in players if player['height'] == height and player['gender'] == gender)
        return f"Number of players with height {height}m and gender {gender}: {count}"

    def players_from_specific_club(self, club):
        players = self.read_data()
        return [player for player in players if player['club'] == club]

    def count_female_players_by_position(self, position):
        players = self.read_data()
        count = sum(1 for player in players if player['gender'] == 'Female' and player['position'] == position)
        return f"Number of female players in position {position}: {count}"

    def top_10_players_by_height_and_agility(self):
        players = self.read_data()
        top_players = sorted(players, key=lambda x: (x['height'], x['agility']), reverse=True)[:10]
        return top_players

    def count_players_in_speed_range(self, min_speed, max_speed):
        players = self.read_data()
        count = sum(1 for player in players if min_speed <= player['speed'] <= max_speed)
        return f"Number of players with speed between {min_speed} and {max_speed}: {count}"

    def average_ball_control_by_position(self, position):
        players = self.read_data()
        position_players = [player for player in players if player['position'] == position]
        if position_players:
            ball_controls = [player['ball_control'] for player in position_players]
            average_ball_control = sum(ball_controls) / len(ball_controls)
            return f"Average ball control for players in position {position}: {average_ball_control}"
        else:
            return None

    def show_stats_by_id(self, player_id):
        players = self.read_data()
        for player in players:
            if player['id'] == player_id:
                return player
        return None

    def compare_players_by_position(self, position):
        players = self.read_data()
        players_in_position = [player for player in players if player['position'] == position]
        if players_in_position:
            return players_in_position
        else:
            return None

