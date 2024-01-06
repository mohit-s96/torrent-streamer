## search and stream torrent videos

## Disclaimer

Downloading/streaming copyrighted content is illegal in most countries. Whatever you stream/download through this application is your resposibility. I am not responsible for how this software is used.

### Requirements

The program can install these automatically as well (must have python 3)

- nodejs

```sh
# install nvm

curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.1/
install.sh | bash

# install node through nvm

nvm use 16
```

- webtorrent

```sh
npm i -g webtorrent-cli
```

- vlc (or mpv or any other player which can play a stream)

### running

- make main.py executable with `chmod u+x main.py`
- run `./main.py -q <ypur search term>`
- run `./main.py --help` for help

### further enhancement

This doesn't work on windows so please submit a PR if you like, thanks.
