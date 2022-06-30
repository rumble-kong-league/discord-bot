from PIL import Image
from util import Globals, Util, OpenSeaUtil


def replace_pixels(data, fromRGB, toRGB):
    new_data = []
    for item in data:
        if (
            abs(item[0] - int(fromRGB[0])) < 20
            and abs(item[1] - int(fromRGB[1])) < 20
            and abs(item[2] - int(fromRGB[2])) < 20
        ):
            new_data.append(tuple(toRGB))
        else:
            new_data.append(item)
    return new_data


def draw_naked_kong(kongId):
    params = {"token_ids": kongId, "collection_slug": "rumble-kong-league"}
    kong_assets = OpenSeaUtil.fetch_opensea_asset(Globals.OPENSEA_ASSETS_URL, params)[
        "assets"
    ][0]
    kong_traits = kong_assets["traits"]

    kong_base = {}
    for asset in kong_traits:
        if asset["trait_type"] == "Background":
            kong_base["Background"] = Globals.BACKGROUND_TO_RGBA[asset["value"]]
        elif asset["trait_type"] == "Fur":
            kong_base["Fur"] = Globals.NAKED_KONG_ID_BY_FUR[asset["value"]]
            background_color = Globals.NAKED_KONG_EXAMPLE_BACKGROUNDS[asset["value"]]

    params = {"token_ids": kong_base["Fur"], "collection_slug": "rumble-kong-league"}
    naked_kong_image_url = OpenSeaUtil.fetch_opensea_asset(
        Globals.OPENSEA_ASSETS_URL, params
    )["assets"][0]["image_url"]
    naked_kong_image = Util.fetch_image(naked_kong_image_url, (512, 512))

    replaced_background = replace_pixels(
        naked_kong_image.getdata(), background_color, kong_base["Background"]
    )
    naked_kong_image.putdata(replaced_background)

    cropped = naked_kong_image.crop((0, 360, 374, 512)).convert("RGBA")
    left_shoulder = naked_kong_image.crop((0, 310, 184, 385)).convert("RGBA")
    right_shoulder = naked_kong_image.crop((270, 354, 291, 368)).convert("RGBA")

    kong_image = Util.fetch_image(kong_assets["image_url"])
    kong_image.paste(cropped, (0, 360), mask=cropped)
    kong_image.paste(left_shoulder, (0, 310), mask=left_shoulder)
    kong_image.paste(right_shoulder, (270, 354), mask=right_shoulder)

    return kong_image


def apply_drip(kong_image, drip_type, isJersey=False):
    drip_image_url = Globals.DRIP_PATH + Globals.DRIP[drip_type]
    if isJersey == True:
        drip_image_url = Globals.JERSEYS_PATH + Globals.DRIP[drip_type]
    drip_image = Image.open(drip_image_url).resize((512, 512))
    kong_image.paste(drip_image, (0, 0), mask=drip_image)

    return kong_image
