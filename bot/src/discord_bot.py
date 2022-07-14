import os
# from os.path import exists
import discord
from discord.ext import commands
from io import BytesIO
# from jokeapi import Jokes
# import time
# from random import randint
import json
# import base64
from typing import Tuple, List

import bot.src.consts as consts  # pylint: disable=import-error
# import bot.src.util as util
import bot.src.opensea as opensea  # pylint: disable=import-error
import bot.src.kong as kong_util  # pylint: disable=import-error



KONG_ASSET_OPENSEA_URL = (
    "https://opensea.io/assets/ethereum/0xef0182dc0574cd5874494a120750fd222fdb909a/"
)

ASSETS_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "assets")
KONGS_PATH = os.path.join(ASSETS_PATH, "kongs")
META_PATH = os.path.join(ASSETS_PATH, "meta.json")
META = json.loads(open(META_PATH).read())


def initialize_bot():
    bot = commands.Bot(command_prefix="$", case_insensitive=True)
    register_commands(bot)
    bot.run(consts.DISCORD_TOKEN)


async def send_image_binary(ctx, img):
    with BytesIO() as image_binary:
        img.save(image_binary, "PNG")
        image_binary.seek(0)
        await ctx.channel.send(file=discord.File(fp=image_binary, filename="tacpeo.png"))    


# Include chat commands within this function to ensure they are registered on startup
def register_commands(bot):

    @bot.command(help="Sweep those thin floors! fr fr", brief="Sweep those thin floors! fr fr")
    async def sweep(ctx, *_args):
        await ctx.channel.send(file=discord.File(os.path.join(consts.MEMES_PATH, "sweep.gif")))

    @bot.command(help="On your head!", brief="On your head!")
    async def oyh(ctx, *_args):
        await ctx.channel.send(file=discord.File(os.path.join(consts.MEMES_PATH, "oyh.gif")))

    @bot.command(help="Let's focking go!", brief="Let's focking go!")
    async def lfg(ctx, *_args):
        await ctx.channel.send(file=discord.File(os.path.join(consts.MEMES_PATH, "lfg.gif")))

    @bot.command(help="Looking for group!", brief="Looking for group!")
    async def lookingforgroup(ctx, *_args):
        await ctx.channel.send(file=discord.File(os.path.join(consts.MEMES_PATH, "lfg.gif")))

    @bot.command(help="Good Morning!", brief="Good Morning!")
    async def gm(ctx, *_args):
        await ctx.channel.send(file=discord.File(os.path.join(consts.MEMES_PATH, "gm.gif")))

    @bot.command(help="Good Night!", brief="Good Night!")
    async def gn(ctx, *_args):
        await ctx.channel.send(file=discord.File(os.path.join(consts.MEMES_PATH, "gn.gif")))

    @bot.command(help="There is no ceiling!", brief="There is no ceiling!")
    async def ceiling(ctx, *_args):
        await ctx.channel.send(file=discord.File(os.path.join(consts.MEMES_PATH, "ceiling.gif")))

    @bot.command(help="I am Kong!", brief="I am Kong!")
    async def iamkong(ctx, *_args):
        await ctx.channel.send(file=discord.File(os.path.join(consts.MEMES_PATH, "iamkong.gif")))

    @bot.command(help="Yes.", brief="Yes.")
    async def yes(ctx, *_args):
        await ctx.channel.send(file=discord.File(os.path.join(consts.MEMES_PATH, "yes.png")))

    @bot.command(help="Ready to Rumble.", brief="Ready to Rumble.")
    async def rumble(ctx, *_args):
        await ctx.channel.send(file=discord.File(os.path.join(consts.MEMES_PATH, "rumble.gif")))

    @bot.command(help="We are Kong.", brief="We are Kong.")
    async def wearekong(ctx, *_args):
        await ctx.channel.send(file=discord.File(os.path.join(consts.MEMES_PATH, "wearekong.gif")))

    @bot.command(help="Alpha alert.", brief="Alpha alert.")
    async def alpha(ctx, *_args):
        await ctx.channel.send(file=discord.File(os.path.join(consts.MEMES_PATH, "alpha.gif")))

    @bot.command(help="Tacpeo.", brief="Tacpeo.")
    async def tacpeo(ctx, *_args):
        await ctx.channel.send(file=discord.File(os.path.join(consts.MEMES_PATH, "tacpeo.gif")))

    @bot.command(
        help="$praise <team member name>",
        brief="Give thanks to the RKL team members.",
    )
    async def praise(ctx, *args):
        name = str(args[0]).lower()
        if name not in consts.STAFF:
            name = "team"
        await ctx.channel.send(
            file=discord.File(os.path.join(consts.STAFF_PATH, consts.STAFF[name]))
        )

    @bot.command(
        help="$image <kong token id> [hd]",
        brief="Get the image of a Rumble Kong by token id.",
    )
    async def image(ctx, *args):
        image_string = "image_url"
        if len(args) > 1 and str(args[1]).lower() == "hd":
            image_string = "image_original_url"

        params = {"token_ids": args[0], "collection_slug": "rumble-kong-league"}
        kong_url = opensea.fetch_opensea_asset(consts.OPENSEA_ASSETS_URL, params)[
            "assets"
        ][0][image_string]
        await ctx.channel.send(str(kong_url))

    @bot.command(
        help=("$jersey <kong token id> <team jersey name>"),
        brief="Rep team's jersey on your Kong.",
    )
    async def jersey(ctx, *args):
        kong = kong_util.draw_naked_kong(int(args[0]))
        jersey_kong = kong_util.apply_drip(kong, str(args[1]).lower(), True)
        await send_image_binary(ctx, jersey_kong)

    @bot.command(
        help=("$jersey <kong token id> <drip name>"),
        brief="Add some drip to your Kong.",
    )
    async def drip(ctx, *args):
        kong = kong_util.draw_naked_kong(int(args[0]))
        dripped_kong = kong_util.apply_drip(kong, str(args[1]).lower(), False)
        await send_image_binary(ctx, dripped_kong)

    def build_rarity_card(kong_token_id: int) -> Tuple[discord.File, discord.Embed]:
        image_name = f"{kong_token_id}.jpg"
        kong_image_path = os.path.join(KONGS_PATH, image_name)
        img_file = discord.File(kong_image_path, filename=image_name)

        discord_message = discord.Embed(
            title=f"Kong #{kong_token_id} Rarity Card",
            url=f"{KONG_ASSET_OPENSEA_URL}{kong_token_id}",
            color=0x00ff00
        )

        discord_message.set_thumbnail(url=f"attachment://{image_name}")
        discord_message.add_field(
            name="Defense",
            value=META[kong_token_id]["boosts"]["defense"],
            inline=True
        )
        discord_message.add_field(
            name="Finish",
            value=META[kong_token_id]["boosts"]["finish"],
            inline=True
        )
        discord_message.add_field(
            name="Shooting",
            value=META[kong_token_id]["boosts"]["shooting"],
            inline=True
        )
        discord_message.add_field(
            name="Vision",
            value=META[kong_token_id]["boosts"]["vision"],
            inline=True
        )
        discord_message.add_field(
            name="Boost Total", value=META[kong_token_id]["boostsRank"]["total"], inline=False
        )
        discord_message.add_field(
            name="Boost Rank", value=META[kong_token_id]["boostsRank"]["rank"], inline=True
        )
        discord_message.add_field(
            name="Visual Rank", value=META[kong_token_id]["visualRarityScore"]["rank"], inline=True
        )
        discord_message.add_field(
            name="Total Rank", value=META[kong_token_id]["totalRarityRank"], inline=True
        )

        return img_file, discord_message

    @bot.command(
        help=("$rank <kong token id>"),
        brief="Gives you (i) visual, (ii) boost and (iii) total rank of your kong."
    )
    async def rank(ctx, *args):

        kong_token_id = int(args[0])
        img_file, discord_message = build_rarity_card(kong_token_id)

        await ctx.channel.send(file=img_file, embed=discord_message)

    @bot.command(
        help=("$totalrank <rank number>"),
        brief="Gives you the kong whose total rank is your input."
    )
    async def totalrank(ctx, *args):

        total_rank_value = int(args[0])
        rank_diff = float('inf')
        kong_token_id = -1

        for ix, kong in enumerate(META):
            new_rank_diff = abs(kong["totalRarityRank"] - total_rank_value)
            if new_rank_diff < rank_diff:
                kong_token_id = ix
                rank_diff = new_rank_diff

        img_file, discord_message = build_rarity_card(kong_token_id)

        await ctx.channel.send(file=img_file, embed=discord_message)

    @bot.command(
        help=("$visualrank <rank number>"),
        brief="Gives you the kong whose visual rank is your input."
    )
    async def visualrank(ctx, *args):

        rank_diff = float('inf')
        closest_kong_token_id = -1
        visual_rank_value = int(args[0])
        kong_token_id: List[int] = []

        for ix, kong in enumerate(META):

            if kong["visualRarityScore"]["rank"] == visual_rank_value:
                # ! only allow up to 5 matches
                if len(kong_token_id) == 5:
                    break
                kong_token_id.append(ix)

            new_rank_diff = abs(kong["visualRarityScore"]["rank"] - visual_rank_value)
            if new_rank_diff < rank_diff:
                closest_kong_token_id = ix
                rank_diff = new_rank_diff

        if len(kong_token_id) > 0:
            for kong_id in kong_token_id:
                img_file, discord_message = build_rarity_card(kong_id)
                await ctx.channel.send(file=img_file, embed=discord_message)
        else:
            img_file, discord_message = build_rarity_card(closest_kong_token_id)
            await ctx.channel.send(file=img_file, embed=discord_message)

    # TODO: not DRY. same as above
    @bot.command(
        help=("$boostrank <rank number>"),
        brief="Gives you the kong whose boost rank is your input."
    )
    async def boostrank(ctx, *args):

        rank_diff = float('inf')
        closest_kong_token_id = -1
        boost_rank_value = int(args[0])
        kong_token_id: List[int] = []

        for ix, kong in enumerate(META):

            if kong["boostsRank"]["rank"] == boost_rank_value:
                # ! only allow up to 5 matches
                if len(kong_token_id) == 5:
                    break
                kong_token_id.append(ix)
            new_rank_diff = abs(kong["visualRarityScore"]["rank"] - boost_rank_value)
            if new_rank_diff < rank_diff:
                closest_kong_token_id = ix
                rank_diff = new_rank_diff

        if len(kong_token_id) > 0:
            for kong_id in kong_token_id:
                img_file, discord_message = build_rarity_card(kong_id)
                await ctx.channel.send(file=img_file, embed=discord_message)
        else:
            img_file, discord_message = build_rarity_card(closest_kong_token_id)
            await ctx.channel.send(file=img_file, embed=discord_message)          

    # @bot.command(help="Tells you a joke.", brief="Funny jokes left and right.")
    # async def joke(ctx, *args):
    #     j = await Jokes()
    #     joke = await j.get_joke(blacklist=["racist", "religious", "political", "sexist", "nsfw",  "explicit"])
    #     if joke["type"] == "single": # Print the joke
    #         await ctx.channel.send(str(joke["joke"]))
    #     else:
    #         await ctx.channel.send(str(joke["setup"]))
    #         time.sleep(3)
    #         await ctx.channel.send(str(joke["delivery"]))

    # TODO:
    # == !Floor ============================================================================
    # @bot.command(
    #     help="Get statistics about the floor price of RKL collections.",
    #     brief="collection (string):",
    # )
    # async def floor(ctx, *args):
    #     collection = args[0]

    #     filter = ""
    #     if len(args) > 1:
    #         filter = args[1].title()
    #     if collection == "sneakers":
    #         filter = "Sneakers"

    #     listings = util.read_json(
    #         os.path.join(consts.CACHE_PATH, collection, "-asset-cache.json")
    #     )["assets"]
    #     embed = opensea.construct_floor_stats_embed(collection, listings, filter)
    #     await ctx.channel.send(embed=embed)
