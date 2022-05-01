import utils
import settings

history_path = utils.get_file_path("history.json")


def append_to_history(item):
    if not utils.check_file_exists(history_path):
        utils.write_file(history_path, "[]")
    history = utils.read_file(history_path)
    history = settings.json_to_dict(history)
    history.append(item)
    utils.write_file(history_path, settings.dict_to_json(history))


def print_history():
    if not utils.check_file_exists(history_path):
        print("No history found")
        exit(1)
    history = utils.read_file(history_path)
    history = settings.json_to_dict(history)
    for item in history:
        print(item)
    exit(0)


def clear_history():
    if not utils.check_file_exists(history_path):
        print("No history found")
        exit(1)
    utils.write_file(history_path, "[]")
    print("History cleared")
    exit(0)
