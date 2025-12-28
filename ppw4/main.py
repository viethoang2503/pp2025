import curses
import numpy as np
import input
import output
from domains.student import Student
from domains.course import Course


class MarkManager:
    def __init__(self):
        self.__students = []
        self.__courses = []
        self.__marks = {} # Cấu trúc: {course_id: {student_id: mark}}

    def calculate_all_gpas(self):
        for student in self.__students:
            marks_arr = []
            credits_arr = []
            for course in self.__courses:
                c_id = course.get_id()
                s_id = student.get_id()
                if c_id in self.__marks and s_id in self.__marks[c_id]:
                    marks_arr.append(self.__marks[c_id][s_id])
                    credits_arr.append(course.get_credits())
            
            if marks_arr:
                # Sử dụng numpy tính trung bình có trọng số theo yêu cầu bài 3
                np_marks = np.array(marks_arr)
                np_credits = np.array(credits_arr)
                gpa = np.sum(np_marks * np_credits) / np.sum(np_credits)
                student.set_gpa(gpa)
        
        # Sắp xếp danh sách giảm dần theo GPA
        self.__students.sort(key=lambda x: x.get_gpa(), reverse=True)

    def process_marks(self, stdscr):
        if not self.__courses:
            output.show_message(stdscr, "Error: No courses available!")
            return
        
        stdscr.addstr("\nAvailable Courses:\n")
        for c in self.__courses:
            stdscr.addstr(f"[{c.get_id()}] {c.get_name()}\n")
        
        c_id = input.get_input_str(stdscr, "Enter Course ID to input marks: ")
        selected_course = next((c for c in self.__courses if c.get_id() == c_id), None)
        
        if selected_course:
            if c_id not in self.__marks:
                self.__marks[c_id] = {}
            for s in self.__students:
                mark = input.input_mark(stdscr, s.get_name())
                self.__marks[c_id][s.get_id()] = mark
        else:
            output.show_message(stdscr, "Course not found!")

    def run(self, stdscr):
        while True:
            choice = output.display_menu(stdscr)
            if choice == ord('1'):
                num = int(input.get_input_str(stdscr, "How many students? "))
                for _ in range(num):
                    self.__students.append(input.input_student(stdscr))
            elif choice == ord('2'):
                num = int(input.get_input_str(stdscr, "How many courses? "))
                for _ in range(num):
                    self.__courses.append(input.input_course(stdscr))
            elif choice == ord('3'):
                self.process_marks(stdscr)
            elif choice == ord('4'):
                self.calculate_all_gpas()
                output.show_student_list(stdscr, self.__students)
            elif choice == ord('5'):
                break
            
    # Tìm đến phương thức run trong lớp MarkManager và sửa lại như sau:
    def run(self, stdscr):
        while True:
            choice = output.display_menu(stdscr)
            if choice == ord('1'):
                # Sử dụng hàm nhập số nguyên an toàn
                num = input.get_input_int(stdscr, "How many students? ")
                for _ in range(num):
                    self.__students.append(input.input_student(stdscr))
            elif choice == ord('2'):
                # Sử dụng hàm nhập số nguyên an toàn
                num = input.get_input_int(stdscr, "How many courses? ")
                for _ in range(num):
                    self.__courses.append(input.input_course(stdscr))
            # ... (các phần còn lại giữ nguyên)
            
    # Trong class MarkManager
    def run(self, stdscr):
        # Thiết lập curses ban đầu
        curses.curs_set(0) # Ẩn con trỏ chuột
        
        while True:
            choice = output.display_menu(stdscr)
            
            # Xử lý trường hợp không nhận được phím bấm hợp lệ
            if choice == -1:
                continue
                
            if choice == ord('1'):
                stdscr.clear()
                num = input.get_input_int(stdscr, "How many students? ")
                for _ in range(num):
                    self.__students.append(input.input_student(stdscr))
            elif choice == ord('2'):
                stdscr.clear()
                num = input.get_input_int(stdscr, "How many courses? ")
                for _ in range(num):
                    self.__courses.append(input.input_course(stdscr))
            elif choice == ord('3'):
                stdscr.clear()
                self.process_marks(stdscr)
            elif choice == ord('4'):
                self.calculate_all_gpas()
                output.show_student_list(stdscr, self.__students)
            elif choice == ord('5'):
                break
    
    def process_marks(self, stdscr):
        stdscr.clear()
        if not self.__courses:
            output.show_message(stdscr, "Error, no course here")
            return
        
        stdscr.addstr(0, 0, "List of courses:\n")
        line = 1
        for c in self.__courses:
            stdscr.addstr(line, 0, f"[{c.get_id()}] {c.get_name()}")
            line += 1
        
        stdscr.addstr(line + 1, 0, "") # Dong trong
        c_id = input.get_input_str(stdscr, "Enter course ID to input mark: ")
        
        # Tim khoa hoc theo ID
        selected_course = None
        for c in self.__courses:
            if c.get_id() == c_id:
                selected_course = c
                break
        
        if selected_course:
            if c_id not in self.__marks:
                self.__marks[c_id] = {}
            
            for s in self.__students:
                stdscr.addstr(line + 3, 0, f"Entering score for : {s.get_name()}")
                # Su dung ham input_mark tu module input
                mark = input.input_mark(stdscr, s.get_name())
                self.__marks[c_id][s.get_id()] = mark
                line += 1 # Xuong dong cho sinh vien tiep theo
            
            output.show_message(stdscr, "Updated scored sucessful!")
        else:
            output.show_message(stdscr, "Can not find ID!")

    def run(self, stdscr):
        # An con tro de giao dien dep hon, khi can nhap lieu curses se tu bat lai
        curses.curs_set(1) 
        
        while True:
            choice_ch = output.display_menu(stdscr)
            
            # curses.getch() tra ve ma ASCII. ord('3') tuong ung voi phim so 3
            if choice_ch == ord('1'):
                stdscr.clear()
                num = input.get_input_int(stdscr, "Enter number of students: ")
                for _ in range(num):
                    self.__students.append(input.input_student(stdscr))
            
            elif choice_ch == ord('2'):
                stdscr.clear()
                num = input.get_input_int(stdscr, "Enter number of courses: ")
                for _ in range(num):
                    self.__courses.append(input.input_course(stdscr))
            
            elif choice_ch == ord('3'):
                self.process_marks(stdscr)
            
            elif choice_ch == ord('4'):
                self.calculate_all_gpas()
                output.show_student_list(stdscr, self.__students)
            
            elif choice_ch == ord('5'):
                break


if __name__ == "__main__":
    manager = MarkManager()
    curses.wrapper(manager.run)