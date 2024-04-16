import datetime
import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QMessageBox, QInputDialog, QAction, QMenu

class PlayerView(QWidget):
    def __init__(self, data_file):
        super().__init__()
        self.data_file = data_file
        self.controller = None
        self.setWindowTitle('Player Management System')
        self.layout = QVBoxLayout(self)

        # Botones básicos
        self.add_button = QPushButton('Añadir Jugador')
        self.add_button.clicked.connect(self.add_player)
        self.layout.addWidget(self.add_button)

        self.read_button = QPushButton('Consultar Jugador')
        self.read_button.clicked.connect(self.read_player)
        self.layout.addWidget(self.read_button)

        self.update_button = QPushButton('Actualizar Jugador')
        self.update_button.clicked.connect(self.update_player)
        self.layout.addWidget(self.update_button)

        self.delete_button = QPushButton('Borrar Jugador')
        self.delete_button.clicked.connect(self.delete_player)
        self.layout.addWidget(self.delete_button)

        # Botón para mostrar el menú de opciones
        self.show_menu_button = QPushButton('Opciones de Jugador')
        self.show_menu_button.setMenu(self.create_menu())
        self.layout.addWidget(self.show_menu_button)

        # Botón para mostrar opciones avanzadas
        self.advanced_button = QPushButton('Consultas Avanzadas')
        self.advanced_button.clicked.connect(self.show_advanced_queries_menu)
        self.layout.addWidget(self.advanced_button)

        self.exit_button = QPushButton('Salir')
        self.exit_button.clicked.connect(self.exit_application)
        self.layout.addWidget(self.exit_button)

        self.setLayout(self.layout)

    def set_controller(self, controller):
        self.controller = controller

    def handle_cancel(self):
        self.show_message("Operación cancelada.")

    def create_menu(self):
        menu = QMenu()
        menu.addAction("Mostrar Lista de Jugadores", lambda: self.show_player_list(self.controller.model.get_players()))
        menu.addAction("Filtrar por Origen", self.filter_players_by_origin)
        menu.addAction("Filtrar por Posición", self.filter_players_by_position)
        menu.addAction("Filtrar por Reconocimientos", self.filter_players_by_recognition)
        return menu

    def exit_application(self):
        QApplication.quit()  # Cerrar la aplicación

    # Metodo CRUD
    def add_player(self):
        player_data = self.get_player_data()
        if player_data is not None:  # Verifica si se canceló la operación
            if not self.controller.model.get_player(player_data['id']):
                self.controller.model.add_player(player_data)
                self.show_message("Jugador añadido exitosamente.")
            else:
                self.show_message("El jugador ya existe!.")
        else:
            self.show_message("Operación cancelada.")

    def read_player(self):
        player_id = self.get_player_id_input()
        if player_id is not None:  # Verificar si se ingresó un ID de jugador válido
            player = self.controller.model.get_player(player_id)
            if player:
                self.show_player_info(player)  # Mostrar la información del jugador en la vista
                self.controller.show_menu()  # Llamar a show_menu() después de mostrar la información del jugador
            else:
                self.show_message("No hay ningún jugador con ese ID.")
        else:
            self.show_message("Operación cancelada.")  # Mostrar un mensaje si se cancela la operación

    def update_player(self):
        player_id = self.get_player_id_input()
        if player_id is not None:
            updated_player_data = self.get_player_data()  # Obtener los datos actualizados del jugador
            updated_player_data['id'] = player_id  # Asegurar que el ID del jugador esté presente en los datos actualizados
            success = self.controller.update_player(updated_player_data)  # Llamar al método update_player del controlador
            if success:
                self.show_message("Jugador actualizado exitosamente.")
            else:
                self.show_message("No se encontró ningún jugador con ese ID.")
        else:
            self.show_message("Operación cancelada.")

    def delete_player(self):
        player_id = self.get_player_id_input()
        success = self.controller.model.delete_player(player_id)
        if success:
            self.show_message("Jugador borrado exitosamente!.")
        else:
            self.show_message("Error al borrar el jugador!.")

    # Opcion de mostrar jugadores y sus respectivos filtros

    def get_origin_input(self):
        origin, ok = QInputDialog.getText(self, 'Origin Input', 'Enter the origin of the player:')
        if ok:
            # Check if the value contains only letters, spaces, and commas, and is in uppercase or lowercase format
            if all(char.isalpha() or char.isspace() or char == ',' for char in origin) and origin.strip():
                return origin.strip().capitalize()  # Convert the first letter of each word to uppercase
            else:
                self.show_message("Invalid input. Please enter only alphabetical characters, spaces, and commas.")
        else:
            pass  # Ignorar la cancelación del diálogo de entrada y continuar ejecutando el programa

    def get_position_input(self):
        position, ok = QInputDialog.getText(self, 'Position Input', 'Enter the position of the player:')
        if ok:
            return position
        else:
            pass  # Ignorar la cancelación del diálogo de entrada y continuar ejecutando el programa
    def get_recognition_input(self):
        recognition, ok = QInputDialog.getInt(self, 'Recognition Input', 'Enter the recognition of the player:')
        if ok:
            return recognition
        else:
            QMessageBox.information(self, "Operación cancelada", "La operación ha sido cancelada.")

    def show_player_info(self, player):
        player_info = f"ID: {player['id']}\nName: {player['name']}\nClub: {player['club']}\n\n{self.format_stats(player)}"
        self.show_message(player_info)
        self.controller.show_menu()  # Llamar a show_menu() después de mostrar la información del jugador

    def show_player_list(self, players):
        if players:
            player_info = "\n".join(
                [f"ID: {player['id']}, Name: {player['name']}, Club: {player['club']}" for player in players])
            self.show_message(player_info)
        else:
            self.show_message("No se encontraron jugadores.")

    def filter_players_by_origin(self):
        origin = self.get_origin_input()
        if origin:
            filtered_players = self.controller.model.filter_players_by_origin(origin)
            if filtered_players:
                self.show_player_list(filtered_players)
            else:
                self.show_message("No hay jugadores con ese lugar de Origen.")
        else:
            self.show_message("Ingresa un lugar de Origen valido.")

    def filter_players_by_position(self):
        position = self.get_position_input()
        if position:
            filtered_players = self.controller.model.filter_players_by_position(position)
            if filtered_players:
                self.show_player_list(filtered_players)
            else:
                self.show_message("No hay jugadores con esa posición en el campo.")
        else:
            self.show_message("Ingresa una posición valida.")

    def filter_players_by_recognition(self):
        recognition, ok = QInputDialog.getInt(self, 'Recognition Input', 'Ingresa el numero minimo de reconocimientos:')
        if ok:
            filtered_players = self.controller.model.filter_players_by_recognition(recognition)
            if filtered_players:
                self.show_player_list(filtered_players)
            else:
                self.show_message("No hay jugadores con esa cantidad de reconocimientos.")
        else:
            self.show_message("Ingresa un numero valido!.")


    # Consultas Avanzadas

    def show_advanced_queries_menu(self):
        menu = QMenu()
        menu.addAction("Cantidad de Jugadores Por Origen", self.count_players_by_origin)
        menu.addAction("Jugadores en un rango de edad", self.players_in_age_range)
        menu.addAction("Cantidad de jugadores por altura y genero", self.count_players_by_height_and_gender)
        menu.addAction("Jugadores de un club específico", self.players_from_specific_club)
        menu.addAction("Cantidad de jugadoras por posición", self.count_female_players_by_position)
        menu.addAction("Top 10 Jugadores por altura y agilidad", self.top_10_players_by_height_and_agility)
        menu.addAction("Cantidad de Jugadores por rango de velocidad", self.count_players_in_speed_range)
        menu.addAction("Promedio de Control de Balón por posición", self.average_ball_control_by_position)
        menu.exec_(self.advanced_button.mapToGlobal(self.advanced_button.rect().bottomLeft()))

    # Filtros de consultas avanzadas
    def count_players_by_origin(self):
        origin = self.get_origin_input()
        if origin:
            count = self.controller.model.count_players_by_origin(origin)
            self.show_message(f"{count}")

    def players_in_age_range(self):
        min_age, ok_min = QInputDialog.getInt(self, 'Age Input', 'Enter minimum age:')
        if ok_min:
            max_age, ok_max = QInputDialog.getInt(self, 'Age Input', 'Enter maximum age:')
            if ok_max:
                filtered_players = self.controller.model.players_in_age_range(min_age, max_age)
                if filtered_players:
                    self.show_player_list(filtered_players)
                else:
                    self.show_message("No players found in the specified age range.")
            else:
                self.show_message("Operation canceled.")
        else:
            self.show_message("Operation canceled.")

    def count_players_by_height_and_gender(self):
        height, ok_height = QInputDialog.getDouble(self, 'Height Input', 'Enter player\'s height:')
        if not ok_height:
            self.show_message("Operation canceled.")
            return

        gender, ok_gender = QInputDialog.getItem(self, 'Gender Input', 'Select player\'s gender:', ['Male', 'Female'],
                                                 0, False)
        if not ok_gender:
            self.show_message("Operation canceled.")
            return

        count = self.controller.model.count_players_by_height_and_gender(height, gender)
        self.show_message(f"Number of {gender} players with height {height}m: {count}")

    def players_from_specific_club(self):
        club, ok_club = QInputDialog.getText(self, 'Club Input', 'Enter the club name:')
        if not ok_club:
            self.show_message("Operation canceled.")
            return

        count = self.controller.model.players_from_specific_club(club)
        self.show_message(f"Number of players from {club}: {count}")

    def count_female_players_by_position(self):
        position, ok_position = QInputDialog.getText(self, 'Position Input', 'Enter position:')
        if not ok_position:
            self.show_message("Operation canceled.")
            return

        count = self.controller.model.count_female_players_by_position(position)
        self.show_message(f"Number of female players in {position} position: {count}")
    def top_10_players_by_height_and_agility(self):
        top_players = self.controller.model.top_10_players_by_height_and_agility()
        if top_players:
            player_list = [f"Name: {player['name']}, Height: {player['height']}, Agility: {player['agility']}" for player in top_players]
            self.show_message("\n".join(player_list))
        else:
            self.show_message("No players found.")

    def count_players_in_speed_range(self):
        min_speed, ok_min_speed = QInputDialog.getInt(self, 'Speed Input', 'Enter minimum speed:')
        if not ok_min_speed:
            self.show_message("Operation canceled.")
            return

        max_speed, ok_max_speed = QInputDialog.getInt(self, 'Speed Input', 'Enter maximum speed:')
        if not ok_max_speed:
            self.show_message("Operation canceled.")
            return

        count = self.controller.model.count_players_in_speed_range(min_speed, max_speed)
        self.show_message(f"Number of players with speed between {min_speed} and {max_speed}: {count}")

    def average_ball_control_by_position(self):
        position, ok_position = QInputDialog.getText(self, 'Position Input', 'Enter position:')
        if not ok_position:
            self.show_message("Operation canceled.")
            return

        average = self.controller.model.average_ball_control_by_position(position)
        self.show_message(f"Average ball control for players in {position} position: {average}")


    def show_message(self, message):
        QMessageBox.information(self, "Information", message)

    # Informacion para agregar un jugador en el CRUD
    def get_player_data(self):
        player_data = {}
        player_data['id'] = self.validate_int_input("ID of the player: ")
        player_data['name'] = self.validate_text_input("Name of the player: ")
        player_data['date_of_birth'] = self.validate_date_input("Date of birth (YYYY-MM-DD): ")
        player_data['origin'] = self.validate_text_input("Origin of the player: ")
        player_data['gender'] = self.validate_gender_input("Gender (Male/Female): ")
        player_data['height'] = self.validate_float_input("Height of the player (in meters): ")
        player_data['weight'] = self.validate_float_input("Weight of the player (in kg): ")
        player_data['position'] = self.validate_text_input("Position in field of the player: ")
        player_data['club'] = self.validate_text_input("Club of the player: ")
        player_data['achievements'] = self.validate_int_input("Achievements of the player: ")
        player_data['acceleration'] = self.validate_int_input("Acceleration of the player: ")
        player_data['short_passes'] = self.validate_int_input("Short Passes: ")
        player_data['power_of_shot'] = self.validate_int_input("Power of Shot: ")
        player_data['long_passes'] = self.validate_int_input("Long Passes: ")
        player_data['speed'] = self.validate_int_input("Speed: ")
        player_data['agility'] = self.validate_int_input("Agility: ")
        player_data['resistence'] = self.validate_int_input("Resistence: ")
        player_data['jump'] = self.validate_int_input("Jump: ")
        player_data['dribbling'] = self.validate_int_input("Dribbling: ")
        player_data['ball_control'] = self.validate_int_input("Ball Control: ")
        return player_data

    # Consultar ID de un jugador
    def get_player_id_input(self):
        while True:
            player_id, ok = QInputDialog.getInt(self, 'Player ID', 'Enter the ID of the player:')
            if ok:
                return player_id
            else:
                return None  # Salir si se cancela la entrada de ID

    # Validaciones
    def validate_text_input(self, message):
        while True:
            value, ok = QInputDialog.getText(self, 'Text Input', message)
            if ok:
                # Check if the value contains only letters, spaces, and commas, and is in uppercase or lowercase format
                if all(char.isalpha() or char.isspace() or char == ',' for char in value) and value.strip():
                    return value.strip().capitalize()  # Convert the first letter of each word to uppercase
                else:
                    self.show_message("Invalid input. Please enter only alphabetical characters, spaces, and commas.")
            else:
                sys.exit()

    def validate_int_input(self, message):
        while True:
            value, ok = QInputDialog.getInt(self, 'Integer Input', message)
            if ok:
                if 0 <= value <= 100:  # Check if the value is between 0 and 100 (inclusive)
                    return value
                else:
                    self.show_message("Invalid input. Please enter a number between 0 and 100.")
            else:
                sys.exit()
    def validate_float_input(self, message):
        while True:
            value, ok = QInputDialog.getText(self, 'Float Input', message)
            if ok:
                try:
                    # Check if the input includes the unit (meters or kg)
                    if "m" in value.lower():
                        float_value = float(value.lower().replace("m", "").strip())
                        if float_value >= 0:  # Check if the value is non-negative
                            return float_value
                        else:
                            self.show_message("Invalid input. Please enter a non-negative number.")
                    elif "kg" in value.lower():
                        float_value = float(value.lower().replace("kg", "").strip())
                        if float_value >= 0:  # Check if the value is non-negative
                            return float_value
                        else:
                            self.show_message("Invalid input. Please enter a non-negative number.")
                    else:
                        self.show_message("Invalid input format. Please include the unit (meters or kg).")
                except ValueError:
                    self.show_message(
                        "Invalid input. Please enter a valid floating-point number with the unit (meters or kg).")
            else:
                sys.exit()

    def validate_date_input(self, message):
        while True:
            value, ok = QInputDialog.getText(self, 'Date Input', message)
            if ok:
                try:
                    datetime.datetime.strptime(value, "%Y-%m-%d")
                    return value
                except ValueError:
                    self.show_message("Invalid date format. Please enter the date in the correct format (YYYY-MM-DD).")
            else:
                sys.exit()

    def validate_gender_input(self, message):
        while True:
            items = ['Male', 'Female']
            item, ok = QInputDialog.getItem(self, 'Gender Input', message, items, 0, False)
            if ok:
                return item
            else:
                sys.exit()
    # Formato en que aparecen las estadisticas
    def format_stats(self, player):
        stats = [
            f"Acceleration: {player['acceleration']}",
            f"Short Passes: {player['short_passes']}",
            f"Power of Shot: {player['power_of_shot']}",
            f"Long Passes: {player['long_passes']}",
            f"Speed: {player['speed']}",
            f"Agility: {player['agility']}",
            f"Resistence: {player['resistence']}",
            f"Jump: {player['jump']}",
            f"Dribbling: {player['dribbling']}",
            f"Ball Control: {player['ball_control']}"
        ]
        return "\n".join(stats)
