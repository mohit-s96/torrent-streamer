import utils
import json

config_path = utils.get_file_path("config.json")
app_config = None

PLAYERS = {"VLC": "vlc", "MPV": "mpv"}

PROVIDERS = {"TPB": "tpb"}


class AppConfig:
    def __init__(self, save_history, show_list, setup, provider, player):
        self.save_history = save_history
        self.show_list = show_list
        self.setup = setup
        self.provider = provider
        self.player = player

    def get_provider(self):
        import providers.providers as providers

        return providers.get_provider_based_on_config(self.provider)


def load_config():
    global app_config
    # my defaults
    # ------------------------------------
    save_history = True
    show_list = True
    setup = False
    provider = PROVIDERS.get("TPB")
    player = PLAYERS.get("VLC")
    # ------------------------------------

    settings = utils.read_file(config_path)
    if settings == None:
        print("config.json not found. Creating a new one...")
        utils.write_file(
            config_path,
            dict_to_json(
                {
                    "history": True,
                    "list": False,
                    "setup": False,
                    "provider": provider,
                    "player": player,
                }
            ),
        )
    else:
        settings = json_to_dict(settings)
        if "history" in settings:
            save_history = settings["history"]
        if "list" in settings:
            show_list = settings["list"]
        if "setup" in settings:
            setup = settings["setup"]
        if "provider" in settings:
            provider = settings["provider"]
        if "player" in settings:
            player = settings["player"]

    app_config = AppConfig(save_history, show_list, setup, provider, player)


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


def save_setup(setup):
    settings = utils.read_file(config_path)
    settings = json_to_dict(settings)
    settings["setup"] = setup
    utils.write_file(config_path, dict_to_json(settings))
