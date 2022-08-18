#! /usr/bin/python3
import subprocess
import requests
import utils
import settings
import history
import platform
import init
from printcolor import colors

dependencies = [
    {
        "name": "node",
        "install": "curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.1/install.sh | bash && nvm install node"
    },
    {
        "name": "webtorrent",
        "install": "npm install -g webtorrent-cli"
    },
    {
        "name": "vlc",
        "install": "sudo apt-get install vlc"
    }
]

overrides_list, input_term = init.init()

saveHistory, showList, setup = settings.init()

if not setup:
    for dependency in dependencies:
        utils.check_dependencies(dependency)
    settings.save_setup(True)


if overrides_list:
    showList = True

base_url = "https://tpb23.ukpass.co/apibay/q.php?q="


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
        quality = input(
            "Enter your preferred quality (eg 720, 1080 etc). Enter nothing to leave default: ") or ""

    if saveHistory:
        history.append_to_history(search_term + "__" + quality)

    search_term = search_term.replace(" ", "%20")

    torrent_list_response = requests.get(base_url + search_term)

    torrent_list = torrent_list_response.json()

    # if list is empty then throw error
    if (torrent_list[0]["id"] == '0'):
        colors.warning("No torrents found")
        exit(1)

    torrent_list = list(
        filter(lambda x: x["name"].find(quality) > -1, torrent_list))

    best_torrent = get_best_torrent(torrent_list)

    if showList:
        table = []
        torrent_index = -1
        number_of_torrents = len(torrent_list)
        curr = number_of_torrents - 1
        if number_of_torrents > 10:
            curr = 9
        colors.message("Torrents found: " + str(number_of_torrents))
        table.append(["#", "Name", colors.green("Seeders"),
                     colors.red("Leechers"), colors.cyan("Size")])

        while curr <= number_of_torrents:
            table = [table[0]]
            for idx, torrent in enumerate(torrent_list[:curr]):
                table.append([str(idx + 1), torrent["name"],  colors.green(
                    torrent["seeders"]), colors.red(torrent["leechers"]), colors.cyan(utils.bytes_to_human(int(torrent["size"])))])

            utils.print_table(table)

            colors.message("\nChoose your torrent number")
            if curr < number_of_torrents:
                colors.message("OR Press m to see more")

            try:
                response = input()
                if response == "m":
                    if curr < number_of_torrents:
                        curr += number_of_torrents - curr >= 10 and 10 or number_of_torrents - curr
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

    bashCommand = ""
    if platform.platform().lower().find("macos") > -1:
        bashCommand = "webtorrent '" + torrent_url + "' --vlc --playlist"
    elif platform.platform().lower().find("linux") > -1:
        bashCommand = "notify-send 'Your torrent " + torrent_name + \
            " is now streaming' && " + "webtorrent '" + torrent_url + "' --vlc --playlist"
    # TODO test what works for windows and add it here

    process = subprocess.run(bashCommand, shell=True)

except KeyboardInterrupt:
    colors.warning("\nExiting...")
except:
    colors.error("\nSomething went wrong...")
