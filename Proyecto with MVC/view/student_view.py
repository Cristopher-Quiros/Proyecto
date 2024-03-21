class StudentView:

    def show_menu(self):
        print("1. Agregar jugador")
        print("2. Consultar jugador")
        print("3. Actualizar jugadores")
        print("4. Eliminar jugadores")
        print("5. Salir")
        return input("Selecione una opción: ")

    def get_student_data(self):
        return {
            "name": input("Nombre del jugador: "),
            "age": input("Cuando nacio el jugador?: "),
            "origin": input("De donde es el jugador?: "),
            "gender": input("Es hombre o mujer?: "),
            "height": input("Cuanto mide el jugador?: "),
            "weight": input("Cuanto pesa el jugador?: ")

        }

    def show_students(self,students):
        for student in students:
            print(f"ID: {student['id']}, Nombre:  {student['name']}, Primer apellido: {student['first_name']}, Segundo apellido: {student['second_last_name']}, Edad: {student['age']}")

    def show_message(self,message):
        print(message)