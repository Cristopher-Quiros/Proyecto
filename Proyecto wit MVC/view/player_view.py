import datetime

class PlayerView:
    def show_menu(self):
        print("\nMenú Principal:")
        print("1. Insertar un nuevo jugador")
        print("2. Leer información de un jugador")
        print("3. Modificar datos de un jugador")
        print("4. Eliminar un jugador de la base de datos")
        print("5. Visualizar la Lista de Jugadores")
        print("6. Estadísticas de Jugadores")
        print("7. Consultas Avanzadas")
        print("8. Salir del sistema")
        return input("Seleccione una opción: ")

    def get_player_data(self):
        player_data = {}
        player_data['id'] = self.validate_int_input("ID del jugador: ")
        player_data['name'] = self.validate_text_input("Nombre del jugador: ")
        player_data['date_of_birth'] = self.validate_date_input("Fecha de nacimiento (YYYY-MM-DD): ")
        player_data['origin'] = self.validate_text_input("Origen del jugador: ")
        player_data['gender'] = self.validate_gender_input("Género (Masculino/Femenino): ")
        player_data['height'] = self.validate_float_input("Altura del jugador (en metros): ")
        player_data['weight'] = self.validate_float_input("Peso del jugador (en kg): ")
        player_data['position'] = self.validate_text_input("Posición en campo del jugador: ")
        player_data['club'] = self.validate_text_input("Club militante del jugador: ")
        player_data['achievements'] = self.validate_int_input("Reconocimientos del jugador: ")
        return player_data

    def get_player_id(self):
        while True:
            try:
                player_id = int(input("Ingrese el ID del jugador: "))
                return player_id
            except ValueError:
                print("El ID debe ser un número entero. Inténtelo de nuevo.")

    def show_player_info(self, player_info):
        print("Información del Jugador:")
        print(f"ID: {player_info.get('id', 'N/A')}")
        print(f"Nombre: {player_info.get('name', 'N/A')}")
        print(f"Fecha de nacimiento: {player_info.get('date_of_birth', 'N/A')}")
        print(f"Origen: {player_info.get('origin', 'N/A')}")
        print(f"Género: {player_info.get('gender', 'N/A')}")
        print(f"Altura: {player_info.get('height', 'N/A')} m")
        print(f"Peso: {player_info.get('weight', 'N/A')} kg")
        print(f"Posición en campo: {player_info.get('position', 'N/A')}")
        print(f"Club Militante: {player_info.get('club', 'N/A')}")
        print(f"Reconocimientos: {player_info.get('achievements', 'N/A')}")

    def show_message(self, message):
        print(message)

    def show_player_list(self, player_list):
        print("\nLista de Jugadores:")
        for player in player_list:
            print(f"ID: {player['id']}, Nombre: {player['name']}, Club: {player['club']}")

    def show_players_by_origin(self, count):
        print(f"Cantidad de jugadores por origen: {count}")

    def show_players_in_age_range(self, players):
        print("\nJugadores en el rango de edad:")
        for player in players:
            print(player)

    def show_players_by_height_and_gender(self, count):
        print(f"Cantidad de jugadores por altura y género: {count}")

    def show_players_by_club(self, players):
        print("\nJugadores del club específico:")
        for player in players:
            print(player)

    def show_female_players_by_position(self, count):
        print(f"Cantidad de jugadoras por posición en el campo: {count}")

    def show_top_players_by_height_and_agility(self, top_players):
        print("\nTop 10 jugadores por altura y agilidad:")
        for player in top_players:
            print(player)

    def show_players_by_speed_range(self, count):
        print(f"Cantidad de jugadores por rango de velocidad: {count}")

    def show_average_ball_control_by_position(self, average):
        print(f"Promedio de control de balón para la posición específica: {average}")

    def validate_text_input(self, message):
        while True:
            value = input(message)
            if value.replace(" ", "").isalpha():
                return value
            else:
                print("Entrada inválida. Por favor, ingrese solo caracteres alfabéticos y espacios.")

    def validate_int_input(self, message):
        while True:
            value = input(message)
            if value.isdigit():
                return int(value)
            else:
                print("Entrada inválida. Por favor, ingrese solo números enteros.")

    def validate_float_input(self, message):
        while True:
            value = input(message)
            try:
                float_value = float(value)
                return float_value
            except ValueError:
                print("Entrada inválida. Por favor, ingrese un número válido.")

    def validate_date_input(self, message):
        while True:
            value = input(message)
            try:
                datetime.datetime.strptime(value, "%Y-%m-%d")
                return value
            except ValueError:
                print("Formato de fecha inválido. Por favor, ingrese la fecha en el formato correcto (YYYY-MM-DD).")

    def validate_gender_input(self, message):
        while True:
            value = input(message)
            if value.lower() in ['masculino', 'femenino']:
                return value.capitalize()
            else:
                print("Género inválido. Por favor, ingrese 'Masculino' o 'Femenino'.")
