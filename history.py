import utils
import settings


def append_to_history(item):
    if not utils.check_file_exists("history.json"):
        utils.write_file("history.json", "[]")
    history = utils.read_file("history.json")
    history = settings.json_to_dict(history)
    history.append(item)
    utils.write_file("history.json", settings.dict_to_json(history))


def print_history():
    if not utils.check_file_exists("history.json"):
        print("No history found")
        exit(1)
    history = utils.read_file("history.json")
    history = settings.json_to_dict(history)
    for item in history:
        print(item)
    exit(0)


def clear_history():
    if not utils.check_file_exists("history.json"):
        print("No history found")
        exit(1)
    utils.write_file("history.json", "[]")
    print("History cleared")
    exit(0)
