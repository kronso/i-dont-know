import curses
import json
import random
import time

from curses import wrapper

# def load_text():
#     type_words = []
#     with open("quote_test.txt", "r") as file:
#         words = file.readlines()
#     # for idx, ele in enumerate(words):
#     #     for idx1, char in enumerate(words):
#     #
#         type_words.append(random.choice(words).strip())
#         return " ".join(type_words)
from _curses import curs_set

saved_wpm = []
error = []
saved_accuracy = []
save_random = []

record_letter = []
record_time = []
# with open("data.json", encoding="utf-8-sig") as f:
#     data = json.load(f)
with open("quotes.json", encoding='cp1252') as f:
    data = json.load(f)


def CAPSLOCK_STATE():
    import ctypes
    hllDll = ctypes.WinDLL("User32.dll")
    VK_CAPITAL = 0x14
    return hllDll.GetKeyState(VK_CAPITAL)


def random_int():
    rand_idx = random.randint(0, 5421)
    save_random.append(rand_idx)
    return rand_idx


def load_quotes(quote):  # quote is not currently proportional with author
    return quote[random_int()]["quoteText"]


def load_author(quote):
    return quote[save_random[0]]["quoteAuthor"]


menu = [" P L A Y ", "", " P R O F I L E ", "", " E X I T "]


def title_intro(stdscr):
    h, w = stdscr.getmaxyx()
    title = "B A B O - T Y P E"
    heading = w // 2 - len(title) // 2
    pad = curses.newwin(1, 50, h // 3, heading)

    rand_response = ["YOU FUCKING SUCK", "KILL YOURSELF", "PLEASE DON'T PLAY", "close the fucking terminal please..."]
    test = random.choice(rand_response)
    saved_time = []
    rand_int = random.randint(0, len(title))
    rand_error = []

    for _ in range(rand_int):
        rand_int = random.randint(0, len(title))
        rand_error.append(rand_int)

    for ele in title:
        rand_time = random.uniform(0.01, 0.3)
        if ele == " ":
            saved_time.append(0)
        else:
            saved_time.append(rand_time)

    for idx, ele in enumerate(saved_time):
        colour = curses.color_pair(5)
        if idx in rand_error:
            colour = curses.color_pair(7)
        pad.addstr(title[idx], colour | curses.A_BOLD)
        pad.refresh()
        time.sleep(ele)
    if len(rand_error) > 5:
        stdscr.addstr(h - 10, w // 2 - len(test) // 2, test)


def main_menu(stdscr, selected_row_idx):
    stdscr.clear()
    h, w = stdscr.getmaxyx()

    for idx, row in enumerate(menu):
        x = w // 2 - len(row) // 2
        y = h // 2 - len(menu) // 2 + idx
        title = "B A B O - T Y P E"
        heading = w // 2 - len(title) // 2
        stdscr.addstr(h // 3, heading, title)
        if idx == selected_row_idx:
            stdscr.attron(curses.color_pair(6))
            stdscr.addstr(y, x, row)
            stdscr.attroff(curses.color_pair(6))
        else:
            stdscr.addstr(y, x, row)
    stdscr.refresh()


def display_text(stdscr, target, clock, current, wpm=0):
    h, w = stdscr.getmaxyx()
    x = w // 2 - len(target) // 2
    y = h // 2
    middle = x + len(target) // 2
    CAPSLOCK = CAPSLOCK_STATE()
    caps_pop = middle - (len(" CAPS LOCK ") // 2)
    if (CAPSLOCK & 0xffff) != 0:
        stdscr.addstr(y - 10, caps_pop, " CAPS LOCK ", curses.color_pair(6))
    stdscr.addstr(0, 0, "Press ")
    stdscr.addstr(0, 6, "[TAB]")  # curses.color_pair(6)
    stdscr.addstr(0, 11, " to force exit")
    stdscr.addstr(y + 5, middle, f"{wpm}")
    stdscr.addstr(y - 5, middle, f"{int(clock)}")
    stdscr.addstr(y, x, target)

    for idx, char in enumerate(current):
        correct_char = target[idx]
        colour = curses.color_pair(1)  # curses.color_pair(5)
        if char != correct_char:
            record_letter.append(char)
            if idx not in error:
                error.append(idx)
            colour = curses.color_pair(2)  # curses.color_pair(7)
        stdscr.addstr(y, x + idx, correct_char, colour | curses.A_BOLD)



def wpm_test(stdscr):
    target_text = load_quotes(data)  # load_text()
    current_text = []
    wpm = 0
    start_time = time.time()
    stdscr.nodelay(True)

    while True:
        time_elapsed = max(time.time() - start_time, 1)
        wpm = round((len(current_text) / (time_elapsed / 60)) / 5)

        stdscr.clear()
        display_text(stdscr, target_text, time_elapsed, current_text, wpm)
        stdscr.refresh()

        if len("".join(current_text)) == len(target_text):
            stdscr.nodelay(False)
            saved_wpm.append(int(wpm))
            break

        try:
            key = stdscr.getkey()
        except:
            continue

        if not current_text:
            start_time = time.time()
            curs_set(1)

        try:
            if ord(key) == 9:
                break
        except TypeError:
            break

        if key in (curses.KEY_BACKSPACE, "\b", "\x7f"):
            if len(current_text) > 0:
                current_text.pop()
        elif len(current_text) < len(target_text):
            current_text.append(key)

    # if len(current_text) < len(target_text):
    #     stdscr.clear()
    #     stdscr.addstr("error")
    #     stdscr.refresh()
    #     stdscr.nodelay(False)
    #     stdscr.getch()
    # elif len("".join(current_text)) == len(target_text):
    end_data(stdscr, current_text, target_text, wpm, time_elapsed)


# def record_data(current_text, time_elapsed):


def end_data(stdscr, current, target, wpm, time_elapsed):
    stdscr.clear()
    curs_set(0)
    if len("".join(current)) != len(target):
        wpm = None
        time_elapsed = None
    if wpm and time_elapsed is not None:
        for idx, char in enumerate(current):
            colour = curses.color_pair(4)
            stdscr.addstr(2, 0 + idx, char, colour)

        for idx, ele in enumerate(error):
            error_pos = current[ele]
            colour = curses.color_pair(4)
            if ele != error_pos:
                colour = curses.color_pair(7) | curses.A_BOLD
            stdscr.addstr(2, 0 + error[idx], target[ele], colour)
        stdscr.addstr(3, 0, f"- {load_author(data)}")
        if load_author(data) == "":
            stdscr.addstr(3, 0, "- Unknown")
    else:
        stdscr.addstr(2, 0, "No data gathered due to force exit", curses.color_pair(8) | curses.A_BOLD)
    save_random.clear()
    stdscr.addstr(5, 0, "Typing speed: ")
    stdscr.addstr(5, 14, str(wpm), curses.color_pair(5) | curses.A_BOLD)
    if len(str(wpm)) == 1:
        stdscr.addstr(5, 16, "WPM")
    elif len(str(wpm)) == 2:
        stdscr.addstr(5, 17, "WPM")
    elif len(str(wpm)) == 3:
        stdscr.addstr(5, 18, "WPM")

    stdscr.addstr(6, 0, f"Duration:")
    if time_elapsed is None:
        stdscr.addstr(6, 10, f"{time_elapsed}", curses.color_pair(5) | curses.A_BOLD)
    else:
        stdscr.addstr(6, 10, f"{time_elapsed:.1f}", curses.color_pair(5) | curses.A_BOLD)
        if len(str(f"{time_elapsed:.1f}")) == 3:
            stdscr.addstr(6, 14, "seconds")
        elif len(str(f"{time_elapsed:.1f}")) == 4:
            stdscr.addstr(6, 15, "seconds")
        elif len(str(f"{time_elapsed:.1f}")) == 5:
            stdscr.addstr(6, 16, "seconds")
    net_wpm = len(target) - len(error)
    if wpm and time_elapsed is not None:
        accuracy = (int(net_wpm) / len(target)) * 100
        saved_accuracy.append(accuracy)
        stdscr.addstr(7, 0, f"Accuracy:")
        stdscr.addstr(7, 10, f"{accuracy:.1f}", curses.color_pair(5))
        if len(str(int(accuracy))) == 1:
            stdscr.addstr(7, 14, "%")
        elif len(str(int(accuracy))) == 2:
            stdscr.addstr(7, 15, "%")
        elif len(str(int(accuracy))) == 3:
            stdscr.addstr(7, 16, "%")
    else:
        stdscr.addstr(7, 0, f"Accuracy:")
        stdscr.addstr(7, 10, "None", curses.color_pair(5))
    error.clear()
    stdscr.addstr(9, 0, "Press ")
    stdscr.addstr(9, 6, " TAB ", curses.color_pair(6))
    stdscr.addstr(9, 12, "to play again")
    stdscr.addstr(11, 0, "Press ")
    stdscr.addstr(11, 6, " ENTER ", curses.color_pair(6))
    stdscr.addstr(11, 14, "to return to menu")
    stdscr.refresh()
    stdscr.nodelay(False)
    key = stdscr.getch()
    if ord("\t") == key:
        wpm_test(stdscr)
    elif key == curses.KEY_ENTER or key in [10, 13]:
        stdscr.clear()
        stdscr.refresh()


def profile(stdscr):
    stdscr.clear()
    max_wpm = 0
    max_accuracy = 0
    for x in saved_wpm:
        max_wpm += x
    for x in saved_accuracy:
        max_accuracy += x
    stdscr.addstr(0, 0, "Average WPM: ")
    stdscr.addstr(1, 0, "Average accuracy: ")
    try:
        average_wpm = max_wpm / len(saved_wpm)
        average_accuracy = max_accuracy / len(saved_accuracy)
        stdscr.addstr(0, 13, f"{average_wpm:.1f}", curses.color_pair(5))
        stdscr.addstr(1, 18, f"{average_accuracy:.1f}", curses.color_pair(5))
        if len(str(int(average_accuracy))) == 1:
            stdscr.addstr(1, 22, "%")
        elif len(str(int(average_accuracy))) == 2:
            stdscr.addstr(1, 23, "%")
        elif len(str(int(average_accuracy))) == 3:
            stdscr.addstr(1, 24, "%")
    except ZeroDivisionError:
        stdscr.addstr(0, 13, "0", curses.color_pair(5))
        stdscr.addstr(1, 18, "0", curses.color_pair(5))
        stdscr.addstr(1, 20, "%")

    stdscr.addstr(2, 0, f"Tests completed: ")
    stdscr.addstr(2, 17, f"{len(saved_wpm)}", curses.color_pair(5))

    stdscr.addstr(6, 0, "Press any key to continue...")
    stdscr.getkey()
    stdscr.refresh()


def main(stdscr):
    curses.use_default_colors()
    curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_WHITE, curses.COLOR_RED)
    curses.init_pair(3, curses.COLOR_BLACK, curses.COLOR_WHITE)
    curses.init_pair(4, curses.COLOR_WHITE, curses.COLOR_BLACK)
    curses.init_color(
        255,
        0x43 * 1000 // 0xff,
        0xff * 1000 // 0xff,
        0xaf * 1000 // 0xff
    )
    curses.init_color(
        254,
        0xff * 1000 // 0xff,
        0x58 * 1000 // 0xff,
        0x58 * 1000 // 0xff,
    )
    # GREEN FG BLACK BG
    curses.init_pair(5, 255, -1)
    # BLACK FG GREEN BG
    curses.init_pair(6, curses.COLOR_BLACK, 255)
    # WHITE FG RED BG
    curses.init_pair(7, -1, 254)
    # RED FG WHITE BG
    curses.init_pair(8, 254, -1)
    current_row_idx = 0
    main_menu(stdscr, current_row_idx)
    curs_set(1)
    title_intro(stdscr)
    curs_set(0)
    while 1:
        key = stdscr.getch()
        stdscr.clear()
        if key == curses.KEY_UP and current_row_idx > 0:
            current_row_idx -= 2
        elif key == curses.KEY_DOWN and current_row_idx < len(menu) - 1:
            current_row_idx += 2
        elif key == curses.KEY_ENTER or key in [10, 13] and current_row_idx == 0:
            wpm_test(stdscr)
        elif key == curses.KEY_ENTER or key in [10, 13] and current_row_idx == 2:
            profile(stdscr)
        elif key == curses.KEY_ENTER or key in [10, 13] and current_row_idx == 4:
            break
        main_menu(stdscr, current_row_idx)
        stdscr.refresh()


wrapper(main)
