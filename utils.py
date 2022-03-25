import urllib.parse


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


def create_torrent_url(info_hash, torrent_name):
    url = 'magnet:?xt=urn:btih:' + info_hash + '&dn=' + \
        encodeURIComponent(torrent_name) + generate_trackers()
    return url
