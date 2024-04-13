import datetime
import json

class PlayerModel:
    def __init__(self, data_file):
        self.data_file = data_file

    def read_data(self):
        try:
            with open(self.data_file, 'r') as file:
                return json.load(file)
        except FileNotFoundError:
            return []

    def write_data(self, data):
        with open(self.data_file, 'w') as file:
            json.dump(data, file, indent=4)

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

    def update_player(self, player_id, new_player_data):
        players = self.read_data()
        for player in players:
            if player['id'] == player_id:
                player.update(new_player_data)
                self.write_data(players)
                return True
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
        return self.read_data()

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