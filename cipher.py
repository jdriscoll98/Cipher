import curses
from curses.textpad import rectangle

ROW = 25
COL = 80
TOP_LEFT_Y = 0
TOP_LEFT_X = 0
BOTTOM_RIGHT_Y = 25
BOTTOM_RIGHT_X = 80


def main(stdscr):

    text = "This is a haiku; it is not too long I think; but you may disagree"
    key = "But there's one sound that no one knows... What does the Fox say?"
    # # Wait for user input

    status = "Application started successfully"
    while 1:
        stdscr.clear()
        print_screen(stdscr, status)
        print_menu(stdscr)
        print_text_and_key(stdscr, text, key)
        option = stdscr.getkey()
        # if key is f or F, read text from a file
        if option == "f" or option == "F":
            tb = display_input_box(
                stdscr, "Enter file to load below, then press [ENTER]"
            )
            filename = get_input_from_user(tb)
            if filename == "":
                status = "File load cancelled"
                continue

            try:
                with open(filename, "r") as f:
                    text = f.read().strip().rstrip()
                    status = "File contents loaded successfully"
            except IOError:
                status = f"ERROR: COULD NOT LOAD FILE: {filename}"


def get_input_from_user(textbox):
    value = textbox.edit()
    return value.strip().rstrip()


def display_input_box(stdscr, msg):
    create_box(6, 78, 18, 1)
    stdscr.addstr(19, COL // 2 - len(msg) // 2, msg)
    stdscr.refresh()
    create_box(3, 68, 20, 6)
    input_area = curses.newwin(1, 65, 21, 7)
    return curses.textpad.Textbox(input_area)


def create_box(height, width, y, x):
    box = curses.newwin(height, width, y, x)
    box.box()
    box.refresh()
    return box


def print_screen(stdscr, status):
    # display status message
    stdscr.addstr(
        25,
        0,
        f"Status: {status}.",
    )
    stdscr.refresh()
    # draw a 25 (row) x 80 (col) box
    screen = curses.newwin(ROW, COL, 0, 0)
    screen.box()
    screen.refresh()

    msg = "Welcome to the XOR-Cipher App!"
    stdscr.addstr(1, COL // 2 - len(msg) // 2, msg)
    stdscr.refresh()


def print_menu(stdscr):
    menu = curses.newwin(10, 40, 3, 20)
    menu.box()

    menu.refresh()
    printOptionToScreen(stdscr, "[F] Read text from a local file", 4)
    printOptionToScreen(stdscr, "[I] Read text from user Input prompt", 5)
    printOptionToScreen(stdscr, "[R] Apply Rust cipher to this text", 6)
    printOptionToScreen(stdscr, "[P] Apply Python cipher to this text", 7)
    printOptionToScreen(stdscr, "[V] Verify cipher results match", 8)
    printOptionToScreen(stdscr, "[K] Change Key used for ciphers", 9)
    printOptionToScreen(stdscr, "[B] Run Benchmarks on test (100000x)", 10)
    printOptionToScreen(stdscr, "[Q] Quit the Application", 11)


def print_text_and_key(stdscr, text, key):
    display = curses.newwin(4, 76, 13, 2)
    display.box()
    display.refresh()

    msg = f"TEXT [{text}]"
    stdscr.addstr(
        14,
        4,
        msg,
    )

    msg = f"KEY  [{key}]"
    stdscr.addstr(
        15,
        4,
        msg,
    )


# def start_terminal():
#     stdscr = curses.initscr()
#     curses.noecho()
#     curses.cbreak()
#     stdscr.keypad(True)
#     return stdscr


# def end_terminal(stdscr):
# curses.nocbreak()
# stdscr.keypad(False)
# curses.echo()
# curses.endwin()


def printOptionToScreen(stdscr, msg, y):
    stdscr.addstr(
        y,
        21,
        msg,
    )


if __name__ == "__main__":
    curses.wrapper(main)
