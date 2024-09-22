import sys
import os
import subprocess
import urllib.parse
import pwd
import pathlib
from datetime import datetime
from printcolor import colors


current_path = pathlib.Path(__file__).parent.resolve()
script_dir = os.path.dirname(os.path.realpath(__file__))
process_dir = os.getcwd()


def get_file_path(file_name):
    return current_path / file_name


def encodeURIComponent(str):
    return urllib.parse.quote(str.encode("utf-8"))


def generate_trackers():
    tr = "&tr=" + encodeURIComponent("udp://tracker.coppersurfer.tk:6969/announce")
    tr += "&tr=" + encodeURIComponent("udp://tracker.openbittorrent.com:6969/announce")
    tr += "&tr=" + encodeURIComponent("udp://tracker.opentrackr.org:1337")
    tr += "&tr=" + encodeURIComponent("udp://movies.zsw.ca:6969/announce")
    tr += "&tr=" + encodeURIComponent("udp://tracker.dler.org:6969/announce")
    tr += "&tr=" + encodeURIComponent("udp://opentracker.i2p.rocks:6969/announce")
    tr += "&tr=" + encodeURIComponent("udp://open.stealth.si:80/announce")
    tr += "&tr=" + encodeURIComponent("udp://tracker.0x.tf:6969/announce")
    return tr


def check_dependencies(command):
    process = subprocess.run(
        command["name"] + " --version",
        shell=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    if process.returncode != 0:
        colors.warning("\n*****************************\n")
        colors.warning(
            command["name"]
            + " is not installed. Do you want to install "
            + command["name"]
            + " (requires root privilege)"
        )
        colors.warning("\n*****************************\n")
        if input("y/n: ") == "y":
            # if the dependency is from npm then we don't need root access
            if command["install"].startswith("npm"):
                if check_root_access():
                    uid = pwd.getpwuid(os.geteuid()).pw_uid
                    os.setuid(uid)
            subprocess.run(command["install"], shell=True)
        else:
            colors.warning("Exiting...")
            exit(1)

    colors.success("found " + command["name"])


def create_torrent_url(info_hash, torrent_name):
    url = (
        "magnet:?xt=urn:btih:"
        + info_hash
        + "&dn="
        + encodeURIComponent(torrent_name)
        + generate_trackers()
    )
    return url


def drop_root_access():
    if check_root_access():
        uid = pwd.getpwuid(os.geteuid()).pw_uid
        os.setuid(uid)


def check_root_access():
    if os.geteuid() == 0:
        return True
    return False


def prompt_root_access():
    subprocess.check_call(["sudo", sys.executable] + sys.argv)


def check_file_exists(file_path):
    return os.path.isfile(file_path)


def read_file(file_path):
    if check_file_exists(file_path):
        with open(file_path, "r") as f:
            return f.read()
    return None


def write_file(file_path, content):
    with open(file_path, "w") as f:
        f.write(content)


def print_help():
    colors.info("\n*****************************\n")
    colors.info("Usage: " + sys.argv[0] + " " + "--option")
    colors.info("\noptions:\n")
    colors.info("--help: print this help")
    colors.info("--upgrade: Update to the latest available version")
    colors.info(
        "--list | -L : list all the torrents and let the user decide which one to choose"
    )
    colors.info("--toggle-history | -TH : toggle saving history on or off")
    colors.info("--toggle-list | -TL : switch the default list mode on or off")
    colors.info("--history | -HL : list search history")
    colors.info("--history-clear | -HC : clear search history")
    colors.info("-q [query term] : Search directly or pipe the results from stdin")
    colors.info(
        "-ph [history index] : pass the index of an item from history to search for it again"
    )
    colors.info("-dl : download the torrent instead of streaming")
    colors.info("-o [location] : change the output location of downloads")
    colors.info("-dbg : enable debug logging in case of errors")
    colors.info("\n*****************************\n")
    exit(0)


def print_table(table):
    """
    Prints a table in a nice way.
    """
    col_width = [max(len(str(row[i])) for row in table) for i in range(len(table[0]))]
    for row in table:
        for i in range(len(row)):
            print(str(row[i]).ljust(col_width[i] + 1), end="")
        print("")


def bytes_to_human(n):
    """
    Returns a human readable string for a given number of bytes
    """
    symbols = ("K", "M", "G", "T", "P", "E", "Z", "Y")
    prefix = {}
    for i, s in enumerate(symbols):
        prefix[s] = 1 << (i + 1) * 10
    for s in reversed(symbols):
        if n >= prefix[s]:
            value = float(n) / prefix[s]
            return "%.2f%s" % (value, s)
    return "%sB" % n


def get_timestamp():
    return str(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))


def upgrade():
    code = 0
    if script_dir != process_dir:
        os.chdir(script_dir)
    process = subprocess.run(
        "git reset --hard && git pull",
        shell=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    if process.returncode != 0:
        print(process.stderr)
        colors.error(
            "Error upgrading the application. Please file a bug at https://github.com/mohit-s96/torrent-streamer/issues"
        )
        code = 1
    else:
        colors.success("Updated successfully")

    if script_dir != process_dir:
        os.chdir(process_dir)
    exit(code)
