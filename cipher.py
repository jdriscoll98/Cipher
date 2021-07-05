import curses
import ctypes
import struct

ROW = 25
COL = 80
TOP_LEFT_Y = 0
TOP_LEFT_X = 0
BOTTOM_RIGHT_Y = 25
BOTTOM_RIGHT_X = 80


def run_gui(background):

    text = "This is a haiku; it is not too long I think; but you may disagree"
    display_text = text
    key = "But there's one sound that no one knows... What does the Fox say?"
    # # Wait for user input

    status = "Application started successfully"
    while 1:
        background.clear()
        print_screen(background, status)
        print_menu(background)
        print_text_and_key(background, display_text, key)
        option = background.getkey()
        # if key is f or F, read text from a file
        if option == "f" or option == "F":
            tb = display_input_box(
                background, "Enter file to load below, then press [ENTER]"
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

        # if key is i or I, read text from user input
        elif option.lower() == "i":
            tb = display_input_box(
                background, "Enter new text below, then press [ENTER]"
            )
            new_text = get_input_from_user(tb)
            if new_text == "":
                status = "Cancelled user input of text (empty string)"
                continue
            text = new_text.strip().rstrip()
            status = "New text loaded into memory from user input"
        # if key is r or R, apply rust cipher to this text
        elif option.lower() == "r":
            lib = load_cipher_lib("./libxorcipher.so")
            text_bytes = text.encode("cp437")
            key_bytes = key.encode("cp437")
            # create a pointer to a new string the same length as the text
            shared_text = ctypes.create_string_buffer(len(text_bytes))
            # call the rust lib to encrypt the text
            lib.cipher(
                text_bytes, key_bytes, shared_text, len(text_bytes), len(key)
            )
            # get the value of the shared pointer
            text = shared_text.raw.decode("cp437")
            display_text = translate(text)
            status = "Applied Rust cipher"
            # pakuri_bytes = struct.pack("bb50s", 15, 6, b"Chuchu")
            # lib.cipher(pakuri_bytes, len(pakuri_bytes))
            # result = struct.unpack("bb50s", lib.result.value)
            # print(result.decode())
        # if key is p or P, apply python cipher to this text
        elif option.lower() == "p":
            status = "Applied Python cipher"
            text = text.encode("cp437")
            key = key.encode("cp437")
            # apply cipher
            text = cipher(text, key).decode("cp437")
            key = key.decode("cp437")
            display_text = translate(text)
            status = "Applied Python cipher"


def translate(text):
    ctrl_translation = str.maketrans(
        bytes(range(0, 32)).decode("cp437"),
        "�☺☻♥♦♣♠•◘○◙♂♀♪♫☼►◄↕‼¶§▬↨↑↓→←∟↔▲▼",
    )
    return text.translate(ctrl_translation)


def cipher(message: bytes, key: bytes) -> bytes:
    return bytes(
        [message[i] ^ key[i % len(key)] for i in range(0, len(message))]
    )


def get_input_from_user(textbox):
    value = textbox.edit()
    return value.strip().rstrip()


def display_input_box(background, msg):
    create_box(6, 78, 18, 1)
    background.addstr(19, COL // 2 - len(msg) // 2, msg)
    background.refresh()
    create_box(3, 68, 20, 6)
    input_area = curses.newwin(1, 65, 21, 7)
    return curses.textpad.Textbox(input_area)


def create_box(height, width, y, x):
    box = curses.newwin(height, width, y, x)
    box.box()
    box.refresh()
    return box


def print_screen(background, status):
    # display status message
    background.addstr(
        25,
        0,
        f"Status: {status}.",
    )
    background.refresh()
    # draw a 25 (row) x 80 (col) box
    screen = curses.newwin(ROW, COL, 0, 0)
    screen.box()
    screen.refresh()

    msg = "Welcome to the XOR-Cipher App!"
    background.addstr(1, COL // 2 - len(msg) // 2, msg)
    background.refresh()


def print_menu(background):
    menu = curses.newwin(10, 40, 3, 20)
    menu.box()

    menu.refresh()
    printOptionToScreen(background, "[F] Read text from a local file", 4)
    printOptionToScreen(background, "[I] Read text from user Input prompt", 5)
    printOptionToScreen(background, "[R] Apply Rust cipher to this text", 6)
    printOptionToScreen(background, "[P] Apply Python cipher to this text", 7)
    printOptionToScreen(background, "[V] Verify cipher results match", 8)
    printOptionToScreen(background, "[K] Change Key used for ciphers", 9)
    printOptionToScreen(background, "[B] Run Benchmarks on test (100000x)", 10)
    printOptionToScreen(background, "[Q] Quit the Application", 11)


def print_text_and_key(background, text, key):
    display = curses.newwin(4, 76, 13, 2)
    display.box()
    display.refresh()

    msg = f"TEXT [{text}]"
    background.addstr(
        14,
        4,
        msg,
    )

    msg = f"KEY  [{key}]"
    background.addstr(
        15,
        4,
        msg,
    )


def load_cipher_lib(library_path):
    lib = ctypes.cdll.LoadLibrary(library_path)
    return lib


def printOptionToScreen(background, msg, y):
    background.addstr(
        y,
        21,
        msg,
    )


if __name__ == "__main__":
    curses.wrapper(run_gui)
