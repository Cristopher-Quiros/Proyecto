class StudentView:

    def show_menu(self):
        print("1. Agregar estudiante")
        print("2. Listar estudiantes")
        print("3. Actualizar estudiante")
        print("4. Eliminar estudiante")
        print("5. Salir")
        return input("Selecione una opción: ")

    def get_student_data(self):
        return {
            "id": input("ID del estudiante: "),
            "name": input("Nombre del estudiante: "),
            "first_name": input("Primer apellido del estudiante: "),
            "second_last_name": input("Segundo apellido del estudiante: "),
            "age": input("Edad del estudiante: ")
        }

    def show_students(self,students):
        for student in students:
            print(f"ID: {student['id']}, Nombre:  {student['name']}, Primer apellido: {student['first_name']}, Segundo apellido: {student['second_last_name']}, Edad: {student['age']}")

    def show_message(self,message):
        print(message)