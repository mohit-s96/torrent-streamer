import utils
import config

history_path = utils.get_file_path("history.json")


def append_to_history(item):
    if not utils.check_file_exists(history_path):
        utils.write_file(history_path, "[]")
    history = utils.read_file(history_path)
    history = config.json_to_dict(history)

    found = False
    for i in range(len(history)):
        if history[i]["item"] == item:
            found = True
            history[i]["timestamps"].append(utils.get_timestamp())
    if not found:
        history.append({"item": item, "timestamps": [utils.get_timestamp()]})
    utils.write_file(history_path, config.dict_to_json(history))


def print_history():
    if not utils.check_file_exists(history_path):
        print("No history found")
        exit(1)
    history = utils.read_file(history_path)
    history = config.json_to_dict(history)
    if len(history) == 0:
        print("No history found")
        exit(1)
    table = []
    table.append(["#", "Item", "Last Searched"])
    for i in range(len(history)):
        table.append([str(i + 1), history[i]["item"], history[i]["timestamps"][0]])
    utils.print_table(table)
    exit(0)


def get_history_at_index(idx):
    if not utils.check_file_exists(history_path):
        print("No history found")
        exit(1)
    history = utils.read_file(history_path)
    history = config.json_to_dict(history)
    if len(history) == 0:
        print("No history found")
        exit(1)
    history_item = history[idx - 1]["item"][0:-2]
    if history_item[-1] == "\n":
        history_item = history_item[0:-1]
    return history_item


def clear_history():
    if not utils.check_file_exists(history_path):
        print("No history found")
        exit(1)
    utils.write_file(history_path, "[]")
    print("History cleared")
    exit(0)
