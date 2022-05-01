import utils
import json

config_path = utils.get_file_path("config.json")


def init():
    saveHistory = True
    showList = False
    settings = utils.read_file(config_path)
    if settings == None:
        print("config.json not found. Creating a new one...")
        utils.write_file(config_path, dict_to_json(
            {"history": True, "list": False}))
    else:
        settings = json_to_dict(settings)
        if "history" in settings:
            saveHistory = settings["history"]
        if "list" in settings:
            showList = settings["list"]
    return saveHistory, showList


def json_to_dict(str):
    return json.loads(str)


def dict_to_json(dict):
    return json.dumps(dict)


def save_history(history):
    settings = utils.read_file(config_path)
    settings = json_to_dict(settings)
    settings["history"] = history
    utils.write_file(config_path, dict_to_json(settings))


def save_list(list):
    settings = utils.read_file(config_path)
    settings = json_to_dict(settings)
    settings["list"] = list
    utils.write_file(config_path, dict_to_json(settings))


def get_setting(setting):
    settings = utils.read_file(config_path)
    settings = json_to_dict(settings)
    return settings[setting]
