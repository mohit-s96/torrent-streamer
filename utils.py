import sys
import os
import subprocess
import urllib.parse

from printcolor import colors


def encodeURIComponent(str):
    return urllib.parse.quote(str.encode("utf-8"))


def generate_trackers():
    tr = '&tr=' + \
        encodeURIComponent('udp://tracker.coppersurfer.tk:6969/announce')
    tr += '&tr=' + \
        encodeURIComponent(
            'udp://tracker.openbittorrent.com:6969/announce')
    tr += '&tr=' + encodeURIComponent('udp://tracker.opentrackr.org:1337')
    tr += '&tr=' + encodeURIComponent('udp://movies.zsw.ca:6969/announce')
    tr += '&tr=' + \
        encodeURIComponent('udp://tracker.dler.org:6969/announce')
    tr += '&tr=' + \
        encodeURIComponent('udp://opentracker.i2p.rocks:6969/announce')
    tr += '&tr=' + encodeURIComponent('udp://open.stealth.si:80/announce')
    tr += '&tr=' + encodeURIComponent('udp://tracker.0x.tf:6969/announce')
    return tr


def check_dependencies(command):
    process = subprocess.run(
        command["name"] + " --version", shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if(process.returncode != 0):
        colors.warning("\n*****************************\n")
        colors.warning(
            command["name"] + " is not installed. Do you want to install " + command["name"] + " (requires root privilege)")
        colors.warning("\n*****************************\n")
        if(input("y/n: ") == "y"):
            subprocess.run(command["install"], shell=True)
        else:
            colors.warning("Exiting...")
            exit(1)

    colors.success("found " + command["name"])


def create_torrent_url(info_hash, torrent_name):
    url = 'magnet:?xt=urn:btih:' + info_hash + '&dn=' + \
        encodeURIComponent(torrent_name) + generate_trackers()
    return url


def check_root_access():
    if os.geteuid() == 0:
        return True
    return False


def prompt_root_access():
    subprocess.check_call(['sudo', sys.executable] + sys.argv)
