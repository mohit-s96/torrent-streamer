#! /usr/bin/python3
import requests
import subprocess
from printcolor import colors
import utils


dependencies = ["node", "webtorrent", "vlc"]


def check_dependencies(command):
    process = subprocess.run(
        command + " --version", shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if(process.returncode != 0):
        colors.error("\n*****************************\n")
        colors.error(command + " is not installed. Please install " + command)
        colors.error("\n*****************************\n")
        exit(1)

    colors.success("found " + command)


for dependency in dependencies:
    check_dependencies(dependency)

base_url = "https://tpb23.ukpass.co/apibay/q.php?q="

try:
    search_term = input("Enter your search term: ")

    quality = input(
        "Enter your preferred quality (eg 720, 1080 etc). Enter nothing to leave default: ") or ""

    search_term = search_term.replace(" ", "+")

    torrent_list_response = requests.get(base_url + search_term)

    torrent_list = torrent_list_response.json()

    # if list is emtpy then throw error
    if(torrent_list[0]["id"] == '0'):
        colors.warning("No torrents found")
        exit(1)

    torrent_list = list(
        filter(lambda x: x["name"].find(quality) > -1, torrent_list))

    torrent_page_base_url = "https://tpb23.ukpass.co/description.php?id="

    best_seeders = int(torrent_list[0]["seeders"])
    best_torrent = torrent_list[0]

    for info in torrent_list:
        if int(info["seeders"]) > best_seeders:
            best_seeders = int(info["seeders"])
            best_torrent = info

    infohash = best_torrent["info_hash"]
    torrent_name = best_torrent["name"]

    torrent_url = utils.create_torrent_url(infohash, torrent_name)

    bashCommand = "notify-send 'Your torrent " + torrent_name + \
        " is now streaming' && " + "webtorrent '" + torrent_url + "' --vlc --playlist"

    process = subprocess.run(bashCommand, shell=True)

except KeyboardInterrupt:
    colors.warning("\nExiting...")
except:
    colors.error("\nSomething went wrong...")
