from math import fabs
import sys
import history
import settings
import utils
from printcolor import colors


def parse_input_buffer(input_str):
    options_dict = {
        "-q": "",
        "-dl": False,
        "-o": ""
    }

    current_buffer = ""
    result = ""
    current_option = ""

    for i in range(0, len(input_str)):
        curr_char = input_str[i]
        if curr_char == " ":
            if current_buffer in options_dict:
                if current_option != "":
                    options_dict[current_option] = True if (
                        current_option == "-dl") else result
                    result = ""
                current_option = current_buffer
                current_buffer = ""
            else:
                result += current_buffer + " "
                current_buffer = ""
        else:
            current_buffer += curr_char
    if current_buffer in options_dict:
        options_dict[current_buffer] = True
        current_buffer = ""
    if (current_option):
        options_dict[current_option] = result + current_buffer
    for key in options_dict:
        if isinstance(options_dict[key], str):
            options_dict[key] = options_dict[key].strip()
    return options_dict


def init():
    history_toggle_option = ["--toggle-history", "-TH"]
    list_toggle_option = ["--toggle-list", "-TL"]
    show_list_option = ["--list", "-L"]
    history_list_option = ["--history", "-HL"]
    history_clear_option = ["--history-clear", "-HC"]
    direct_search_option = "-q"
    pick_from_history_option = "-ph"
    help_option = "--help"

    overrides_list = False
    input_term = ""
    options_dict = {}

    if len(sys.argv) > 1:
        if any(option in sys.argv for option in history_toggle_option):
            saveHistory = not settings.get_setting("history")
            settings.save_history(saveHistory)
            print("History tracking has been switched " +
                  ("on" if saveHistory else "off"))
        elif any(option in sys.argv for option in list_toggle_option):
            showList = not settings.get_setting("list")
            settings.save_list(showList)
            print("List has been switched " + ("on" if showList else "off"))
        elif any(option in sys.argv for option in show_list_option):
            overrides_list = True
        elif any(option in sys.argv for option in history_list_option):
            history.print_history()
        elif any(option in sys.argv for option in history_clear_option):
            history.clear_history()
        elif direct_search_option in sys.argv:
            if not sys.stdin.isatty():
                input_term = "-q " + sys.stdin.readlines()[0]
                sys.stdin = open("/dev/tty")
                options_dict = parse_input_buffer(input_term)
                input_term = options_dict["-q"]
            else:
                input_term = " ".join(sys.argv[1:])
                options_dict = parse_input_buffer(input_term)
                input_term = options_dict["-q"]
        elif pick_from_history_option in sys.argv:
            try:
                history_num = int(sys.argv[2])
                input_term = history.get_history_at_index(history_num)
            except ValueError:
                print("Invalid index")
                exit(0)
            except:
                colors.error("Something went wrong. Invalid input maybe??")
                exit(0)
        elif help_option in sys.argv:
            utils.print_help()
    return overrides_list, options_dict
