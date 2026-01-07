import os
import pickle
import gzip
import curses

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_FILE = os.path.join(SCRIPT_DIR, "students.dat")

def select_compression_method(stdscr):
    """Let user select compression method"""
    stdscr.clear()
    stdscr.addstr(0, 0, "=== SELECT COMPRESSION METHOD ===", curses.A_BOLD)
    stdscr.addstr(2, 0, "1. Pickle (Python binary format)")
    stdscr.addstr(3, 0, "2. Gzip (Compressed format)")
    stdscr.addstr(5, 0, "Select method (1 or 2): ")
    stdscr.refresh()
    
    while True:
        choice = stdscr.getch()
        if choice == ord('1'):
            return 'pickle'
        elif choice == ord('2'):
            return 'gzip'

def compress_data(stdscr, method='pickle'):
    """Compress all text files into students.dat"""
    try:
        students_file = os.path.join(SCRIPT_DIR, "students.txt")
        courses_file = os.path.join(SCRIPT_DIR, "courses.txt")
        marks_file = os.path.join(SCRIPT_DIR, "marks.txt")
        
        # Read all files
        data = {
            'students': [],
            'courses': [],
            'marks': []
        }
        
        if os.path.exists(students_file):
            with open(students_file, 'r', encoding='utf-8') as f:
                data['students'] = f.readlines()
        
        if os.path.exists(courses_file):
            with open(courses_file, 'r', encoding='utf-8') as f:
                data['courses'] = f.readlines()
        
        if os.path.exists(marks_file):
            with open(marks_file, 'r', encoding='utf-8') as f:
                data['marks'] = f.readlines()
        
        # Compress based on method
        if method == 'pickle':
            with open(DATA_FILE, 'wb') as f:
                pickle.dump(data, f)
        elif method == 'gzip':
            with gzip.open(DATA_FILE, 'wb') as f:
                pickle.dump(data, f)
        
        stdscr.clear()
        stdscr.addstr(0, 0, f"Successfully compressed data using {method.upper()}!", curses.A_BOLD)
        stdscr.addstr(1, 0, f"Saved to: students.dat")
        stdscr.addstr(3, 0, "Press any key to continue...")
        stdscr.refresh()
        stdscr.getch()
        return True
        
    except Exception as e:
        stdscr.clear()
        stdscr.addstr(0, 0, f"Error compressing data: {str(e)}")
        stdscr.addstr(2, 0, "Press any key to continue...")
        stdscr.refresh()
        stdscr.getch()
        return False

def decompress_data(stdscr):
    """Decompress students.dat and load data"""
    try:
        if not os.path.exists(DATA_FILE):
            return None
        
        # Try to decompress with different methods
        data = None
        
        # Try gzip first
        try:
            with gzip.open(DATA_FILE, 'rb') as f:
                data = pickle.load(f)
        except:
            # If gzip fails, try regular pickle
            with open(DATA_FILE, 'rb') as f:
                data = pickle.load(f)
        
        if data:
            students_file = os.path.join(SCRIPT_DIR, "students.txt")
            courses_file = os.path.join(SCRIPT_DIR, "courses.txt")
            marks_file = os.path.join(SCRIPT_DIR, "marks.txt")
            
            # Write decompressed data to files
            with open(students_file, 'w', encoding='utf-8') as f:
                f.writelines(data.get('students', []))
            
            with open(courses_file, 'w', encoding='utf-8') as f:
                f.writelines(data.get('courses', []))
            
            with open(marks_file, 'w', encoding='utf-8') as f:
                f.writelines(data.get('marks', []))
            
            stdscr.clear()
            stdscr.addstr(0, 0, "Successfully decompressed students.dat!", curses.A_BOLD)
            stdscr.addstr(1, 0, f"Loaded {len(data.get('students', []))} students")
            stdscr.addstr(2, 0, f"Loaded {len(data.get('courses', []))} courses")
            stdscr.addstr(3, 0, f"Loaded {len(data.get('marks', []))} marks")
            stdscr.addstr(5, 0, "Press any key to continue...")
            stdscr.refresh()
            stdscr.getch()
            
        return data
        
    except Exception as e:
        stdscr.clear()
        stdscr.addstr(0, 0, f"Error decompressing data: {str(e)}")
        stdscr.addstr(2, 0, "Press any key to continue...")
        stdscr.refresh()
        stdscr.getch()
        return None

def check_and_load_data(stdscr):
    """Check if students.dat exists and load it"""
    if os.path.exists(DATA_FILE):
        stdscr.clear()
        stdscr.addstr(0, 0, "Found students.dat file!", curses.A_BOLD)
        stdscr.addstr(1, 0, "Decompressing and loading data...")
        stdscr.refresh()
        return decompress_data(stdscr)
    return None
