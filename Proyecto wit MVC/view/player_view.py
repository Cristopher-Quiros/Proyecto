import datetime  # Importa el módulo datetime para trabajar con fechas
import json  # Importa el módulo json para leer y escribir archivos JSON

class PlayerView:
    def __init__(self, data_file):
        # Inicializa la vista con el archivo de datos
        self._data_file = data_file

    def read_data(self):
        # Lee los datos del archivo JSON
        try:
            with open(self._data_file, 'r') as file:
                return json.load(file)  # Carga los datos del archivo JSON y los retorna
        except FileNotFoundError:
            return []  # Retorna una lista vacía si el archivo no existe

    def write_data(self, data):
        # Escribe los datos en el archivo JSON
        with open(self._data_file, 'w') as file:
            json.dump(data, file, indent=4)  # Escribe los datos en el archivo JSON con formato indentado

    def show_menu(self):
        # Muestra el menú principal
        print("\nMenú Principal:")
        print("1. Insertar un nuevo jugador")
        print("2. Leer información de un jugador")
        print("3. Modificar datos de un jugador")
        print("4. Eliminar un jugador de la base de datos")
        print("5. Visualizar la Lista de Jugadores")
        print("6. Estadísticas de Jugadores")
        print("7. Consultas Avanzadas")
        print("8. Salir del sistema")
        return input("Seleccione una opción: ")  # Retorna la opción seleccionada por el usuario

    def get_player_data(self):
        # Obtiene los datos de un nuevo jugador
        player_data = {}
        player_data['id'] = self.validate_int_input("ID del jugador: ")  # Valida y obtiene el ID del jugador
        player_data['name'] = self.validate_text_input("Nombre del jugador: ")  # Valida y obtiene el nombre del jugador
        player_data['date_of_birth'] = self.validate_date_input("Fecha de nacimiento (YYYY-MM-DD): ")  # Valida y obtiene la fecha de nacimiento del jugador
        player_data['origin'] = self.validate_text_input("Origen del jugador: ")  # Valida y obtiene el origen del jugador
        player_data['gender'] = self.validate_gender_input("Género (Masculino/Femenino): ")  # Valida y obtiene el género del jugador
        player_data['height'] = self.validate_float_input("Altura del jugador (en metros): ")  # Valida y obtiene la altura del jugador
        player_data['weight'] = self.validate_float_input("Peso del jugador (en kg): ")  # Valida y obtiene el peso del jugador
        player_data['position'] = self.validate_text_input("Posición en campo del jugador: ")  # Valida y obtiene la posición en campo del jugador
        player_data['club'] = self.validate_text_input("Club militante del jugador: ")  # Valida y obtiene el club del jugador
        player_data['achievements'] = self.validate_int_input("Reconocimientos del jugador: ")  # Valida y obtiene los reconocimientos del jugador
        print("Estadisticas del jugador (Solo en numeros):")
        player_data['acceleration'] = self.validate_int_input("Velocidad del jugador: ")
        player_data['short_passes'] = self.validate_int_input("Pases Cortos: ")
        player_data['power_of_shot'] = self.validate_int_input("Poder de Tiro: ")
        player_data['long_passes'] = self.validate_int_input("Pases Largos: ")
        player_data['speed'] = self.validate_int_input("Velocidad: ")
        player_data['jump'] = self.validate_int_input("Poder de Salto: ")
        player_data['dribbling'] = self.validate_int_input("Dribleo: ")
        player_data['ball_control'] = self.validate_int_input("Control del balon: ")
        return player_data  # Retorna los datos del jugador

    def get_player_id(self):
        # Obtiene el ID de un jugador
        while True:
            try:
                player_id = int(input("Ingrese el ID del jugador: "))  # Solicita al usuario ingresar el ID del jugador
                return player_id  # Retorna el ID del jugador
            except ValueError:
                print("El ID debe ser un número entero. Inténtelo de nuevo.")  # Maneja la excepción en caso de que no se ingrese un número entero

    def show_player_info(self, player_info):
        # Muestra la información de un jugador
        print("Información del Jugador:")
        print(f"ID: {player_info.get('id', 'N/A')}")  # Imprime el ID del jugador
        print(f"Nombre: {player_info.get('name', 'N/A')}")  # Imprime el nombre del jugador
        print(f"Fecha de nacimiento: {player_info.get('date_of_birth', 'N/A')}")  # Imprime la fecha de nacimiento del jugador
        print(f"Origen: {player_info.get('origin', 'N/A')}")  # Imprime el origen del jugador
        print(f"Género: {player_info.get('gender', 'N/A')}")  # Imprime el género del jugador
        print(f"Altura: {player_info.get('height', 'N/A')} m")  # Imprime la altura del jugador
        print(f"Peso: {player_info.get('weight', 'N/A')} kg")  # Imprime el peso del jugador
        print(f"Posición en campo: {player_info.get('position', 'N/A')}")  # Imprime la posición en campo del jugador
        print(f"Club Militante: {player_info.get('club', 'N/A')}")  # Imprime el club del jugador
        print(f"Reconocimientos: {player_info.get('achievements', 'N/A')}")  # Imprime los reconocimientos del jugador
        print(f"Aceleración: {player_info.get('acceleration', 'N/A')}")
        print(f"Pases Cortos: {player_info.get('short_passes', 'N/A')}")
        print(f"Poder de Tiro: {player_info.get('power_of_shot', 'N/A')}")
        print(f"Pases Largos: {player_info.get('long_passes', 'N/A')}")
        print(f"Velocidad: {player_info.get('speed', 'N/A')}")
        print(f"Agilidad: {player_info.get('agility', 'N/A')}")
        print(f"Resistencia: {player_info.get('resistence', 'N/A')}")
        print(f"Poder de Salto: {player_info.get('jump', 'N/A')}")
        print(f"Dribleo: {player_info.get('dribbling', 'N/A')}")
        print(f"Control del Balón: {player_info.get('ball_control', 'N/A')}")

    def show_player_statistics(self, player_statistics):
        print(f"ID: {player_statistics.get('id', 'N/A')}")  # Imprime el ID del jugador
        print(f"Nombre: {player_statistics.get('name', 'N/A')}")  # Imprime el nombre del jugador
        print(f"Aceleración: {player_statistics.get('acceleration', 'N/A')}")
        print(f"Pases Cortos: {player_statistics.get('short_passes', 'N/A')}")
        print(f"Poder de Tiro: {player_statistics.get('power_of_shot', 'N/A')}")
        print(f"Pases Largos: {player_statistics.get('long_passes', 'N/A')}")
        print(f"Velocidad: {player_statistics.get('speed', 'N/A')}")
        print(f"Agilidad: {player_statistics.get('agility', 'N/A')}")
        print(f"Resistencia: {player_statistics.get('resistence', 'N/A')}")
        print(f"Poder de Salto: {player_statistics.get('jump', 'N/A')}")
        print(f"Dribleo: {player_statistics.get('dribbling', 'N/A')}")
        print(f"Control del Balón: {player_statistics.get('ball_control', 'N/A')}")


    def show_message(self, message):
        # Muestra un mensaje
        print(message)  # Imprime el mensaje

    def show_player_list(self, player_list):
        # Muestra una lista de jugadores
        print("\nLista de Jugadores:")
        for player in player_list:
            print(f"ID: {player['id']}, Nombre: {player['name']}, Club: {player['club']}")  # Imprime el ID, nombre y club de cada jugador

    def show_stats_menu(self):
        # Muestra el menú de estadísticas
        print("\nMenú de Estadísticas:")
        print("1. Ver estadísticas de un jugador por ID")
        print("2. Comparar estadísticas de jugadores por posición en el campo")
        return input("Seleccione una opción: ")  # Retorna la opción seleccionada por el usuario

    def show_player_stats(self, player_stats):
        # Muestra las estadísticas de un jugador
        print("\nEstadísticas del Jugador:")
        for stat, value in player_stats.items():
            print(f"{stat}: {value}")

    def show_players_stats_comparison(self, players_stats_comparison):
        # Muestra la comparación de estadísticas de los jugadores que juegan en la misma posición
        print("\nComparación de Estadísticas de Jugadores:")
        for player, stats in players_stats_comparison.items():
            print(f"\nJugador: {player}")
            for stat, value in stats.items():
                print(f"{stat}: {value}")

    def get_player_id_input(self):
        # Obtiene el ID del jugador desde la entrada del usuario
        return input("Ingrese el ID del jugador: ")

    def get_position_for_comparison(self):
        # Obtiene la posición en el campo para comparar las estadísticas de los jugadores
        return self.get_position_input()

    def show_players_by_origin(self, count):
        # Muestra la cantidad de jugadores por origen
        print(f"Cantidad de jugadores por origen: {count}")  # Imprime la cantidad de jugadores por origen

    def validate_text_input(self, message):
        # Valida la entrada de texto
        while True:
            value = input(message)  # Solicita al usuario ingresar un valor
            if value.replace(" ", "").isalpha():  # Verifica si el valor contiene solo letras y espacios
                return value  # Retorna el valor validado
            else:
                print("Entrada inválida. Por favor, ingrese solo caracteres alfabéticos y espacios.")  # Imprime un mensaje de error

    def validate_int_input(self, message):
        # Valida la entrada de números enteros
        while True:
            value = input(message)  # Solicita al usuario ingresar un valor
            if value.isdigit():  # Verifica si el valor es un número entero
                return int(value)  # Retorna el valor convertido a entero
            else:
                print("Entrada inválida. Por favor, ingrese solo números enteros.")  # Imprime un mensaje de error

    def validate_float_input(self, message):
        # Valida la entrada de números flotantes
        while True:
            value = input(message)  # Solicita al usuario ingresar un valor
            try:
                float_value = float(value)  # Intenta convertir el valor a flotante
                return float_value  # Retorna el valor flotante validado
            except ValueError:
                print("Entrada inválida. Por favor, ingrese un número válido.")  # Imprime un mensaje de error

    def validate_date_input(self, message):
        # Valida la entrada de fechas
        while True:
            value = input(message)  # Solicita al usuario ingresar una fecha
            try:
                datetime.datetime.strptime(value, "%Y-%m-%d")  # Intenta analizar la fecha en el formato especificado
                return value  # Retorna la fecha validada
            except ValueError:
                print("Formato de fecha inválido. Por favor, ingrese la fecha en el formato correcto (YYYY-MM-DD).")  # Imprime un mensaje de error

    def validate_gender_input(self, message):
        # Valida la entrada de género
        while True:
            value = input(message)  # Solicita al usuario ingresar el género
            if value.lower() in ['masculino', 'femenino']:  # Verifica si el género es masculino o femenino
                return value.capitalize()  # Retorna el género con la primera letra en mayúscula
            else:
                print("Género inválido. Por favor, ingrese 'Masculino' o 'Femenino'.")  # Imprime un mensaje de error

    def get_list_option(self):
        # Obtiene la opción de la lista
        print("\nOpciones de visualización:")
        print("1. Por origen")
        print("2. Por posición de campo")
        print("3. Por reconocimientos")
        return input("Seleccione una opción para filtrar la lista de jugadores: ")  # Retorna la opción seleccionada por el usuario

    def get_origin_input(self):
        # Obtiene el origen para filtrar la lista de jugadores
        return input("Ingrese el origen para filtrar la lista de jugadores: ")  # Retorna el origen ingresado por el usuario

    def get_position_input(self):
        # Obtiene la posición para filtrar la lista de jugadores
        return input("Ingrese la posición para filtrar la lista de jugadores: ")  # Retorna la posición ingresada por el usuario

    def get_recognition_input(self):
        # Obtiene el número de reconocimientos para filtrar la lista de jugadores
        return input("Ingrese el número de reconocimientos para filtrar la lista de jugadores: ")  # Retorna el número de reconocimientos ingresado por el usuario