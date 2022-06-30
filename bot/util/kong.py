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


def draw_nakes_kong(kongId):
    params = {
        "token_ids": kongId,
        "collection_slug": "rumble-kong-league"
    }
    kongAssets = OpenSeaUtil.fetch_opensea_asset(Globals.OPENSEA_ASSETS_URL, params)["assets"][0]
    kongTraits = kongAssets["traits"]
    
    kongBase = {}
    for asset in kongTraits:
        if asset["trait_type"] == "Background":
            kongBase["Background"] = Globals.BACKGROUND_TO_RGBA[asset["value"]]
        elif asset["trait_type"] == "Fur":
            kongBase["Fur"] = Globals.NAKED_KONG_ID_BY_FUR[asset["value"]]
            backgroundColor = Globals.NAKED_KONG_EXAMPLE_BACKGROUNDS[asset["value"]]

    params = {
        "token_ids": kongBase["Fur"],
        "collection_slug": "rumble-kong-league"
    }
    nakedKongImageUrl = OpenSeaUtil.fetch_opensea_asset(Globals.OPENSEA_ASSETS_URL, params)["assets"][0]["image_url"]
    nakedKongImage = Util.fetch_image(nakedKongImageUrl, (512, 512))

    replacedBackground = replace_pixels(nakedKongImage.getdata(), backgroundColor, kongBase["Background"])
    nakedKongImage.putdata(replacedBackground)

    cropped = nakedKongImage.crop((0, 360, 374, 512)).convert("RGBA")
    leftShoulder = nakedKongImage.crop((0, 310, 184, 385)).convert("RGBA")
    rightShoulder = nakedKongImage.crop((270, 354, 291, 368)).convert("RGBA")

    kongImage = Util.fetch_image(kongAssets["image_url"])
    kongImage.paste(cropped, (0, 360), mask=cropped)
    kongImage.paste(leftShoulder, (0, 310), mask=leftShoulder)
    kongImage.paste(rightShoulder, (270, 354), mask=rightShoulder)

    return kongImage


def apply_drip(kongImage, dripType, isJersey=False):
    dripImageUrl = Globals.DRIP_PATH + Globals.DRIP[dripType]
    if isJersey == True:
        dripImageUrl = Globals.JERSEYS_PATH + Globals.DRIP[dripType]
    dripImage = Image.open(dripImageUrl).resize((512, 512))
    kongImage.paste(dripImage, (0, 0), mask=dripImage)

    return kongImage
