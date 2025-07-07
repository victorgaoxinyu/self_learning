import sys
import shutil

# https://gist.github.com/ConnerWill/d4b6c776b509add763e17f9f113fd25b
# \033 is ANSI Escape
def save_cursor_positions():
    # ESC 7 - DEC
    sys.stdout.write('\0337')


def restore_cursor_positions():
    sys.stdout.write('\0338')


def move_to_top_of_screen():
    sys.stdout.write('\033[H')


def delete_line():
    sys.stdout.write('\033[2K')


def clear_line():
    sys.stdout.write('\033[2K\033[0G')  # ESC[0G: move cursor to column 0


def move_back_one_char():
    sys.stdout.write('\033[1D')  # ESC[1D: move cursor left 1 column


def move_to_bottom_of_screen() -> int:
    _, total_rows = shutil.get_terminal_size()
    input_row = total_rows - 1
    sys.stdout.write(f'\033[{input_row}E')  # ESC[#E: move cursor to beginning of line, # lines down
    return total_rows