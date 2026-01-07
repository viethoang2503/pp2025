import curses
import numpy as np
import input
import output
# Ensure you have the domains package with student.py and course.py
from domains.student import Student
from domains.course import Course


class MarkManager:
    def __init__(self):
        self.__students = []
        self.__courses = []
        self.__marks = {} # Structure: {course_id: {student_id: mark}}

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
                # Use numpy for weighted average specific to requirement 3
                np_marks = np.array(marks_arr)
                np_credits = np.array(credits_arr)
                if np.sum(np_credits) > 0:
                    gpa = np.sum(np_marks * np_credits) / np.sum(np_credits)
                    student.set_gpa(gpa)
                else:
                    student.set_gpa(0.0)
            else:
                student.set_gpa(0.0)
        
        # Sort students descending by GPA
        self.__students.sort(key=lambda x: x.get_gpa(), reverse=True)

    def process_marks(self, stdscr):
        stdscr.clear()
        if not self.__courses:
            output.show_message(stdscr, "Error: No courses available!")
            return
        
        stdscr.addstr(0, 0, "List of courses:\n")
        line = 1
        for c in self.__courses:
            stdscr.addstr(line, 0, f"[{c.get_id()}] {c.get_name()}")
            line += 1
        
        stdscr.addstr(line + 1, 0, "") # Empty line
        c_id = input.get_input_str(stdscr, "Enter course ID to input mark: ")
        
        # Find course by ID
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
                # Use input_mark from input module, passing all required arguments
                mark = input.input_mark(stdscr, s.get_id(), s.get_name(), c_id)
                self.__marks[c_id][s.get_id()] = mark
                line += 1 # Move to next line
            
            output.show_message(stdscr, "Updated scores successfully!")
        else:
            output.show_message(stdscr, "Course not found!")

    def run(self, stdscr):
        # Initial curses setup
        curses.curs_set(0) # Hide cursor
        
        while True:
            choice = output.display_menu(stdscr)
            
            # Handle invalid choice
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
                self.process_marks(stdscr)
            elif choice == ord('4'):
                self.calculate_all_gpas()
                output.show_student_list(stdscr, self.__students)
            elif choice == ord('5'):
                break

if __name__ == "__main__":
    manager = MarkManager()
    curses.wrapper(manager.run)