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
    kong_traits = kong_assets["traits"]

    kong_base = {}
    for asset in kong_traits:
        if asset["trait_type"] == "Background":
            kong_base["Background"] = consts.BACKGROUND_TO_RGBA[asset["value"]]
        elif asset["trait_type"] == "Fur":
            kong_base["Fur"] = consts.NAKED_KONG_ID_BY_FUR[asset["value"]]
            background_color = consts.NAKED_KONG_EXAMPLE_BACKGROUNDS[asset["value"]]

    params = {"token_ids": kong_base["Fur"], "collection_slug": "rumble-kong-league"}
    # ! remove the below
    # naked_kong_image_url = opensea.fetch_opensea_asset(
    #     consts.OPENSEA_ASSETS_URL, params
    # )["assets"][0]["image_url"]
    naked_kong_image_url = kong_assets["image_url"]
    naked_kong_image = util.fetch_image(naked_kong_image_url, (512, 512))

    replaced_background = replace_pixels(
        naked_kong_image.getdata().convert("RGBA"), background_color, kong_base["Background"]
    )
    naked_kong_image.putdata(replaced_background)

    kong_image = util.fetch_image(kong_assets["image_url"])

    return kong_image


def apply_drip(kong_image, drip_type, is_jersey=False):
    drip_image_url = ""

    if is_jersey == True:
        drip_image_url = os.path.join(consts.JERSEYS_PATH, consts.TEAMS[drip_type])
    else:
        if drip_type in consts.AVAILABLE_DRIPS:
            drip_image_url = os.path.join(consts.DRIP_PATH, consts.DRIP[drip_type])
        else:
            raise Exception("Drip not available")

    drip_image = Image.open(drip_image_url).resize((512, 512))
    kong_image = kong_image.convert("RGB")
    kong_image.paste(drip_image.convert("RGB"), (0, 0), mask=drip_image)

    return kong_image
