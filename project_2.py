class Student:
    
    def __init__(self, student_id=None, name=None, dob=None):
        self.__id = student_id
        self.__name = name
        self.__dob = dob
    
    def get_id(self):
        return self.__id
    
    def get_name(self):
        return self.__name
    
    def get_dob(self):
        return self.__dob
    
    def set_id(self, student_id):
        self.__id = student_id
    
    def set_name(self, name):
        self.__name = name
    
    def set_dob(self, dob):
        self.__dob = dob
    
    def input(self):
        print("--- Input Student Information ---")
        self.__id = input("Enter Student ID: ")
        self.__name = input("Enter Student Name: ")
        self.__dob = input("Enter Date of Birth (DoB): ")
    
    def __str__(self):
        return f"ID: {self.__id}, Name: {self.__name}, DoB: {self.__dob}"


class Course:
    
    def __init__(self, course_id=None, name=None):
        self.__id = course_id
        self.__name = name
    
    def get_id(self):
        return self.__id
    
    def get_name(self):
        return self.__name
    
    def set_id(self, course_id):
        self.__id = course_id
    
    def set_name(self, name):
        self.__name = name
    
    def input(self):
        print("--- Input Course Information ---")
        self.__id = input("Enter Course ID: ")
        self.__name = input("Enter Course Name: ")
    
    def __str__(self):
        return f"ID: {self.__id}, Name: {self.__name}"


class MarkManager:
    
    def __init__(self):
        self.__students = []
        self.__courses = []
        self.__marks = {}
    
    def input_number_of_students(self):
        count = int(input("Enter number of students in class: "))
        return count
    
    def input_student_information(self):
        student = Student()
        student.input()
        self.__students.append(student)
    
    def input_number_of_courses(self):
        count = int(input("Enter number of courses: "))
        return count
    
    def input_course_information(self):
        course = Course()
        course.input()
        self.__courses.append(course)
    
    def input_marks(self):
        print("--- Input Marks ---")
        self.list_courses()
        
        course_id = input("Select Course ID to input marks: ")
        
        if not self.__find_course(course_id):
            print("Course not found!")
            return
        
        if course_id not in self.__marks:
            self.__marks[course_id] = {}
        
        for student in self.__students:
            mark = float(input(f"Enter mark for student {student.get_name()} (ID: {student.get_id()}): "))
            self.__marks[course_id][student.get_id()] = mark
    
    def list_students(self):
        print("\n-------------------------")
        print("LIST OF STUDENTS:")
        for student in self.__students:
            print(student)
        print("-------------------------\n")
    
    def list_courses(self):
        print("\n-------------------------")
        print("LIST OF COURSES:")
        for course in self.__courses:
            print(course)
        print("-------------------------\n")
    
    def show_student_marks(self):
        print("--- Show Marks ---")
        self.list_courses()
        course_id = input("Select Course ID to view marks: ")
        
        if course_id in self.__marks:
            print(f"\nMarks for Course {course_id}:")
            for student in self.__students:
                mark = self.__marks[course_id].get(student.get_id(), "N/A")
                print(f"Student: {student.get_name()}, Mark: {mark}")
        else:
            print("No marks data for this course yet.")
    
    def __find_course(self, course_id):
        for course in self.__courses:
            if course.get_id() == course_id:
                return course
        return None
    
    def run(self):
        num_students = self.input_number_of_students()
        for _ in range(num_students):
            self.input_student_information()
        
        num_courses = self.input_number_of_courses()
        for _ in range(num_courses):
            self.input_course_information()
        
        while True:
            print("\n--- MENU ---")
            print("1. List Students")
            print("2. List Courses")
            print("3. Input Marks")
            print("4. Show Marks")
            print("5. Exit")
            choice = input("Your choice: ")
            
            if choice == '1':
                self.list_students()
            elif choice == '2':
                self.list_courses()
            elif choice == '3':
                self.input_marks()
            elif choice == '4':
                self.show_student_marks()
            elif choice == '5':
                print("Exiting program...")
                break
            else:
                print("Invalid choice, please try again.")


if __name__ == "__main__":
    manager = MarkManager()
    manager.run()
