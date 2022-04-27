import sys
import history
import settings
import utils


def init():
    history_toggle_option = ["--toggle-history", "-TH"]
    list_toggle_option = ["--toggle-list", "-TL"]
    show_list_option = ["--list", "-L"]
    history_list_option = ["--history", "-HL"]
    history_clear_option = ["--history-clear", "-HC"]
    help_option = "--help"

    overrides_list = False

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
        elif help_option in sys.argv:
            utils.print_help()
    return overrides_list
