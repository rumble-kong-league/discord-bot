from PIL import Image
import os

import bot.src.consts as consts
import bot.src.opensea as opensea
import bot.src.util as util


def replace_pixels(data, from_rgb, to_rgb):
    new_data = []
    for item in data:
        if (
            abs(item[0] - int(from_rgb[0])) < 20
            and abs(item[1] - int(from_rgb[1])) < 20
            and abs(item[2] - int(from_rgb[2])) < 20
        ):
            new_data.append(tuple(to_rgb))
        else:
            new_data.append(item)
    return new_data


def draw_naked_kong(kong_id):
    kong_assets = opensea.fetch_opensea_asset(consts.KONGS_ETHEREUM_ADDRESS, kong_id)[
        "nft"
    ]

    kong_url = kong_assets["image_url"]
    if "pinata" in kong_url:
        kong_url = util.pinata2ipfs_url(kong_url)
        
    kong_image = util.fetch_image(kong_url, (512, 512))
    
    return kong_image


def apply_drip(kong_image, drip_type, is_jersey=False):
    drip_image_url = ""

    if is_jersey:
        drip_image_url = os.path.join(consts.JERSEYS_PATH, consts.TEAMS[drip_type])
    else:
        drip_image_url = os.path.join(consts.DRIP_PATH, consts.DRIP[drip_type])

    size = (500, 500)
    drip_image = Image.open(drip_image_url).resize(size)
    kong_image = kong_image.convert("RGB").resize(size)
    kong_image.paste(drip_image.convert("RGB"), (0, 0), mask=drip_image)

    return kong_image
