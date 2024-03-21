import json

class StudentModel:
    def __init__(self,data_file):
        self._data_file = data_file
    def read_data(self):
        try:
            with open(self._data_file,'r') as File:
                return json.load(File)
        except FileNotFoundError:
            return[]
    def write_data(self,data):
        with open(self._data_file, 'w') as File:
            json.dump(data,File,indent=4)

    def add_student(self,student):
        students= self.read_data()
        students.append(student)
        self.write_data(students)

    def get_students(self):
        return self.read_data()
    def update_student(self,student_id,updated_student):
        students= self.read_data()
        for i, student in enumerate(students):
            if student['id'] == student_id:
                students[i] = updated_student
                break
        self.write_data(students)

    def delete_student(self,student_id):
        students= self.read_data()
        students= [student for student in students if student['id'] != student_id ]
        self.write_data(students)
