import os
from dotenv import load_dotenv

load_dotenv()


DEFAULT_REST_TIME = 180
DEFAULT_MAX_ATTEMPTS = 3

CACHE_UPDATE_RATE = 600

SRC_PATH = os.path.dirname(os.path.abspath(__file__)) # ../src
BOT_PATH = os.path.dirname(SRC_PATH)
LOG_PATH = BOT_PATH # ../bot
CACHE_PATH = os.path.join(BOT_PATH, "cache") # ../discord-bot/cache
ASSETS_PATH = os.path.join(BOT_PATH, "assets")
TMP_PATH = os.path.join(ASSETS_PATH, "tmp")
DRIP_PATH = os.path.join(ASSETS_PATH, "drip")
JERSEYS_PATH = os.path.join(DRIP_PATH, "jerseys")
MEMES_PATH = os.path.join(ASSETS_PATH, "memes")
STAFF_PATH = os.path.join(ASSETS_PATH, "staff")

DISCORD_TOKEN = os.environ["DISCORD_TOKEN"]
OPENSEA_API_KEY = os.environ["OPENSEA_API_KEY"]

OPENSEA_API_BASE_URL = "https://api.opensea.io/api/v1"
OPENSEA_ASSETS_URL = OPENSEA_API_BASE_URL + "/assets"
OPENSEA_EVENTS_URL = OPENSEA_API_BASE_URL + "/events"

STYLE_TRAIT_TYPES = ["Background", "Fur", "Clothes", "Mouth", "Eyes", "Head"]
BOOST_TRAIT_TYPES = ["Shooting", "Defense", "Vision", "Finish"]

AVAILABLE_DRIPS = [
    "overalls",
]

COLLECTIONS = {
    "kongs": {
        "verbose": "Rumble Kong League",
        "slug": "rumble-kong-league",
        "image": (
            "https://lh3.googleusercontent.com/"
            "x18rNFBg9leLL9TtHkhhiC8cwIurh1UhMKU6TL_"
            "JMbGyUsY8MTMhyPiz8Nz7VRJHShEgIQlCP070UB9"
            "gGWvJ05ST7IclovIWnwAUww=s120"
        ),
        "contract_address": "0xef0182dc0574cd5874494a120750fd222fdb909a",
    },
    "sneakers": {
        "verbose": "Rumble Kong League Sneakers",
        "slug": "rumble-kong-league-sneakers",
        "image": (
            "https://lh3.googleusercontent.com/"
            "dPsSX97-jVU9igM_6bGyIcL9A13kWBz5wlb-"
            "b76OuEiRX3H7dMVUHWA0-U7hFhYVr4R7eC0Zu"
            "9A75SbfEiaAOFl5Yo5V914BbIOX=s120"
        ),
        "contract_address": "0x5180f2a553e76fac3cf019c8011711cf2b5c6035",
    },
}

STAFF = {
    "team": "team.gif",
    "naztynaz": "nastynaz.gif",
    "nazty": "nastynaz.gif",
    "naz": "nastynaz.gif",
    "nickev": "nickev.gif",
    "nick": "nickev.gif",
    "direkkt": "direkkt.gif",
    "goodpencil": "goodpencil.gif",
    "sickpencil": "goodpencil.gif",
    "steph": "steph.gif",
    "vapour": "vapour.gif",
    "apeantics": "apeantics.gif",
    "jandc": "jandc.gif",
    "pizza": "pizza.gif"
}

# TODO: drip and teams dicts are useless. Just use the arg passed in the bot command
# TODO: and add .png to the end. If the file does not exist, just don't do anything
DRIP = {
    "hoodie": "hoodie.png",
    "virgil": "virgil.png",
    "pinksuit": "pinksuit.png",
    "blacksuit": "blacksuit.png",
    "usa": "usa.png",
    "boostgang": "boostgang.png",
    "denim": "denim.png",
    "overalls": "overalls.png",
    "princebattlesuit": "princebattlesuit.png",
    "r21rkl": "r21rkl.png",
    "raregang": "raregang.png",
    "sppuffer": "sppuffer.png",
    "suave": "suave.png",
    "spnyc": "spnyc.png",
    "pennyjar": "pennyjar.png"
}

TEAMS = {
    "gulag": "gulag.png",
    "kongsota": "kongsota.png",
    "100club": "100club.png",
    "superkongs": "superkongs.png",
    "coastal": "coastal.png",
    "kongshow": "kongshow.png",
    "kamikazes": "kamikazes.png",
    "versace": "versace.png",
    "sac": "sac.png",
    "swagz": "swagz.png",
    "kongvictz": "kongvictz.png",
    "hooperz": "hooperz.png",
    "badboyz": "badboyz.png",
    "bushido": "bushido.png",
    "arkongsas": "arkongsas.png",
    "latinkong": "latinkong.png",
    "kongcrete": "kongcrete.png",
    "kings": "kings.png",
    "empire": "empire.png",
    "surfcity": "surfcity.png",
}

BACKGROUND_TO_RGBA = {
    "Gold": [233, 168, 22, 1],
    "Light Blue": [109, 173, 222, 1],
    "Cyan": [75, 212, 205, 1],
    "Pink": [236, 110, 190, 1],
    "Dark Blue": [10, 79, 232, 1],
    "Purple": [116, 94, 218, 1],
    "Grey": [105, 110, 129, 1],
    "Red": [182, 10, 48, 1],
    "Brown": [155, 97, 80, 0],
    "Yellow": [254, 218, 94, 1],
    "Light Grey": [186, 193, 220, 1],
}

NAKED_KONG_ID_BY_FUR = {
    "Crystal": 1442,
    "Hyper Cat": 4004,
    "Zebra": 536,
    "Gold": 1275,
    "Camo": 1131,
    "Aurora": 1630,
    "Green": 989,
    "White Noise": 969,
    "Sky Blue": 298,
    "Red": 77,
    "Pink": 33,
    "Grey": 101,
    "Black": 167,
    "Brown": 44,
}

NAKED_KONG_EXAMPLE_BACKGROUNDS = {
    "Crystal": [254, 218, 94],
    "Hyper Cat": [186, 193, 220],
    "Zebra": [116, 94, 218],
    "Gold": [75, 212, 205],
    "Camo": [182, 10, 48],
    "Aurora": [116, 94, 218],
    "Green": [155, 97, 80],
    "White Noise": [75, 212, 205],
    "Sky Blue": [236, 110, 190],
    "Red": [116, 94, 218],
    "Pink": [186, 193, 220],
    "Grey": [186, 193, 220],
    "Black": [75, 212, 205],
    "Brown": [109, 173, 222],
}
