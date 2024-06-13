#! /usr/bin/python3
from importlib.resources import path
import subprocess
from time import sleep
import utils
import settings
import history
import platform
import init
import json
from printcolor import colors

dependencies = [
    {
        "name": "node",
        "install": "curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.1/install.sh | bash && nvm install node",
    },
    {"name": "webtorrent", "install": "npm install -g webtorrent-cli"},
    {"name": "vlc", "install": "sudo apt-get install vlc"},
]

overrides_list, options_dict = init.init()

input_term = options_dict.get("-q")
download = options_dict.get("-dl")
save_path = options_dict.get("-o")
debug = options_dict.get("-dbg")

saveHistory, showList, setup = settings.init()

if not setup:
    for dependency in dependencies:
        utils.check_dependencies(dependency)
    settings.save_setup(True)


if overrides_list:
    showList = True

base_url = "https://tpb34.ukpass.co/apibay/q.php?q="


def get_best_torrent(torrent_list):
    best_seeders = int(torrent_list[0]["seeders"])
    best_torrent = torrent_list[0]

    for info in torrent_list:
        if int(info["seeders"]) > best_seeders:
            best_seeders = int(info["seeders"])
            best_torrent = info
    return best_torrent


try:
    search_term = input_term or input("Enter your search term: ")

    quality = ""
    if not input_term:
        quality = (
            input(
                "Enter your preferred quality (eg 720, 1080 etc). Enter nothing to leave default: "
            )
            or ""
        )

    if saveHistory:
        history.append_to_history(search_term + "__" + quality)

    search_term = search_term.replace(" ", "%20")
    curl_cmd = f'curl "{base_url + search_term + "&cat="}"'
    response = subprocess.run(curl_cmd, shell=True, capture_output=True, text=True)
    torrent_list = json.loads(response.stdout)

    # if list is empty then throw error
    if torrent_list[0]["id"] == "0":
        colors.warning("No torrents found")
        exit(1)

    torrent_list = list(filter(lambda x: x["name"].find(quality) > -1, torrent_list))

    best_torrent = get_best_torrent(torrent_list)

    if showList:
        table = []
        torrent_index = -1
        number_of_torrents = len(torrent_list)
        curr = number_of_torrents - 1
        if number_of_torrents > 10:
            curr = 9
        colors.message("Torrents found: " + str(number_of_torrents))
        table.append(
            [
                "#",
                "Name",
                colors.green("Seeders"),
                colors.red("Leechers"),
                colors.cyan("Size"),
            ]
        )

        while curr <= number_of_torrents:
            table = [table[0]]
            for idx, torrent in enumerate(torrent_list[:curr]):
                table.append(
                    [
                        str(idx + 1),
                        torrent["name"],
                        colors.green(torrent["seeders"]),
                        colors.red(torrent["leechers"]),
                        colors.cyan(utils.bytes_to_human(int(torrent["size"]))),
                    ]
                )

            utils.print_table(table)

            colors.message("\nChoose your torrent number")
            if curr < number_of_torrents:
                colors.message("OR Press m to see more")

            try:
                print("> ", end="")
                response = input()
                if response == "m":
                    if curr < number_of_torrents:
                        curr += (
                            number_of_torrents - curr >= 10
                            and 10
                            or number_of_torrents - curr
                        )
                    else:
                        colors.warning("No more torrents to show")
                else:
                    torrent_index = int(response) - 1
            except ValueError:
                colors.success("\nChoosing the best torrent automatically")
                break
            if torrent_index >= 0 and torrent_index < len(torrent_list):
                best_torrent = torrent_list[torrent_index]
                break

    infohash = best_torrent["info_hash"]
    torrent_name = best_torrent["name"]
    torrent_url = utils.create_torrent_url(infohash, torrent_name)
    stream_or_dl = "streaming" if not download else "downloading"

    bash_command = "webtorrent '" + torrent_url + "'"

    if not download:
        bash_command += " --vlc --playlist"
    if save_path != "" and save_path != None:
        bash_command += " -o " + "'" + save_path + "'"
    # TODO test what works for windows and add it here
    print(stream_or_dl + " " + torrent_name)
    sleep(2)
    process = subprocess.run(bash_command, shell=True)

except KeyboardInterrupt:
    colors.warning("\nExiting...")
except Exception as e:
    if debug:
        print(str(e))
    colors.error("\nSomething went wrong...")
