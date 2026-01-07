import os
import pickle
import gzip
import curses
import threading
import time

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_FILE = os.path.join(SCRIPT_DIR, "students.dat")

# Global variables for thread management
compression_thread = None
compression_status = {"running": False, "success": False, "error": None, "progress": ""}


def compress_data_background():
    """Background thread function to compress data using pickle + gzip"""
    global compression_status
    
    try:
        compression_status["running"] = True
        compression_status["progress"] = "Reading files..."
        
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
        
        compression_status["progress"] = "Reading courses..."
        if os.path.exists(courses_file):
            with open(courses_file, 'r', encoding='utf-8') as f:
                data['courses'] = f.readlines()
        
        compression_status["progress"] = "Reading marks..."
        if os.path.exists(marks_file):
            with open(marks_file, 'r', encoding='utf-8') as f:
                data['marks'] = f.readlines()
        
        # Compress using pickle with gzip
        compression_status["progress"] = "Compressing with PICKLE + GZIP..."
        with gzip.open(DATA_FILE, 'wb') as f:
            pickle.dump(data, f)
        
        compression_status["progress"] = "Compression complete!"
        compression_status["success"] = True
        compression_status["error"] = None
        
    except Exception as e:
        compression_status["success"] = False
        compression_status["error"] = str(e)
        compression_status["progress"] = f"Error: {str(e)}"
    
    finally:
        compression_status["running"] = False


def compress_data_async(stdscr):
    """Start compression in background thread and show progress"""
    global compression_thread, compression_status
    
    # Reset status
    compression_status = {"running": False, "success": False, "error": None, "progress": ""}
    
    # Start background thread
    compression_thread = threading.Thread(target=compress_data_background, daemon=True)
    compression_thread.start()
    
    # Show progress while thread is running
    stdscr.clear()
    stdscr.nodelay(True)  # Non-blocking input
    
    try:
        while compression_status["running"]:
            stdscr.clear()
            stdscr.addstr(0, 0, "=== BACKGROUND COMPRESSION ===", curses.A_BOLD)
            stdscr.addstr(2, 0, f"Status: {compression_status['progress']}")
            stdscr.addstr(4, 0, "Compressing in background thread...")
            stdscr.addstr(5, 0, "Please wait..." + "." * (int(time.time() * 2) % 4))
            stdscr.addstr(7, 0, "(Press 'q' to return to menu, compression continues)")
            stdscr.refresh()
            
            # Check for user input
            ch = stdscr.getch()
            if ch == ord('q') or ch == ord('Q'):
                stdscr.clear()
                stdscr.addstr(0, 0, "Compression running in background...", curses.A_BOLD)
                stdscr.addstr(1, 0, "You can continue using the program.")
                stdscr.addstr(3, 0, "Press any key to continue...")
                stdscr.refresh()
                stdscr.nodelay(False)
                stdscr.getch()
                return True
            
            time.sleep(0.1)
        
        # Show final result
        stdscr.clear()
        if compression_status["success"]:
            stdscr.addstr(0, 0, "✓ COMPRESSION SUCCESSFUL!", curses.A_BOLD)
            stdscr.addstr(2, 0, "Data compressed using PICKLE + GZIP")
            stdscr.addstr(3, 0, f"Saved to: {DATA_FILE}")
        else:
            stdscr.addstr(0, 0, "✗ COMPRESSION FAILED!", curses.A_BOLD)
            stdscr.addstr(2, 0, f"Error: {compression_status['error']}")
        
        stdscr.addstr(5, 0, "Press any key to continue...")
        stdscr.refresh()
        stdscr.nodelay(False)
        stdscr.getch()
        
        return compression_status["success"]
        
    except KeyboardInterrupt:
        stdscr.nodelay(False)
        return False


def decompress_data(stdscr):
    """Decompress students.dat and load data using pickle with gzip"""
    try:
        if not os.path.exists(DATA_FILE):
            return None
        
        stdscr.clear()
        stdscr.addstr(0, 0, "Decompressing data...", curses.A_BOLD)
        stdscr.refresh()
        
        # Decompress using gzip and pickle
        with gzip.open(DATA_FILE, 'rb') as f:
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
            stdscr.addstr(0, 0, "✓ Successfully decompressed students.dat!", curses.A_BOLD)
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
        stdscr.addstr(1, 0, "Decompressing and loading data using PICKLE + GZIP...")
        stdscr.refresh()
        return decompress_data(stdscr)
    return None
