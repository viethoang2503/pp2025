import curses
import math
import os
from domains.student import Student
from domains.course import Course

# Get the directory where this script is located
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

def get_input_str(stdscr, prompt):
    stdscr.addstr(prompt)
    stdscr.refresh()
    curses.echo()
    result = stdscr.getstr().decode('utf-8').strip()
    curses.noecho()
    return result

def get_input_int(stdscr, prompt):
    while True:
        try:
            val = get_input_str(stdscr, prompt)
            if not val:
                continue
            return int(val)
        except ValueError:
            stdscr.addstr("Invalid number! Please enter an integer.\n")

def is_valid_name(name):
    if not name:
        return False
    return all(char.isalpha() or char.isspace() for char in name)

def is_valid_id(id_str):
    if not id_str:
        return False
    return " " not in id_str

def input_student(stdscr):
    stdscr.addstr("\n--- Add New Student ---\n")
    while True:
        s_id = get_input_str(stdscr, "Enter Student ID (no spaces): ")
        if is_valid_id(s_id):
            break
        stdscr.addstr("Invalid ID! ID must not contain spaces.\n")

    while True:
        name = get_input_str(stdscr, "Enter Student Name (letters only): ")
        if is_valid_name(name):
            break
        stdscr.addstr("Invalid name! Name must contain only letters.\n")
        
    dob = get_input_str(stdscr, "Enter Date of Birth: ")
    
    students_file = os.path.join(SCRIPT_DIR, "students.txt")
    with open(students_file, "a", encoding="utf-8") as f:
        f.write(f"{s_id}|{name}|{dob}\n")
        
    return Student(s_id, name, dob)

def input_course(stdscr):
    stdscr.addstr("\n--- Add New Course ---\n")
    while True:
        c_id = get_input_str(stdscr, "Enter Course ID (no spaces): ")
        if is_valid_id(c_id):
            break
        stdscr.addstr("Invalid ID! ID must not contain spaces.\n")

    while True:
        name = get_input_str(stdscr, "Enter Course Name (letters only): ")
        if is_valid_name(name):
            break
        stdscr.addstr("Invalid name! Name must contain only letters.\n")
        
    credits = get_input_int(stdscr, "Enter Credits: ")
    
    courses_file = os.path.join(SCRIPT_DIR, "courses.txt")
    with open(courses_file, "a", encoding="utf-8") as f:
        f.write(f"{c_id}|{name}|{credits}\n")
        
    return Course(c_id, name, credits)

def input_mark(stdscr, student_id, student_name, course_id):
    while True:
        try:
            val = get_input_str(stdscr, f"Enter mark for {student_name}: ")
            raw_mark = float(val)
            final_mark = math.floor(raw_mark * 10) / 10
            
            marks_file = os.path.join(SCRIPT_DIR, "marks.txt")
            with open(marks_file, "a", encoding="utf-8") as f:
                f.write(f"{student_id}|{course_id}|{final_mark}\n")
                
            return final_mark
        except ValueError:
            stdscr.addstr("Invalid mark! Please enter a number.\n")