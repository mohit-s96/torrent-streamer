import sys
import history
import settings
import utils
from printcolor import colors


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
                input_term = sys.stdin.readlines()[0]
                sys.stdin = open("/dev/tty")
            else:
                input_term = " ".join(sys.argv[2:])
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
    return overrides_list, input_term
