import datetime
import sys # noqa # Es una lista que contiene argumentos pasados al script Python
from PyQt5.QtWidgets import (QApplication, QWidget, QVBoxLayout, QPushButton, QMessageBox, QInputDialog, QAction,
                             QMenu, QDialog, QTableWidget, QTableWidgetItem, QAbstractItemView)
# Widget funcionalidades básicas como la gestión de eventos, el manejo de la geometría (tamaño y posición) y la gestión de la apariencia.
# VBoxLayout administrador de diseño que organiza los widgets en una disposición vertical, es decir, uno encima del otro. Se utiliza para organizar widgets dentro de contenedores, como ventanas o diálogos.
# TableWidget widget que proporciona una vista tabular en la que se pueden mostrar datos en forma de filas y columnas. Se utiliza para mostrar y editar datos tabulares en una interfaz de usuario.
# TableWidgetItem es un objeto que representa un elemento individual dentro de un QTableWidget. Se utiliza para almacenar y manipular los datos mostrados en las celdas de la tabla.
# AbstractItemView es la clase base para las vistas de los modelos de datos en PyQt5. Proporciona funcionalidades comunes para trabajar con datos, como la selección de elementos, la edición de datos,
# la ordenación y el filtrado. QTableWidget hereda de esta clase para proporcionar una vista tabular específica.


class PlayerView(QWidget):
    def __init__(self, data_file):
        super().__init__()
        self.data_file = data_file
        self.controller = None # Se inicializa en None, para mas adelante asignarselo y poder manejar errores potenciales
        self.setWindowTitle('Player Management System')
        self.layout = QVBoxLayout(self)

        # Botón para la gestión de jugadores (CRUD)
        self.crud_button = QPushButton('Gestión de Jugadores')
        self.crud_button.clicked.connect(self.show_crud_menu)
        self.layout.addWidget(self.crud_button)

        # Botón para mostrar el menú de opciones de jugador
        self.show_menu_button = QPushButton('Opciones de Jugador')
        self.show_menu_button.setMenu(self.create_menu())
        self.layout.addWidget(self.show_menu_button)

        self.stats_button = QPushButton('Estadísticas de Jugador')
        self.stats_button.clicked.connect(self.show_player_statistics)
        self.layout.addWidget(self.stats_button)

        # Botón para mostrar opciones avanzadas
        self.advanced_button = QPushButton('Consultas Avanzadas')
        self.advanced_button.clicked.connect(self.show_advanced_queries_menu)
        self.layout.addWidget(self.advanced_button)

        # Botón para salir de la aplicación
        self.exit_button = QPushButton('Salir')
        self.exit_button.clicked.connect(self.exit_application)
        self.layout.addWidget(self.exit_button)

        self.setLayout(self.layout) #Establece un diseño de como se organizara la GUI



    def set_controller(self, controller):
        self.controller = controller

    def exit_application(self):
        QApplication.quit()
    def create_menu(self):
        menu = QMenu()
        menu.addAction("Mostrar Lista de Jugadores", lambda: self.show_player_list(self.controller.model.get_players()))
        menu.addAction("Filtrar por Origen", self.filter_players_by_origin)
        menu.addAction("Filtrar por Posición", self.filter_players_by_position)
        menu.addAction("Filtrar por Reconocimientos", self.filter_players_by_recognition)
        return menu

    def show_crud_menu(self):
        crud_menu = QMenu()
        crud_menu.addAction("Añadir Jugador", self.add_player)
        crud_menu.addAction("Consultar Jugador", self.read_player)
        crud_menu.addAction("Actualizar Jugador", self.update_player)
        crud_menu.addAction("Borrar Jugador", self.delete_player)
        crud_menu.exec_(self.crud_button.mapToGlobal(self.crud_button.rect().bottomLeft()))
        # self.crud_button.rect() devuelve el rectángulo del botón crud_button en sus coordenadas locales.
        # bottomLeft() se aplica a ese rectángulo para obtener las coordenadas del punto inferior izquierdo del rectángulo.
        # Estas coordenadas locales se pasan como argumento a mapToGlobal(), que convierte estas coordenadas locales en coordenadas globales en la pantalla.
        # Las coordenadas globales resultantes se utilizan para determinar la posición en la que se mostrará el menú contextual asociado al botón.

    def show_player_statistics(self):
        menu = QMenu()
        menu.addAction("Estadísticas de Jugador", self.show_player_stats_menu)
        menu.addAction("Comparar Jugadores por Posición", self.compare_players_by_position)
        menu.exec_(self.stats_button.mapToGlobal(self.stats_button.rect().bottomLeft()))

    def show_players_list_for_selection(self, players_with_ids):
        player_names = [f"{player['name']} (ID: {player['id']})" for player in players_with_ids]
        selected_player, ok = QInputDialog.getItem(self, 'Selecciona un jugador', 'Jugadores:', player_names, 0, False)

        if ok and selected_player:
            # Extraer el ID del jugador seleccionado
            selected_id = int(selected_player.split('(ID: ')[1].split(')')[0])
            return selected_id
        else:
            return None

    # Metodo CRUD
    def add_player(self):
        player_data = self.get_player_data()  # Obtener los datos del jugador desde la vista
        if player_data is not None:  # Verificar si se canceló la operación
            players = self.controller.model.get_players()  # Obtener la lista de jugadores actuales
            if players:
                # Encontrar el último ID y asignar el nuevo ID al siguiente número después del último
                last_id = max(player['id'] for player in players)
                player_data['id'] = last_id + 1
            else:
                # Si no hay jugadores, asignar ID 1 al nuevo jugador
                player_data['id'] = 1

            # Pasar los datos del jugador con el ID asignado automáticamente al controlador para agregarlo
            self.controller.model.add_player(player_data)
            self.show_message("Jugador Ingresado Exitosamente")
        else:
            self.show_message("Operación cancelada.")

    def read_player(self):
        players = self.controller.model.get_players()
        if not players:
            self.show_message("No hay jugadores registrados.")
            return

        # Crear la tabla de jugadores
        player_table_dialog = QDialog(self)
        player_table_dialog.setWindowTitle('Seleccionar Jugador')
        player_table_layout = QVBoxLayout()
        player_table = QTableWidget()
        player_table.setColumnCount(2)
        player_table.setHorizontalHeaderLabels(["ID", "Nombre"])

        # Llenar la tabla con los jugadores
        for row, player in enumerate(players):
            player_table.insertRow(row)
            player_table.setItem(row, 0, QTableWidgetItem(str(player['id'])))
            player_table.setItem(row, 1, QTableWidgetItem(player['name']))

        # Configurar la tabla como solo visual y permitir selección de filas
        player_table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        player_table.setSelectionBehavior(QAbstractItemView.SelectRows)

        player_table_layout.addWidget(player_table)
        select_button = QPushButton('Seleccionar')
        select_button.clicked.connect(lambda: self.select_player(player_table))
        player_table_layout.addWidget(select_button)

        player_table_dialog.setLayout(player_table_layout)
        player_table_dialog.exec_()

    # player_table_dialog = QDialog(self): Se crea un nuevo diálogo (QDialog) y se establece como padre el widget self (probablemente la ventana principal de la aplicación). Esto crea una nueva ventana modal que contendrá la tabla de jugadores y un botón de selección.
    # player_table_dialog.setWindowTitle('Seleccionar Jugador'): Se establece el título de la ventana modal como "Seleccionar Jugador".
    # player_table_layout = QVBoxLayout(): Se crea un nuevo diseño vertical (QVBoxLayout) que se utilizará para organizar los widgets dentro del diálogo.
    # player_table = QTableWidget(): Se crea un nuevo widget QTableWidget que se utilizará para mostrar la información de los jugadores en forma de tabla.
    # player_table.setColumnCount(2): Se establece el número de columnas de la tabla en 2.
    # player_table.setHorizontalHeaderLabels(["ID", "Nombre"]): Se establecen las etiquetas de encabezado horizontal de las columnas de la tabla como "ID" y "Nombre".
    # Se recorre la lista de jugadores (players) y se llena la tabla con los datos de cada jugador. Para cada jugador, se inserta una nueva fila en la tabla (insertRow()) y se establecen los elementos de la fila con el ID y el nombre del jugador utilizando setItem().
    # player_table.setEditTriggers(QAbstractItemView.NoEditTriggers): Se configura la tabla para que no se pueda editar directamente ningún elemento de la tabla. Esto significa que los usuarios no pueden modificar los datos directamente en la tabla.
    # player_table.setSelectionBehavior(QAbstractItemView.SelectRows): Se configura el comportamiento de selección de la tabla para que los usuarios puedan seleccionar filas completas en lugar de celdas individuales.
    # player_table_layout.addWidget(player_table): Se agrega la tabla de jugadores al diseño vertical del diálogo.
    # select_button = QPushButton('Seleccionar'): Se crea un nuevo botón de "Seleccionar".
    # select_button.clicked.connect(lambda: self.select_player(player_table)): Se conecta la señal clicked del botón a una función select_player() cuando se hace clic en el botón. Se utiliza un lambda para pasar la tabla de jugadores como argumento a la función select_player().
    # player_table_layout.addWidget(select_button): Se agrega el botón "Seleccionar" al diseño vertical del diálogo.
    # player_table_dialog.setLayout(player_table_layout): Se establece el diseño vertical como el diseño del diálogo.
    # player_table_dialog.exec_(): Se ejecuta el diálogo modal. Esto muestra la ventana modal con la tabla de jugadores y el botón "Seleccionar". El diálogo bloquea la interacción con el resto de la aplicación hasta que se cierre.

    def select_player(self, player_table):
        selected_items = player_table.selectedItems()
        if len(selected_items) != 2:
            self.show_message("Por favor selecciona un jugador.")
            return

        player_id = int(selected_items[0].text())
        player_name = selected_items[1].text()
        player = self.controller.model.get_player(player_id)
        if player:
            self.show_player_info(player)
            self.controller.show_menu()
        else:
            self.show_message("No hay ningún jugador con ese ID.")

    # Cuando seleccionas una fila en la tabla, en realidad estás seleccionando las celdas de esa fila. Si tu tabla tiene dos columnas (ID y Nombre), entonces cada fila seleccionada tendrá dos elementos
    # en selected_items: uno para el ID y otro para el Nombre.

    # Entonces, selected_items[0] es el primer elemento seleccionado, que generalmente corresponde al ID del jugador en la tabla. Y selected_items[1] es el segundo elemento seleccionado,
    # que generalmente corresponde al Nombre del jugador en la tabla.

    # Por lo tanto, selected_items[0] y selected_items[1] no son los índices de los jugadores, sino los elementos seleccionados en la tabla que representan el ID y el Nombre del jugador, respectivamente.

    def show_player_info(self, player):
        player_info = f"ID: {player['id']}\nNombre: {player['name']}\nClub: {player['club']}\n\n{self.format_stats(player)}"
        self.show_message(player_info)

    def update_player(self):
        players = self.controller.model.get_players()
        if not players:
            self.show_message("No hay jugadores registrados.")
            return

        self.table = QTableWidget()
        self.table.setEditTriggers(QAbstractItemView.DoubleClicked)  # Permitir edición al doble clic

        # Mostrar la tabla de jugadores
        player_table_dialog = QDialog(self)
        player_table_dialog.setWindowTitle('Actualizar Jugadores')
        player_table_layout = QVBoxLayout()
        player_table = QTableWidget()
        player_table.setColumnCount(20)  # Ajustar según la cantidad de atributos del jugador
        player_table.setHorizontalHeaderLabels(["ID", "Nombre", "Fecha de nacimiento", "Origen", "Género", "Altura",
                                                "Peso", "Posición", "Club", "Logros", "Aceleración", "Pases Cortos",
                                                "Potencia de Tiro", "Pases Largos", "Velocidad", "Agilidad",
                                                "Resistencia",
                                                "Salto", "Dribbling", "Control de Balón"])

        # Llenar la tabla con los jugadores
        for row, player in enumerate(players):
            player_table.insertRow(row)
            player_table.setItem(row, 0, QTableWidgetItem(str(player['id'])))
            player_table.setItem(row, 1, QTableWidgetItem(player['name']))
            player_table.setItem(row, 2, QTableWidgetItem(player['date_of_birth']))
            player_table.setItem(row, 3, QTableWidgetItem(player['origin']))
            player_table.setItem(row, 4, QTableWidgetItem(player['gender']))
            player_table.setItem(row, 5, QTableWidgetItem(str(player['height'])))
            player_table.setItem(row, 6, QTableWidgetItem(str(player['weight'])))
            player_table.setItem(row, 7, QTableWidgetItem(player['position']))
            player_table.setItem(row, 8, QTableWidgetItem(player['club']))
            player_table.setItem(row, 9, QTableWidgetItem(player['achievements']))
            player_table.setItem(row, 10, QTableWidgetItem(str(player['acceleration'])))
            player_table.setItem(row, 11, QTableWidgetItem(str(player['short_passes'])))
            player_table.setItem(row, 12, QTableWidgetItem(str(player['power_of_shot'])))
            player_table.setItem(row, 13, QTableWidgetItem(str(player['long_passes'])))
            player_table.setItem(row, 14, QTableWidgetItem(str(player['speed'])))
            player_table.setItem(row, 15, QTableWidgetItem(str(player['agility'])))
            player_table.setItem(row, 16, QTableWidgetItem(str(player['resistence'])))
            player_table.setItem(row, 17, QTableWidgetItem(str(player['jump'])))
            player_table.setItem(row, 18, QTableWidgetItem(str(player['dribbling'])))
            player_table.setItem(row, 19, QTableWidgetItem(str(player['ball_control'])))

        player_table_layout.addWidget(player_table)
        update_button = QPushButton('Actualizar')
        update_button.clicked.connect(lambda: self.apply_changes_to_players(player_table))
        player_table_layout.addWidget(update_button)

        player_table_dialog.setLayout(player_table_layout)
        player_table_dialog.exec_()

    def apply_changes_to_players(self, player_table):
        updated_players = []
        column_names = [player_table.horizontalHeaderItem(col).text() for col in range(player_table.columnCount())]

        for row in range(player_table.rowCount()):
            player_data = {}
            for col, col_name in enumerate(column_names):
                item = player_table.item(row, col)
                if item is not None:
                    player_data[col_name] = item.text()
            updated_players.append(player_data)

        success = self.controller.update_players(updated_players)
        if success:
            self.show_message("Cambios aplicados exitosamente.")
        else:
            self.show_message("Error al aplicar los cambios.")

    # Se inicializa una lista vacía llamada updated_players que contendrá los datos actualizados de los jugadores después de aplicar los cambios.
    # column_names es una lista que contiene los nombres de las columnas de la tabla de jugadores. Se obtienen recorriendo todas las columnas de la tabla y obteniendo el texto del encabezado de cada columna
    # utilizando player_table.horizontalHeaderItem(col).text().

    # Se recorre cada fila de la tabla de jugadores utilizando un bucle for row in range(player_table.rowCount()). Para cada fila, se crea un diccionario llamado player_data que representará los datos de un jugador.
    # Dentro del bucle anidado for col, col_name in enumerate(column_names), se recorren todas las columnas de la fila actual y se obtiene el texto de cada celda utilizando
    # player_table.item(row, col).text(). Este texto se asigna al diccionario player_data con el nombre de la columna correspondiente como clave.

    # Una vez que se han obtenido los datos de todos los jugadores en la tabla y se han almacenado en updated_players, se intenta actualizar los jugadores en el modelo utilizando
    # self.controller.update_players(updated_players). Esto puede implicar guardar los cambios en una base de datos u otro almacenamiento de datos.
    # Dependiendo del éxito o fracaso de la operación de actualización (success), se muestra un mensaje al usuario utilizando self.show_message().
    def delete_player(self):
        players = self.controller.model.get_players()
        if not players:
            self.show_message("No hay jugadores registrados.")
            return

        # Crear la tabla de jugadores para seleccionar uno para borrar
        player_table_dialog = QDialog(self)
        player_table_dialog.setWindowTitle('Seleccionar Jugador para Borrar')
        player_table_layout = QVBoxLayout()
        player_table = QTableWidget()
        player_table.setColumnCount(2)
        player_table.setHorizontalHeaderLabels(["ID", "Nombre"])

        # Llenar la tabla con los jugadores
        for row, player in enumerate(players):
            player_table.insertRow(row)
            player_table.setItem(row, 0, QTableWidgetItem(str(player['id'])))
            player_table.setItem(row, 1, QTableWidgetItem(player['name']))

        # Configurar la tabla como solo visual y permitir selección de filas
        player_table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        player_table.setSelectionBehavior(QAbstractItemView.SelectRows)

        player_table_layout.addWidget(player_table)
        delete_button = QPushButton('Borrar')
        delete_button.clicked.connect(lambda: self.delete_selected_player(player_table))
        player_table_layout.addWidget(delete_button)

        player_table_dialog.setLayout(player_table_layout)
        player_table_dialog.exec_()
    def delete_selected_player(self, player_table):
        selected_items = player_table.selectedItems()
        if len(selected_items) != 2:
            self.show_message("Por favor selecciona un jugador.")
            return

        player_id = int(selected_items[0].text())
        player_name = selected_items[1].text()
        confirm_message = f"¿Estás seguro de que quieres borrar al jugador {player_name}? Esta acción no se puede deshacer."
        reply = QMessageBox.question(self, 'Confirmar Borrado', confirm_message, QMessageBox.Yes | QMessageBox.No,
                                     QMessageBox.No)
        if reply == QMessageBox.Yes:
            success = self.controller.model.delete_player(player_id)
            if success:
                self.show_message("Jugador borrado exitosamente.")
            else:
                self.show_message("Error al borrar el jugador.")
        else:
            self.show_message("Borrado cancelado.")

    # Opcion de mostrar jugadores y sus respectivos filtros
    def get_origin_input(self):  # Método para obtener la entrada de origen del jugador
        origin, ok = QInputDialog.getText(self, 'Origin Input',
                                          'Enter the origin of the player:')  # Abre un cuadro de diálogo para que el usuario ingrese el origen del jugador y devuelve el texto ingresado y un booleano que indica si se presionó "Aceptar"
        if ok:  # Verifica si se presionó "Aceptar" en el cuadro de diálogo
            # Comprueba si el valor contiene solo letras, espacios y comas, y está en formato mayúsculas o minúsculas
            if all(char.isalpha() or char.isspace() or char == ',' for char in
                   origin) and origin.strip():  # Verifica si cada carácter es una letra, un espacio o una coma, y si el texto no está vacío después de quitar los espacios
                return origin.strip().capitalize()  # Devuelve el origen ingresado con el primer carácter de cada palabra en mayúscula
            else:
                self.show_message(
                    "Invalid input. Please enter only alphabetical characters, spaces, and commas.")  # Muestra un mensaje de error si la entrada no es válida
        else:
            pass  # Ig
    def get_position_input(self):
        position, ok = QInputDialog.getText(self, 'Position Input', 'Enter the position of the player:')
        if ok:
            return position
        else:
            pass  # Ignorar la cancelación del diálogo de entrada y continuar ejecutando el programa
    def get_recognition_input(self):
        recognition, ok = QInputDialog.getInt(self, 'Recognition Input', 'Enter the recognition of the player:')
        if ok: # Si le da aceptar devuelve la información
            return recognition
        else:
            QMessageBox.information(self, "Operación cancelada", "La operación ha sido cancelada.")
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
            filtered_players = self.controller.model.filter_players_by_origin(origin) # Analiza si esta vacio o no la información
            if filtered_players: # Si no esta vacio devuelve la información
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
    def show_player_stats_menu(self):
        players = self.controller.model.get_players()
        if not players:
            self.show_message("No hay jugadores registrados.")
            return

        player_table_dialog = QDialog(self)
        player_table_dialog.setWindowTitle('Seleccionar Jugador')
        player_table_layout = QVBoxLayout()
        player_table = QTableWidget()
        player_table.setColumnCount(2)
        player_table.setHorizontalHeaderLabels(["ID", "Nombre"])

        for row, player in enumerate(players):
            player_table.insertRow(row)
            player_table.setItem(row, 0, QTableWidgetItem(str(player['id'])))
            player_table.setItem(row, 1, QTableWidgetItem(player['name']))

        player_table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        player_table.setSelectionBehavior(QAbstractItemView.SelectRows)

        player_table_layout.addWidget(player_table)
        select_button = QPushButton('Seleccionar')
        select_button.clicked.connect(lambda: self.show_player_stats(player_table))
        player_table_layout.addWidget(select_button)

        player_table_dialog.setLayout(player_table_layout)
        player_table_dialog.exec_()
    def compare_players_by_position(self):
        position = self.get_position_input()
        if position:
            players = self.controller.model.filter_players_by_position(position)
            if players:
                player_info = "\n\n".join(
                    [f"Name: {player['name']}\n{self.format_stats(player)}" for player in players])
                self.show_message(player_info)
            else:
                self.show_message("No hay jugadores en esa posición.")
        else:
            self.show_message("Ingresa una posición válida.")

    def show_player_stats(self, player_table):
        selected_items = player_table.selectedItems()
        if len(selected_items) != 2:
            self.show_message("Por favor selecciona un jugador.")
            return

        player_id = int(selected_items[0].text())
        player_name = selected_items[1].text()
        player = self.controller.model.get_player(player_id)
        if player:
            player_stats = f"Estadísticas para el jugador {player_name} (ID: {player_id}):\n"
            player_stats += self.format_stats(player)
            self.show_message(player_stats)
        else:
            self.show_message("No hay ningún jugador con ese ID.")

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
        # Esto proporciona una ubicación visualmente coherente para el menú en relación con el botón que lo activa.
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
        height, ok_height = QInputDialog.getDouble(self, 'Height Input', 'Enter player\'s height:', decimals=2)
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
        QMessageBox.information(self, "Information", message) # Crea una ventana de texto con la información
    # Informacion para agregar un jugador en el CRUD
    def get_player_data(self):
        player_data = {}
        fields = [
            ("Name of the player", "name"),
            ("Date of birth (YYYY-MM-DD)", "date_of_birth"),
            ("Origin of the player", "origin"),
            ("Gender (Male/Female)", "gender"),  # Cambio aquí
            ("Height of the player (in meters)", "height"),
            ("Weight of the player (in kg)", "weight"),
            ("Position in field of the player", "position"),
            ("Club of the player", "club"),
            ("Achievements of the player", "achievements"),
            ("Acceleration of the player", "acceleration"),
            ("Short Passes", "short_passes"),
            ("Power of Shot", "power_of_shot"),
            ("Long Passes", "long_passes"),
            ("Speed", "speed"),
            ("Agility", "agility"),
            ("Resistence", "resistence"),
            ("Jump", "jump"),
            ("Dribbling", "dribbling"),
            ("Ball Control", "ball_control")
        ]

        for prompt, field in fields:
            value = None
            if field == "gender":  # Cambio aquí
                value = self.validate_gender_input(prompt)  # Cambio aquí
            else:
                value = self.get_input(prompt, field)
            if value is None:  # Si la entrada es None, significa que se canceló
                return None
            else:
                player_data[field] = value

        return player_data

    # Se inicializa un diccionario vacío llamado player_data que contendrá los datos del jugador.

    # fields es una lista de tuplas donde cada tupla contiene una pregunta (prompt) que se le hace al usuario y el nombre del campo (field) asociado con ese dato del jugador en el diccionario.

    # Se recorre la lista fields utilizando un bucle for, donde en cada iteración se obtiene la pregunta y el nombre del campo asociado.

    # Se verifica si el nombre del campo es "gender". Si es así, se llama a la función validate_gender_input(prompt) para obtener la entrada del usuario para el género. Esto sugiere que validate_gender_input
    # es una función que se encarga de validar la entrada de género del usuario.

    # Si el nombre del campo no es "gender", se llama a la función get_input(prompt, field) para obtener la entrada del usuario para ese campo específico.

    # Si el valor obtenido no es None, lo que indicaría que el usuario canceló la entrada, se agrega al diccionario player_data utilizando el nombre del campo como clave y el valor como valor.

    # Una vez que se han obtenido todos los datos del jugador, se devuelve el diccionario player_data que contiene todos los datos ingresados por el usuario.

    #Una tupla en Python es una colección ordenada e inmutable de elementos. Esto significa que una vez que se crea una tupla, sus elementos no pueden ser modificados, añadidos ni eliminados.
    #Las tuplas se definen utilizando paréntesis () y pueden contener cualquier tipo de elemento, incluyendo números, cadenas, listas u otras tuplas

    def get_input(self, prompt, field):
        if field == "id" or field == "achievements" or field == "acceleration" or field == "short_passes" or \
                field == "power_of_shot" or field == "long_passes" or field == "speed" or field == "agility" or \
                field == "resistence" or field == "jump" or field == "dribbling" or field == "ball_control":
            return self.validate_int_input(prompt)
        elif field == "date_of_birth":
            return self.validate_date_input(prompt)
        elif field == "height":
            return self.validate_height_input(prompt)
        elif field == "weight":
            return  self.validate_weight_input(prompt)
        else:
            return self.validate_text_input(prompt)

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
                if all(char.isalpha() or char.isspace() or char == ',' for char in value) and value.strip(): # El value strip lo que hace es quitar espacios en blanco
                    return value.strip().capitalize()  # Convert the first letter of each word to uppercase
                else:
                    self.show_message("Invalid input. Please enter only alphabetical characters, spaces, and commas.")
            else:
                return None

    def validate_int_input(self, message):
        while True:
            value, ok = QInputDialog.getInt(self, 'Integer Input', message)
            if ok:
                if 1 <= value <= 100:  # Check if the value is between 1 and 100 (inclusive)
                    return value
                else:
                    self.show_message("Invalid input. Please enter a number between 0 and 100.")
            else:
                return None

    def validate_height_input(self, message):
        while True:
            value, ok = QInputDialog.getText(self, 'Height Input', message)
            if ok:
                try:
                    # Check if the input includes the unit (meters)
                    if "m" in value.lower():
                        float_value = float(value.lower().replace("m", "").strip())
                        if float_value >= 0:  # Check if the value is non-negative
                            return float_value
                        else:
                            self.show_message("Invalid input. Please enter a non-negative number.")
                    else:
                        self.show_message("Invalid input format. Please include the unit (meters).")
                except ValueError:
                    self.show_message(
                        "Invalid input. Please enter a valid floating-point number with the unit (meters).")
            else:
                return None

    def validate_weight_input(self, message):
        while True:
            value, ok = QInputDialog.getText(self, 'Weight Input', message)
            if ok:
                try:
                    # Check if the input includes the unit (kg)
                    if "kg" in value.lower():
                        float_value = float(value.lower().replace("kg", "").strip())
                        if float_value >= 0:  # Check if the value is non-negative
                            return float_value
                        else:
                            self.show_message("Invalid input. Please enter a non-negative number.")
                    else:
                        self.show_message("Invalid input format. Please include the unit (kg).")
                except ValueError:
                    self.show_message(
                        "Invalid input. Please enter a valid floating-point number with the unit (kg).")
            else:
                return None

    def validate_gender_input(self, message):
        while True:
            items = ['Male', 'Female']
            item, ok = QInputDialog.getItem(self, 'Gender Input', message, items, 0, False)
            if ok:
                return item
            else:
                return None
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

