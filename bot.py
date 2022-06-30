# IMPORT DISCORD.PY. ALLOWS ACCESS TO DISCORD'S API.
import discord
import pandas as pd
import numpy as np

# IMPORT THE OS MODULE.
import os
from PIL import Image
import requests
from io import BytesIO
from googleapiclient.discovery import build
import boto3
from datetime import datetime

# IMPORT LOAD_DOTENV FUNCTION FROM DOTENV MODULE.
from dotenv import load_dotenv

# IMPORT COMMANDS FROM THE DISCORD.EXT MODULE.
from discord.ext import commands
from google.oauth2 import service_account

# LOADS THE .ENV FILE THAT RESIDES ON THE SAME LEVEL AS THE SCRIPT.
load_dotenv()

# GRAB THE API TOKEN FROM THE .ENV FILE.
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
KONG_URL = os.getenv("KONG_URL")
SNEAKER_URL = os.getenv("SNEAKER_URL")
DISCORD_GENERAL_CHANNEL_ID = int(os.getenv("DISCORD_GENERAL_CHANNEL_ID"))

SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]
SERVICE_ACCOUNT_FILE = "keys.json"
credentials = service_account.Credentials.from_service_account_file(
    SERVICE_ACCOUNT_FILE, scopes=SCOPES
)

s3 = boto3.client(
    "s3",
    aws_access_key_id="<aws_access_key_id>",
    aws_secret_access_key="<aws_secret_access_key>",
)


spreadsheet_id = "<spreadsheet_id>"
fur_colors = {
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

fur_background = {
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
    "Brown": [109, 173, 222],  # rgb(110, 172, 222)
}

background_color = {
    "Gold": (233, 168, 22, 1),
    "Light Blue": (109, 173, 222, 1),
    "Cyan": (75, 212, 205, 1),
    "Pink": (236, 110, 190, 1),
    "Dark Blue": (10, 79, 232, 1),
    "Purple": (116, 94, 218, 1),
    "Grey": (105, 110, 129, 1),
    "Red": (182, 10, 48, 1),
    "Brown": (155, 97, 80, 0),
    "Yellow": (254, 218, 94, 1),
    "Light Grey": (186, 193, 220, 1),  # rgb(110, 172, 222)
}
headers = {
    "X-API-KEY": "<opensea_api_key>",
    "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:47.0) Gecko/20100101 Firefox/47.0",
}


def get_kong_image_url(kong_id):
    url = (
        "https://api.opensea.io/api/v1/asset/0xef0182dc0574cd5874494a120750fd222fdb909a/"
        + str(kong_id)
    )
    response = requests.request("GET", url, headers=headers)
    return response.json()["image_url"]


def get_high_res_kong_url(kong_id):
    url = (
        "https://api.opensea.io/api/v1/asset/0xef0182dc0574cd5874494a120750fd222fdb909a/"
        + str(kong_id)
    )
    response = requests.request("GET", url, headers=headers)
    return response.json()["image_original_url"]


def get_naked_kong(kong_id):
    url = (
        "https://api.opensea.io/api/v1/asset/0xef0182dc0574cd5874494a120750fd222fdb909a/"
        + str(kong_id)
    )
    response = requests.request("GET", url, headers=headers)
    traits = response.json()["traits"]
    fur = ""
    kong_background_color = ""
    for dic in traits:
        for key in dic:
            if dic["trait_type"] == "Fur":
                fur = dic["value"]
            if dic["trait_type"] == "Background":
                kong_background_color = dic["value"]
    naked_kong_url = get_kong_image_url(fur_colors[fur])
    background = fur_background[fur]

    response = requests.get(naked_kong_url)
    naked_kong = Image.open(BytesIO(response.content))
    naked_kong.resize((512, 512))

    datas = naked_kong.getdata()

    new_data = []
    for item in datas:
        if (
            abs(item[0] - background[0]) < 20
            and abs(item[1] - background[1]) < 20
            and abs(item[2] - background[2]) < 20
        ):
            new_data.append(background_color[kong_background_color])
        else:
            new_data.append(item)

    naked_kong.putdata(new_data)

    if fur in ("Hyper Cat", "Zebra"):
        im_crop = naked_kong.crop((0, 360, 374, 512))
        im_crop = im_crop.convert("RGBA")

        left_shoulder = naked_kong.crop((0, 310, 184, 385))
        left_shoulder = left_shoulder.convert("RGBA")
        right_shoulder = naked_kong.crop((270, 354, 291, 368))
        right_shoulder = right_shoulder.convert("RGBA")
        kong_url = get_kong_image_url(kong_id)
        response = requests.get(kong_url)
        kong = Image.open(BytesIO(response.content))
        r, g, b = kong.getpixel((1, 1))

        kong.paste(im_crop, (0, 360), mask=im_crop)
        kong.paste(left_shoulder, (0, 310), mask=left_shoulder)
        kong.paste(right_shoulder, (270, 354), mask=right_shoulder)

    else:
        im_crop = naked_kong.crop((0, 360, 374, 512))
        im_crop = im_crop.convert("RGBA")

        left_shoulder = naked_kong.crop((0, 310, 184, 385))
        left_shoulder = left_shoulder.convert("RGBA")
        right_shoulder = naked_kong.crop((270, 354, 291, 368))
        right_shoulder = right_shoulder.convert("RGBA")
        kong_url = get_kong_image_url(kong_id)
        response = requests.get(kong_url)
        kong = Image.open(BytesIO(response.content))
        r, g, b = kong.getpixel((1, 1))

        kong.paste(im_crop, (0, 360), mask=im_crop)
        kong.paste(left_shoulder, (0, 310), mask=left_shoulder)
        kong.paste(right_shoulder, (270, 354), mask=right_shoulder)
    return kong


# CREATES A NEW BOT OBJECT WITH A SPECIFIED PREFIX. IT CAN BE WHATEVER YOU WANT IT TO BE.
bot = commands.Bot(command_prefix="!", case_insensitive=True)


# COMMAND !floor.
@bot.command(
    help="Sends back the current floor for RKL Kongs or Sneakers.",
    brief="Sends back the current floor for RKL Kongs or Sneakers.",
)
async def floor(ctx, *args):
    # print(type(DISCORD_GENERAL_CHANNEL_ID))
    # print(type(ctx.channel.id))
    if 873956958485491772 != ctx.channel.id:
        await ctx.channel.send("Please check the floor in <#873956958485491772>")
    else:
        read_file = s3.get_object(Bucket="kongtracker", Key="konglistings.csv")
        data = pd.read_csv(read_file["Body"], sep=",")
        if len(args) < 1:
            await ctx.channel.send(
                "It seems like there was a mistake, the current commands are \n`!floor kongs` - Returning floor prices for boosts from 180-250 \n`!floor sneakers` - Returning floor prices for all models of RKL sneakers \n`!floor kongs [[overall boost]]` - Returning the floor Kong listing at the given boost"
            )
        if args[0] == "kongs":
            if len(args) > 1:

                # I assume Naz is reading this, Hi Naz! I'll probably make a list and iterate over it for the floors that matter, Hi RKL Team

                embed = discord.Embed(
                    title=args[1]
                    + " Floor: "
                    + str(data[data.Cumulative >= int(args[1])]["listing_price"].min())
                    + "Ξ",
                    url=data.loc[
                        data[data.Cumulative >= int(args[1])]["listing_price"].idxmin(),
                        "opensea_url",
                    ]
                    + "?ref=0x05A2f7F467CefE9D67c95d9Ca3ff82870FCb0042",
                    description="There can be up to a 10 minute delay",
                    color=discord.Color.blue(),
                )
                embed.set_thumbnail(
                    url=data.loc[
                        data[data.Cumulative >= int(args[1])]["listing_price"].idxmin(),
                        "image_url",
                    ]
                )
                # embed.add_field(name="Overall", value=data.loc[data[data.Cumulative >= int(args[1])]['listing_price'].idxmin(), "Cumulative"], inline=True)
                embed.add_field(
                    name="Shooting",
                    value=data.loc[
                        data[data.Cumulative >= int(args[1])]["listing_price"].idxmin(),
                        "Shooting",
                    ],
                    inline=True,
                )
                embed.add_field(
                    name="Finish",
                    value=data.loc[
                        data[data.Cumulative >= int(args[1])]["listing_price"].idxmin(),
                        "Finish",
                    ],
                    inline=True,
                )
                embed.add_field(
                    name="Defense",
                    value=data.loc[
                        data[data.Cumulative >= int(args[1])]["listing_price"].idxmin(),
                        "Defense",
                    ],
                    inline=True,
                )
                embed.add_field(
                    name="Vision",
                    value=data.loc[
                        data[data.Cumulative >= int(args[1])]["listing_price"].idxmin(),
                        "Vision",
                    ],
                    inline=True,
                )
                await ctx.channel.send(embed=embed)
            else:
                embed = discord.Embed(
                    title="Global Floor: " + str(data["listing_price"].min()) + "Ξ",
                    url="https://opensea.io/collection/rumble-kong-league?collectionSlug=rumble-kong-league&search[sortAscending]=true&search[sortBy]=PRICE&search[toggles][0]=BUY_NOW",
                    description="There can be up to a 10 minute delay",
                    color=discord.Color.blue(),
                )

                embed.add_field(
                    name="180+ Floor: "
                    + str(data[data.Cumulative >= 180]["listing_price"].min())
                    + "Ξ",
                    value="[OpenSea Link]"
                    + "("
                    + data.loc[
                        data[data.Cumulative >= 180]["listing_price"].idxmin(),
                        "opensea_url",
                    ]
                    + "?ref=0x05A2f7F467CefE9D67c95d9Ca3ff82870FCb0042"
                    + ")",
                    inline=False,
                )
                embed.add_field(
                    name="190+ Floor: "
                    + str(data[data.Cumulative >= 190]["listing_price"].min())
                    + "Ξ",
                    value="[OpenSea Link]"
                    + "("
                    + data.loc[
                        data[data.Cumulative >= 190]["listing_price"].idxmin(),
                        "opensea_url",
                    ]
                    + "?ref=0x05A2f7F467CefE9D67c95d9Ca3ff82870FCb0042"
                    + ")",
                    inline=False,
                )
                embed.add_field(
                    name="200+ Floor: "
                    + str(data[data.Cumulative >= 200]["listing_price"].min())
                    + "Ξ",
                    value="[OpenSea Link]"
                    + "("
                    + data.loc[
                        data[data.Cumulative >= 200]["listing_price"].idxmin(),
                        "opensea_url",
                    ]
                    + "?ref=0x05A2f7F467CefE9D67c95d9Ca3ff82870FCb0042"
                    + ")",
                    inline=False,
                )
                embed.add_field(
                    name="210+ Floor: "
                    + str(data[data.Cumulative >= 210]["listing_price"].min())
                    + "Ξ",
                    value="[OpenSea Link]"
                    + "("
                    + data.loc[
                        data[data.Cumulative >= 210]["listing_price"].idxmin(),
                        "opensea_url",
                    ]
                    + "?ref=0x05A2f7F467CefE9D67c95d9Ca3ff82870FCb0042"
                    + ")",
                    inline=False,
                )
                embed.add_field(
                    name="220+ Floor: "
                    + str(data[data.Cumulative >= 220]["listing_price"].min())
                    + "Ξ",
                    value="[OpenSea Link]"
                    + "("
                    + data.loc[
                        data[data.Cumulative >= 220]["listing_price"].idxmin(),
                        "opensea_url",
                    ]
                    + "?ref=0x05A2f7F467CefE9D67c95d9Ca3ff82870FCb0042"
                    + ")",
                    inline=False,
                )
                embed.add_field(
                    name="230+ Floor: "
                    + str(data[data.Cumulative >= 230]["listing_price"].min())
                    + "Ξ",
                    value="[OpenSea Link]"
                    + "("
                    + data.loc[
                        data[data.Cumulative >= 230]["listing_price"].idxmin(),
                        "opensea_url",
                    ]
                    + "?ref=0x05A2f7F467CefE9D67c95d9Ca3ff82870FCb0042"
                    + ")",
                    inline=False,
                )
                embed.add_field(
                    name="240+ Floor: "
                    + str(data[data.Cumulative >= 240]["listing_price"].min())
                    + "Ξ",
                    value="[OpenSea Link]"
                    + "("
                    + data.loc[
                        data[data.Cumulative >= 240]["listing_price"].idxmin(),
                        "opensea_url",
                    ]
                    + "?ref=0x05A2f7F467CefE9D67c95d9Ca3ff82870FCb0042"
                    + ")",
                    inline=False,
                )
                embed.add_field(
                    name="250+ Floor: "
                    + str(data[data.Cumulative >= 250]["listing_price"].min())
                    + "Ξ",
                    value="[OpenSea Link]"
                    + "("
                    + data.loc[
                        data[data.Cumulative >= 250]["listing_price"].idxmin(),
                        "opensea_url",
                    ]
                    + "?ref=0x05A2f7F467CefE9D67c95d9Ca3ff82870FCb0042"
                    + ")",
                    inline=False,
                )
                embed.add_field(
                    name="Rare Furs Floor: "
                    + str(data[data.rarity_rank <= 250]["listing_price"].min())
                    + "Ξ",
                    value="[OpenSea Link]"
                    + "("
                    + data.loc[
                        data[data.rarity_rank <= 250]["listing_price"].idxmin(),
                        "opensea_url",
                    ]
                    + "?ref=0x05A2f7F467CefE9D67c95d9Ca3ff82870FCb0042"
                    + ")",
                    inline=False,
                )
                # SENDS A MESSAGE TO THE CHANNEL USING THE CONTEXT OBJECT.
                await ctx.channel.send(embed=embed)

        elif args[0] == "sneakers":
            data = pd.read_csv(SNEAKER_URL)

            embed = discord.Embed(
                title="Global Floor: " + str(data["listing_price"].min()) + "Ξ",
                url="https://opensea.io/collection/rumble-kong-league-sneakers",
                description="There can be up to a 10 minute delay",
                color=discord.Color.blue(),
            )

            embed.add_field(
                name="Kamo II: "
                + str(data[data.sneaker_type == "Kamo II"]["listing_price"].min())
                + "Ξ",
                value="[OpenSea Link]"
                + "("
                + data.loc[
                    data[data.sneaker_type == "Kamo II"]["listing_price"].idxmin(),
                    "opensea_url",
                ]
                + "?ref=0x05A2f7F467CefE9D67c95d9Ca3ff82870FCb0042"
                + ")",
                inline=True,
            )
            embed.add_field(
                name="Aurora II: "
                + str(data[data.sneaker_type == "Aurora II"]["listing_price"].min())
                + "Ξ",
                value="[OpenSea Link]"
                + "("
                + data.loc[
                    data[data.sneaker_type == "Aurora II"]["listing_price"].idxmin(),
                    "opensea_url",
                ]
                + "?ref=0x05A2f7F467CefE9D67c95d9Ca3ff82870FCb0042"
                + ")",
                inline=True,
            )
            embed.add_field(
                name="Lilac: "
                + str(data[data.sneaker_type == "Lilac"]["listing_price"].min())
                + "Ξ",
                value="[OpenSea Link]"
                + "("
                + data.loc[
                    data[data.sneaker_type == "Lilac"]["listing_price"].idxmin(),
                    "opensea_url",
                ]
                + "?ref=0x05A2f7F467CefE9D67c95d9Ca3ff82870FCb0042"
                + ")",
                inline=True,
            )
            embed.add_field(
                name="Rose: "
                + str(data[data.sneaker_type == "Rose"]["listing_price"].min())
                + "Ξ",
                value="[OpenSea Link]"
                + "("
                + data.loc[
                    data[data.sneaker_type == "Rose"]["listing_price"].idxmin(),
                    "opensea_url",
                ]
                + "?ref=0x05A2f7F467CefE9D67c95d9Ca3ff82870FCb0042"
                + ")",
                inline=True,
            )
            embed.add_field(
                name="Snow: "
                + str(data[data.sneaker_type == "Snow"]["listing_price"].min())
                + "Ξ",
                value="[OpenSea Link]"
                + "("
                + data.loc[
                    data[data.sneaker_type == "Snow"]["listing_price"].idxmin(),
                    "opensea_url",
                ]
                + "?ref=0x05A2f7F467CefE9D67c95d9Ca3ff82870FCb0042"
                + ")",
                inline=True,
            )
            embed.add_field(
                name="Kamo: "
                + str(data[data.sneaker_type == "Kamo"]["listing_price"].min())
                + "Ξ",
                value="[OpenSea Link]"
                + "("
                + data.loc[
                    data[data.sneaker_type == "Kamo"]["listing_price"].idxmin(),
                    "opensea_url",
                ]
                + "?ref=0x05A2f7F467CefE9D67c95d9Ca3ff82870FCb0042"
                + ")",
                inline=True,
            )
            embed.add_field(
                name="Grey: "
                + str(data[data.sneaker_type == "Grey"]["listing_price"].min())
                + "Ξ",
                value="[OpenSea Link]"
                + "("
                + data.loc[
                    data[data.sneaker_type == "Grey"]["listing_price"].idxmin(),
                    "opensea_url",
                ]
                + "?ref=0x05A2f7F467CefE9D67c95d9Ca3ff82870FCb0042"
                + ")",
                inline=True,
            )
            embed.add_field(
                name="Noise: "
                + str(data[data.sneaker_type == "Noise"]["listing_price"].min())
                + "Ξ",
                value="[OpenSea Link]"
                + "("
                + data.loc[
                    data[data.sneaker_type == "Noise"]["listing_price"].idxmin(),
                    "opensea_url",
                ]
                + "?ref=0x05A2f7F467CefE9D67c95d9Ca3ff82870FCb0042"
                + ")",
                inline=True,
            )
            embed.add_field(
                name="Sky: "
                + str(data[data.sneaker_type == "Sky"]["listing_price"].min())
                + "Ξ",
                value="[OpenSea Link]"
                + "("
                + data.loc[
                    data[data.sneaker_type == "Sky"]["listing_price"].idxmin(),
                    "opensea_url",
                ]
                + "?ref=0x05A2f7F467CefE9D67c95d9Ca3ff82870FCb0042"
                + ")",
                inline=True,
            )
            embed.add_field(
                name="Jungle: "
                + str(data[data.sneaker_type == "Jungle"]["listing_price"].min())
                + "Ξ",
                value="[OpenSea Link]"
                + "("
                + data.loc[
                    data[data.sneaker_type == "Jungle"]["listing_price"].idxmin(),
                    "opensea_url",
                ]
                + "?ref=0x05A2f7F467CefE9D67c95d9Ca3ff82870FCb0042"
                + ")",
                inline=True,
            )
            embed.add_field(
                name="Kat II: "
                + str(data[data.sneaker_type == "Kat II"]["listing_price"].min())
                + "Ξ",
                value="[OpenSea Link]"
                + "("
                + data.loc[
                    data[data.sneaker_type == "Kat II"]["listing_price"].idxmin(),
                    "opensea_url",
                ]
                + "?ref=0x05A2f7F467CefE9D67c95d9Ca3ff82870FCb0042"
                + ")",
                inline=True,
            )
            embed.add_field(
                name="REKD: "
                + str(data[data.sneaker_type == "Kat II"]["listing_price"].min())
                + "Ξ",
                value="[OpenSea Link]"
                + "("
                + data.loc[
                    data[data.sneaker_type == "REKD"]["listing_price"].idxmin(),
                    "opensea_url",
                ]
                + "?ref=0x05A2f7F467CefE9D67c95d9Ca3ff82870FCb0042"
                + ")",
                inline=True,
            )
            embed.add_field(
                name="Snow Gold: "
                + str(data[data.sneaker_type == "Kat II"]["listing_price"].min())
                + "Ξ",
                value="[OpenSea Link]"
                + "("
                + data.loc[
                    data[data.sneaker_type == "Snow Gold"]["listing_price"].idxmin(),
                    "opensea_url",
                ]
                + "?ref=0x05A2f7F467CefE9D67c95d9Ca3ff82870FCb0042"
                + ")",
                inline=True,
            )
            embed.add_field(
                name="Kat: "
                + str(data[data.sneaker_type == "Kat II"]["listing_price"].min())
                + "Ξ",
                value="[OpenSea Link]"
                + "("
                + data.loc[
                    data[data.sneaker_type == "Kat"]["listing_price"].idxmin(),
                    "opensea_url",
                ]
                + "?ref=0x05A2f7F467CefE9D67c95d9Ca3ff82870FCb0042"
                + ")",
                inline=True,
            )
            embed.add_field(
                name="Aurora: "
                + str(data[data.sneaker_type == "Aurora"]["listing_price"].min())
                + "Ξ",
                value="[OpenSea Link]"
                + "("
                + data.loc[
                    data[data.sneaker_type == "Aurora"]["listing_price"].idxmin(),
                    "opensea_url",
                ]
                + "?ref=0x05A2f7F467CefE9D67c95d9Ca3ff82870FCb0042"
                + ")",
                inline=True,
            )
            embed.add_field(
                name="Gold: "
                + str(data[data.sneaker_type == "Gold"]["listing_price"].min())
                + "Ξ",
                value="[OpenSea Link]"
                + "("
                + data.loc[
                    data[data.sneaker_type == "Gold"]["listing_price"].idxmin(),
                    "opensea_url",
                ]
                + "?ref=0x05A2f7F467CefE9D67c95d9Ca3ff82870FCb0042"
                + ")",
                inline=True,
            )
            embed.add_field(
                name="Krystal: "
                + str(data[data.sneaker_type == "Krystal"]["listing_price"].min())
                + "Ξ",
                value="[OpenSea Link]"
                + "("
                + data.loc[
                    data[data.sneaker_type == "Krystal"]["listing_price"].idxmin(),
                    "opensea_url",
                ]
                + "?ref=0x05A2f7F467CefE9D67c95d9Ca3ff82870FCb0042"
                + ")",
                inline=True,
            )

            # SENDS A MESSAGE TO THE CHANNEL USING THE CONTEXT OBJECT.
            await ctx.channel.send(embed=embed)
        else:
            await ctx.channel.send(
                "It seems like there was a mistake, the current commands are \n`!floor kongs` - Returning floor prices for boosts from 180-250 \n`!floor sneakers` - Returning Floor prices for all models of RKL sneakers \n`!floor kongs [[overall boost]]` - Returning the floor Kong listing at the given boost"
            )


# COMMAND !creator.
@bot.command(
    # ADDS THIS VALUE TO THE !creator PRINT MESSAGE.
    help="Checks if you are my creator.",
    # ADDS THIS VALUE TO THE !creator MESSAGE.
    brief="Checks if you are my creator.",
)
async def creator(ctx, *args):
    response = ""
    username = ctx.message.author.id
    if username == 374326261608087553:
        await ctx.channel.send("you are my creator, thanks for making me")
    else:
        await ctx.channel.send("imposter! KongTracker made this")


# COMMAND !creator.
@bot.command(
    # ADDS THIS VALUE TO THE !creator PRINT MESSAGE.
    help="I AM KONG",
    # ADDS THIS VALUE TO THE !creator MESSAGE.
    brief="I AM KONG, an initiative by ethwave.eth ",
)
async def iamkong(ctx, *args):
    await ctx.channel.send(file=discord.File("iamkong_compressed.gif"))


# EXECUTES THE BOT WITH THE SPECIFIED TOKEN. TOKEN HAS BEEN REMOVED AND USED JUST AS AN EXAMPLE.


# COMMAND !creator.
@bot.command(
    # ADDS THIS VALUE TO THE !creator PRINT MESSAGE.
    help="Praise Naz",
    # ADDS THIS VALUE TO THE !creator MESSAGE.
    brief="Praise Naz, an initiative by Aron ",
)
async def naztynaz(ctx, *args):
    await ctx.channel.send(file=discord.File("naztynaz.gif"))


# EXECUTES THE BOT WITH THE SPECIFIED TOKEN. TOKEN HAS BEEN REMOVED AND USED JUST AS AN EXAMPLE.

# COMMAND !creator.
@bot.command(
    # ADDS THIS VALUE TO THE !creator PRINT MESSAGE.
    help="Praise Naz",
    # ADDS THIS VALUE TO THE !creator MESSAGE.
    brief="Praise Naz, an initiative by Aron ",
)
async def nazty(ctx, *args):
    await ctx.channel.send(file=discord.File("naztynaz.gif"))


# EXECUTES THE BOT WITH THE SPECIFIED TOKEN. TOKEN HAS BEEN REMOVED AND USED JUST AS AN EXAMPLE.

# COMMAND !naz.
@bot.command(
    # ADDS THIS VALUE TO THE !naz PRINT MESSAGE.
    help="Praise Naz",
    # ADDS THIS VALUE TO THE !naz MESSAGE.
    brief="Praise Naz, an initiative by Aron ",
)
async def naz(ctx, *args):
    await ctx.channel.send(file=discord.File("naztynaz.gif"))


# EXECUTES THE BOT WITH THE SPECIFIED TOKEN. TOKEN HAS BEEN REMOVED AND USED JUST AS AN EXAMPLE.

# COMMAND !naz.
@bot.command(
    # ADDS THIS VALUE TO THE !naz PRINT MESSAGE.
    help="Praise Nickev",
    # ADDS THIS VALUE TO THE !naz MESSAGE.
    brief="Praise Nickev, an initiative by Aron ",
)
async def nickev(ctx, *args):
    await ctx.channel.send(file=discord.File("nickev.gif"))


# EXECUTES THE BOT WITH THE SPECIFIED TOKEN. TOKEN HAS BEEN REMOVED AND USED JUST AS AN EXAMPLE.


# COMMAND !naz.
@bot.command(
    # ADDS THIS VALUE TO THE !naz PRINT MESSAGE.
    help="Praise Direkkt",
    # ADDS THIS VALUE TO THE !naz MESSAGE.
    brief="Praise Direkkt, an initiative by Aron ",
)
async def direkkt(ctx, *args):
    await ctx.channel.send(file=discord.File("direkkt.gif"))


# EXECUTES THE BOT WITH THE SPECIFIED TOKEN. TOKEN HAS BEEN REMOVED AND USED JUST AS AN EXAMPLE.

# COMMAND !naz.
@bot.command(
    # ADDS THIS VALUE TO THE !naz PRINT MESSAGE.
    help="Praise sickpencil",
    # ADDS THIS VALUE TO THE !naz MESSAGE.
    brief="Praise sickpencil, an initiative by Aron ",
)
async def sickpencil(ctx, *args):
    await ctx.channel.send(file=discord.File("goodpencil.gif"))


# EXECUTES THE BOT WITH THE SPECIFIED TOKEN. TOKEN HAS BEEN REMOVED AND USED JUST AS AN EXAMPLE.

# COMMAND !naz.
@bot.command(
    # ADDS THIS VALUE TO THE !naz PRINT MESSAGE.
    help="Praise sickpencil",
    # ADDS THIS VALUE TO THE !naz MESSAGE.
    brief="Praise sickpencil, an initiative by Aron ",
)
async def goodpencil(ctx, *args):
    await ctx.channel.send(file=discord.File("goodpencil.gif"))


# EXECUTES THE BOT WITH THE SPECIFIED TOKEN. TOKEN HAS BEEN REMOVED AND USED JUST AS AN EXAMPLE.


# COMMAND !naz.
@bot.command(
    # ADDS THIS VALUE TO THE !naz PRINT MESSAGE.
    help="Praise KongTracker",
    # ADDS THIS VALUE TO THE !naz MESSAGE.
    brief="Praise KongTracker, an initiative by Aron ",
)
async def kongtracker(ctx, *args):
    await ctx.channel.send(file=discord.File("kongtracker.gif"))


# EXECUTES THE BOT WITH THE SPECIFIED TOKEN. TOKEN HAS BEEN REMOVED AND USED JUST AS AN EXAMPLE.


# COMMAND !naz.
@bot.command(
    # ADDS THIS VALUE TO THE !naz PRINT MESSAGE.
    help="Praise RKL Team",
    # ADDS THIS VALUE TO THE !naz MESSAGE.
    brief="Praise RKL Team",
)
async def team(ctx, *args):
    await ctx.channel.send(file=discord.File("team.gif"))


# EXECUTES THE BOT WITH THE SPECIFIED TOKEN. TOKEN HAS BEEN REMOVED AND USED JUST AS AN EXAMPLE.


# COMMAND !naz.
@bot.command(
    # ADDS THIS VALUE TO THE !naz PRINT MESSAGE.
    help="Praise Steph",
    # ADDS THIS VALUE TO THE !naz MESSAGE.
    brief="Praise Steph",
)
async def steph(ctx, *args):
    await ctx.channel.send(file=discord.File("steph.gif"))


# EXECUTES THE BOT WITH THE SPECIFIED TOKEN. TOKEN HAS BEEN REMOVED AND USED JUST AS AN EXAMPLE.


# COMMAND !naz.
@bot.command(
    # ADDS THIS VALUE TO THE !naz PRINT MESSAGE.
    help="Yes",
    # ADDS THIS VALUE TO THE !naz MESSAGE.
    brief="Yes",
)
async def yes(ctx, *args):
    await ctx.channel.send(file=discord.File("yes.png"))


# EXECUTES THE BOT WITH THE SPECIFIED TOKEN. TOKEN HAS BEEN REMOVED AND USED JUST AS AN EXAMPLE.


# COMMAND !floor.
@bot.command(help="Add merch to your Kong.", brief="Add merch to your Kong.")
async def drip(ctx, *args):
    if 914693919088992296 != ctx.channel.id:
        await ctx.channel.send("Please use this feature in <#914693919088992296>")
    else:
        if len(args) < 1:
            await ctx.channel.send(
                "It seems like there was a mistake, the current commands are \n`!drip [[kong id]] hoodie` - Returning your kong in a hoodie \n`!drip [[kong id]] virgil` - Returning your kong in the virgil abloh t-shirt"
            )

        kong = get_naked_kong(args[0])  # get_kong_image_url(args[0])
        # response = requests.get(kong_url)
        # kong = Image.open(BytesIO(response.content))

        if args[1] == "hoodie":
            if len(args) > 1:
                hoodie = Image.open(r"hoodie.png")
                hoodie = hoodie.resize((512, 512))
                kong.paste(hoodie, (0, 0), mask=hoodie)
                kong.save("kong_hoodie.png")
                kong.close()
                hoodie.close()
                await ctx.send(file=discord.File("kong_hoodie.png"))
        if args[1] == "virgil":
            if len(args) > 1:
                hoodie = Image.open(r"virgil_teeshirt.png")
                hoodie = hoodie.resize((512, 512))
                kong.paste(hoodie, (0, 0), mask=hoodie)
                kong.save("kong_hoodie.png")
                kong.close()
                hoodie.close()
                await ctx.send(file=discord.File("kong_hoodie.png"))
        if args[1] == "pinksuit":
            if len(args) > 1:
                hoodie = Image.open(r"pinksuit.png")
                hoodie = hoodie.resize((512, 512))
                kong.paste(hoodie, (0, 0), mask=hoodie)
                kong.save("kong_hoodie.png")
                kong.close()
                hoodie.close()
                await ctx.send(file=discord.File("kong_hoodie.png"))


# COMMAND !floor.
@bot.command(help="Add jersey to your Kong.", brief="Add jersey to your Kong.")
async def jersey(ctx, *args):
    if 914693919088992296 != ctx.channel.id:
        await ctx.channel.send("Please use this feature in <#914693919088992296>")
    else:
        if len(args) < 1:
            await ctx.channel.send(
                "It seems like there was a mistake, the current commands are \n`!drip [[kong id]] hoodie` - Returning your kong in a hoodie \n`!drip [[kong id]] virgil` - Returning your kong in the virgil abloh t-shirt"
            )

        kong = get_naked_kong(args[0])  # get_kong_image_url(args[0])
        # response = requests.get(kong_url)
        # kong = Image.open(BytesIO(response.content))

        if args[1] == "gulag":
            if len(args) > 1:
                hoodie = Image.open(r"assets/gulag.png")
                hoodie = hoodie.resize((512, 512))
                kong.paste(hoodie, (0, 0), mask=hoodie)
                kong.save("kong_hoodie.png")
                kong.close()
                hoodie.close()
                await ctx.send(file=discord.File("kong_hoodie.png"))
        if args[1] == "kongsota":
            if len(args) > 1:
                hoodie = Image.open(r"assets/kongsota.png")
                hoodie = hoodie.resize((512, 512))
                kong.paste(hoodie, (0, 0), mask=hoodie)
                kong.save("kong_hoodie.png")
                kong.close()
                hoodie.close()
                await ctx.send(file=discord.File("kong_hoodie.png"))
        if args[1] == "100club":
            if len(args) > 1:
                hoodie = Image.open(r"assets/100club.png")
                hoodie = hoodie.resize((512, 512))
                kong.paste(hoodie, (0, 0), mask=hoodie)
                kong.save("kong_hoodie.png")
                kong.close()
                hoodie.close()
                await ctx.send(file=discord.File("kong_hoodie.png"))
        if args[1] == "swagz":
            if len(args) > 1:
                hoodie = Image.open(r"assets/swagz.png")
                hoodie = hoodie.resize((512, 512))
                kong.paste(hoodie, (0, 0), mask=hoodie)
                kong.save("kong_hoodie.png")
                kong.close()
                hoodie.close()
                await ctx.send(file=discord.File("kong_hoodie.png"))
        if args[1] == "superkongs":
            if len(args) > 1:
                hoodie = Image.open(r"assets/superkongs.png")
                hoodie = hoodie.resize((512, 512))
                kong.paste(hoodie, (0, 0), mask=hoodie)
                kong.save("kong_hoodie.png")
                kong.close()
                hoodie.close()
                await ctx.send(file=discord.File("kong_hoodie.png"))
        if args[1] == "coastal":
            if len(args) > 1:
                hoodie = Image.open(r"assets/coastal.png")
                hoodie = hoodie.resize((512, 512))
                kong.paste(hoodie, (0, 0), mask=hoodie)
                kong.save("kong_hoodie.png")
                kong.close()
                hoodie.close()
                await ctx.send(file=discord.File("kong_hoodie.png"))
        if args[1] == "kongshow":
            if len(args) > 1:
                hoodie = Image.open(r"assets/kongshow.png")
                hoodie = hoodie.resize((512, 512))
                kong.paste(hoodie, (0, 0), mask=hoodie)
                kong.save("kong_hoodie.png")
                kong.close()
                hoodie.close()
                await ctx.send(file=discord.File("kong_hoodie.png"))
        if args[1] == "kamikazes":
            if len(args) > 1:
                hoodie = Image.open(r"assets/kamikazes.png")
                hoodie = hoodie.resize((512, 512))
                kong.paste(hoodie, (0, 0), mask=hoodie)
                kong.save("kong_hoodie.png")
                kong.close()
                hoodie.close()
                await ctx.send(file=discord.File("kong_hoodie.png"))
        if args[1] == "versace":
            if len(args) > 1:
                hoodie = Image.open(r"assets/versace.png")
                hoodie = hoodie.resize((512, 512))
                kong.paste(hoodie, (0, 0), mask=hoodie)
                kong.save("kong_hoodie.png")
                kong.close()
                hoodie.close()
                await ctx.send(file=discord.File("kong_hoodie.png"))
        if args[1] == "sac":
            if len(args) > 1:
                hoodie = Image.open(r"assets/sac.png")
                hoodie = hoodie.resize((512, 512))
                kong.paste(hoodie, (0, 0), mask=hoodie)
                kong.save("kong_hoodie.png")
                kong.close()
                hoodie.close()
                await ctx.send(file=discord.File("kong_hoodie.png"))
        if args[1] == "kongvictz":
            if len(args) > 1:
                hoodie = Image.open(r"assets/kongvictz.png")
                hoodie = hoodie.resize((512, 512))
                kong.paste(hoodie, (0, 0), mask=hoodie)
                kong.save("kong_hoodie.png")
                kong.close()
                hoodie.close()
                await ctx.send(file=discord.File("kong_hoodie.png"))
        if args[1] == "hooperz":
            if len(args) > 1:
                hoodie = Image.open(r"assets/hooperz.png")
                hoodie = hoodie.resize((512, 512))
                kong.paste(hoodie, (0, 0), mask=hoodie)
                kong.save("kong_hoodie.png")
                kong.close()
                hoodie.close()
                await ctx.send(file=discord.File("kong_hoodie.png"))
        if args[1] == "kongcrete":
            if len(args) > 1:
                hoodie = Image.open(r"assets/kongcrete.png")
                hoodie = hoodie.resize((512, 512))
                kong.paste(hoodie, (0, 0), mask=hoodie)
                kong.save("kong_hoodie.png")
                kong.close()
                hoodie.close()
                await ctx.send(file=discord.File("kong_hoodie.png"))
        if args[1] == "badboyz":
            if len(args) > 1:
                hoodie = Image.open(r"assets/badboyz.png")
                hoodie = hoodie.resize((512, 512))
                kong.paste(hoodie, (0, 0), mask=hoodie)
                kong.save("kong_hoodie.png")
                kong.close()
                hoodie.close()
                await ctx.send(file=discord.File("kong_hoodie.png"))
        if args[1] == "bushido":
            if len(args) > 1:
                hoodie = Image.open(r"assets/bushido.png")
                hoodie = hoodie.resize((512, 512))
                kong.paste(hoodie, (0, 0), mask=hoodie)
                kong.save("kong_hoodie.png")
                kong.close()
                hoodie.close()
                await ctx.send(file=discord.File("kong_hoodie.png"))
        if args[1] == "arkongsas":
            if len(args) > 1:
                hoodie = Image.open(r"assets/arkongsas.png")
                hoodie = hoodie.resize((512, 512))
                kong.paste(hoodie, (0, 0), mask=hoodie)
                kong.save("kong_hoodie.png")
                kong.close()
                hoodie.close()
                await ctx.send(file=discord.File("kong_hoodie.png"))
        if args[1] == "latinkong":
            if len(args) > 1:
                hoodie = Image.open(r"assets/latinkong.png")
                hoodie = hoodie.resize((512, 512))
                kong.paste(hoodie, (0, 0), mask=hoodie)
                kong.save("kong_hoodie.png")
                kong.close()
                hoodie.close()
                await ctx.send(file=discord.File("kong_hoodie.png"))
        if args[1] == "kings":
            if len(args) > 1:
                hoodie = Image.open(r"assets/kings.png")
                hoodie = hoodie.resize((512, 512))
                kong.paste(hoodie, (0, 0), mask=hoodie)
                kong.save("kong_hoodie.png")
                kong.close()
                hoodie.close()
                await ctx.send(file=discord.File("kong_hoodie.png"))
        if args[1] == "empire":
            if len(args) > 1:
                hoodie = Image.open(r"assets/empire.png")
                hoodie = hoodie.resize((512, 512))
                kong.paste(hoodie, (0, 0), mask=hoodie)
                kong.save("kong_hoodie.png")
                kong.close()
                hoodie.close()
                await ctx.send(file=discord.File("kong_hoodie.png"))
        if args[1] == "surfcity":
            if len(args) > 1:
                hoodie = Image.open(r"assets/surfcity.png")
                hoodie = hoodie.resize((512, 512))
                kong.paste(hoodie, (0, 0), mask=hoodie)
                kong.save("kong_hoodie.png")
                kong.close()
                hoodie.close()
                await ctx.send(file=discord.File("kong_hoodie.png"))


# COMMAND !floor.
@bot.command(
    help="Get Hi Res Image of your Kong", brief="Get Hi Res Image of your Kong"
)
async def image(ctx, *args):
    if 914693919088992296 != ctx.channel.id:
        await ctx.channel.send("Please use this feature in <#914693919088992296>")
    else:

        kong_url = get_high_res_kong_url(args[0])
        await ctx.channel.send("`" + str(kong_url) + "`")


# COMMAND !floor.
@bot.command(
    help="Vote for your favorite jersey", brief="Vote for your favorite jersey"
)
async def vote(ctx, *args):
    if 914693919088992296 != ctx.channel.id:
        await ctx.channel.send("Please use this feature in <#914693919088992296>")
    else:
        rows = [
            [
                ctx.message.author.name,
                ctx.message.author.id,
                ctx.message.content,
                datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
            ]
        ]
        service = build("sheets", "v4", credentials=credentials)
        service.spreadsheets().values().append(
            spreadsheetId=spreadsheet_id,
            range="Sheet1!A:Z",
            body={"majorDimension": "ROWS", "values": rows},
            valueInputOption="USER_ENTERED",
        ).execute()
        await ctx.channel.send("Your Vote has been logged")


bot.run(DISCORD_TOKEN)
