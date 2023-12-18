from requests import get
from io import BytesIO
from PIL import Image
from datetime import datetime
import json

import bot.src.consts as consts


def get_formatted_datetime(as_path=False):
    time = datetime.now()
    if as_path:
        return time.strftime("%d-%m-%Y_%H-%M-%S")
    return time.strftime("%d/%m/%Y %H:%M:%S")


def initialize_log():
    name = get_formatted_datetime(as_path=True) + ".txt"
    path = consts.LOG_PATH + name
    open(path, "w+").close()
    consts.set_log_file(name)
    return path


def pinata2ipfs_url(pinata_url):
    cid = pinata_url.split("/")[-1]
    return f"https://ipfs.io/ipfs/{cid}"


def log(text, depth=0):
    msg = "[" + get_formatted_datetime() + "] " + ("--> " * depth) + text
    print(msg)


def read_json(path):
    data = ""
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)
    return data


def write_json(path, data):
    text = json.dumps(data)
    with open(path, "w+") as outfile:
        outfile.write(text)


def fetch_image(url, size=None):
    response = get(url)
    image = Image.open(BytesIO(response.content))
    if size:
        image.resize(size)
    return image


def from_wei(wei, precision=2):
    return round((int(wei) / 1000000000000000000), precision)
