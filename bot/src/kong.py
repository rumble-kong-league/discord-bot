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
    params = {"token_ids": kong_id, "collection_slug": "rumble-kong-league"}
    kong_assets = opensea.fetch_opensea_asset(consts.OPENSEA_ASSETS_URL, params)[
        "assets"
    ][0]
    
    kong_image = util.fetch_image(kong_assets["image_url"], (512, 512))
    
    return kong_image


def apply_drip(kong_image, drip_type, is_jersey=False):
    drip_image_url = ""

    if is_jersey:
        drip_image_url = os.path.join(consts.JERSEYS_PATH, consts.TEAMS[drip_type])
    else:
        drip_image_url = os.path.join(consts.DRIP_PATH, consts.DRIP[drip_type])

    drip_image = Image.open(drip_image_url).resize((500, 500))
    kong_image = kong_image.convert("RGB")
    kong_image.paste(drip_image.convert("RGB"), (0, 0), mask=drip_image)

    return kong_image
