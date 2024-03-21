from model.student_model import StudentModel
from view.student_view import StudentView

class StudentController:
    def __init__(self):
        self.view = StudentView()
        self.model = StudentModel('students.json')
    def run(self):
        while True:
            choice = self.view.show_menu()
            if choice == '1':
                self.add_student()
            elif choice == '2':
                self.list_students()
            elif choice == '3':
                self.update_student()
            elif choice == '4':
                self.delete_student()
            elif choice == '5':
                break
            else:
                self.view.show_message("Opción inválida, intente de nuevo.")

    def add_student(self):
        student_data = self.view.get_student_data()
        self.model.add_student(student_data)
        self.view.show_message("Estudiante agregado exitosamente")

    def list_students(self):
        students = self.model.get_students()
        self.view.show_students(students)
    def update_student(self):
        student_id = input("Ingrese el ID del estudiante a actualizar: ")
        updated_student = self.view.get_student_data()
        self.model.update_student(student_id, updated_student)
        self.view.show_message("Estudiante actualizado exitosamente")

    def delete_student(self):
        student_id = input("Ingrese el ID del estudiante a eliminar: ")
        self.model.delete_student(student_id)
        self.view.show_message("Estudiante eliminado exitosamente")
