from requests import get
from io import BytesIO
from PIL import Image
from datetime import datetime
from google.oauth2.service_account import Credentials
import json
from util import consts


def get_formatted_datetime(asPath=False):
    time = datetime.now()
    if asPath:
        return time.strftime("%d-%m-%Y_%H-%M-%S")
    return time.strftime("%d/%m/%Y %H:%M:%S")


def initialize_log():
    name = get_formatted_datetime(asPath=True) + ".txt"
    path = consts.LOG_PATH + name
    open(path, "w").close()
    consts.setLogFile(name)
    return path


def log(text, depth=0):
    msg = "[" + get_formatted_datetime() + "] " + ("--> " * depth) + text
    if consts.LOG:
        with open(consts.LOG_PATH + consts.LOG_FILE, "a") as f:
            f.write(msg + "\n")
    if consts.DEBUG:
        print(msg)


def read_json(path):
    data = ""
    with open(path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    return data


def write_json(path, data):
    text = json.dumps(data)
    with open(path, 'w+') as outfile:
        outfile.write(text)


def fetch_image(url, size=None):
    response = get(url)
    image = Image.open(BytesIO(response.content))
    if size:
        image.resize(size)
    return image


def from_wei(wei, precision=2):
    return round((int(wei) / 1000000000000000000), precision)


def read_service_account_credentials(path):
    return Credentials.from_service_account_file(
        path, 
        scopes=["https://www.googleapis.com/auth/spreadsheets"]
    )
