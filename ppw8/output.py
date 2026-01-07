import curses

def display_menu(stdscr):
    try:
        stdscr.clear()
        # Lấy kích thước hiện tại của terminal để tránh ghi tràn
        rows, cols = stdscr.getmaxyx()
        
        # Chỉ in nếu terminal đủ lớn
        if rows > 10:
            stdscr.addstr(0, 0, "=== UNIVERSITY MANAGEMENT SYSTEM (PW4) ===", curses.A_BOLD)
            stdscr.addstr(1, 0, "1. Add Students")
            stdscr.addstr(2, 0, "2. Add Courses")
            stdscr.addstr(3, 0, "3. Input Marks for a Course")
            stdscr.addstr(4, 0, "4. Show Student List & GPAs (Sorted)")
            stdscr.addstr(5, 0, "5. Exit")
            stdscr.addstr(7, 0, "Select an option: ")
        else:
            stdscr.addstr(0, 0, "Terminal too small!")
            
        stdscr.refresh()
        return stdscr.getch()
    except curses.error:
        # Bắt lỗi nếu terminal bị thay đổi kích thước đột ngột
        pass

def show_message(stdscr, message):
    stdscr.clear()
    stdscr.addstr(0, 0, message)
    stdscr.addstr(2, 0, "Press any key to continue...")
    stdscr.refresh()
    stdscr.getch()

def show_student_list(stdscr, students):
    stdscr.clear()
    stdscr.addstr(0, 0, "RANKING BY GPA (Descending):", curses.A_REVERSE)
    stdscr.addstr(1, 0, "-" * 50)
    
    line = 2
    rows, cols = stdscr.getmaxyx()
    for s in students:
        if line < rows - 2: # Kiểm tra xem còn dòng để in không
            stdscr.addstr(line, 0, str(s))
            line += 1
            
    stdscr.addstr(line + 1, 0, "Press any key to return...")
    stdscr.refresh()
    stdscr.getch()