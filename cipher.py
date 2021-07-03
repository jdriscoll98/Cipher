import curses
from curses.textpad import rectangle


def main(stdscr):
    stdscr.clear()
    print_screen(stdscr)
    print_menu(stdscr)

    text = "This is a haiku; it is not too long; but you may disagree"
    key = "But there's one sound that no one knows... What does the Fox say?"
    print_text_and_key(stdscr, text, key)

    stdscr.refresh()

    # Wait for user input
    stdscr.getkey()


def print_screen(stdscr):
    rectangle(stdscr, 2, 2, curses.LINES - 2, curses.COLS - 2)

    stdscr.addstr(
        curses.LINES - 1,
        0,
        "Status: Application started successfully.",
    )

    stdscr.addstr(
        3,
        (curses.COLS - len("Welcome to the XOR-Cipher App!")) // 2,
        "Welcome to the XOR-Cipher App!",
    )

    # draw a small rectange in the middle of the screen
    rectangle(
        stdscr,
        4,
        curses.COLS // 2 - 20,
        13,
        curses.COLS // 2 + 20,
    )


def print_menu(stdscr):
    printOptionToScreen(stdscr, "[F] Read text from a local file", 5)
    printOptionToScreen(stdscr, "[I] Read text from user Input prompt", 6)
    printOptionToScreen(stdscr, "[R] Apply Rust cipher to this text", 7)
    printOptionToScreen(stdscr, "[P] Apply Python cipher to this text", 8)
    printOptionToScreen(stdscr, "[V] Verify cipher results match", 9)
    printOptionToScreen(stdscr, "[K] Change Key used for ciphers", 10)
    printOptionToScreen(stdscr, "[B] Run Benchmarks on test", 11)
    printOptionToScreen(stdscr, "[Q] Quit the Application", 12)


def print_text_and_key(stdscr, text, key):
    rectangle(
        stdscr,
        curses.LINES // 2,
        4,
        curses.LINES // 2 + 3,
        curses.COLS - 4,
    )
    msg = f"TEXT [{text}]"
    stdscr.addstr(
        curses.LINES // 2 + 1,
        (curses.COLS - len(msg)) // 2,
        msg,
    )

    msg = f"KEY [{key}]"
    # print message on screen left aligned to x = 4
    stdscr.addstr(
        curses.LINES // 2 + 2,
        (curses.COLS - len(msg)) // 2,
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
        max(curses.COLS // 2 - 18, curses.COLS // 2 - len(msg)),
        msg,
    )


if __name__ == "__main__":
    curses.wrapper(main)
