import os
# from os.path import exists
import discord
from discord.ext import commands
from io import BytesIO
from jokeapi import Jokes
import time
from random import randint
# from time import time, sleep

import bot.src.consts as consts
import bot.src.util as util
import bot.src.opensea as opensea
import bot.src.kong as kong_util


def initialize_bot():
    bot = commands.Bot(command_prefix="!", case_insensitive=True)
    register_commands(bot)
    bot.run(consts.DISCORD_TOKEN)


async def send_image_binary(ctx, img):
    with BytesIO() as image_binary:
        img.save(image_binary, "PNG")
        image_binary.seek(0)
        await ctx.channel.send(file=discord.File(fp=image_binary, filename="tacpeo.png"))    


# TODO: remove these commands from here, they do not belong here
# TODO: main is purely an entrypoint
# Include chat commands within this function to ensure they are registered on startup
def register_commands(bot):

    @bot.command(help="Sweep!", brief="Sweep!")
    async def sweep(ctx, *_args):
        await ctx.channel.send(file=discord.File(os.path.join(consts.MEMES_PATH, "sweep.gif")))

    @bot.command(help="On your head!", brief="OYH!")
    async def oyh(ctx, *_args):
        await ctx.channel.send(file=discord.File(os.path.join(consts.MEMES_PATH, "oyh.gif")))

    @bot.command(help="Let's fucking go!", brief="LFG!")
    async def lfg(ctx, *_args):
        await ctx.channel.send(file=discord.File(os.path.join(consts.MEMES_PATH, "lfg.gif")))

    @bot.command(help="Good Morning!", brief="Good Morning!")
    async def gm(ctx, *_args):
        await ctx.channel.send(file=discord.File(os.path.join(consts.MEMES_PATH, "gm.gif")))

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
        help="Give thanks to the RKL team members.",
        brief="name (string): Name of the team member to praise",
    )
    async def praise(ctx, *args):
        name = args[0]
        if name not in consts.STAFF:
            name = "team"
        await ctx.channel.send(
            file=discord.File(os.path.join(consts.STAFF_PATH, consts.STAFF[name]))
        )

    @bot.command(
        help="Get the image of a Rumble Kong by id.",
        brief="id (number): Token ID of the Kong to display",
    )
    async def image(ctx, *args):
        image_string = "image_url"
        if len(args) > 1 and args[1] == "hd":
            image_string = "image_original_url"

        params = {"token_ids": args[0], "collection_slug": "rumble-kong-league"}
        kong_url = opensea.fetch_opensea_asset(consts.OPENSEA_ASSETS_URL, params)[
            "assets"
        ][0][image_string]
        await ctx.channel.send(str(kong_url))

    # TODO: not DRY the part where you save to binary
    @bot.command(
        help="Rep your team's jersey on your Kong.",
        brief=("id (number): Token ID of the Kong to display,"
        " team (string): Name of the team to use the jersey from"),
    )
    async def jersey(ctx, *args):
        kong = kong_util.draw_naked_kong(int(args[0]))
        jersey_kong = kong_util.apply_drip(kong, args[1], True)
        await send_image_binary(ctx, jersey_kong)

    @bot.command(
        help="Add some drip to your Kong.",
        brief=("id (number): Token ID of the Kong to display,"
        " team (string): Name of the drip to apply"),
    )
    async def drip(ctx, *args):
        kong = kong_util.draw_naked_kong(int(args[0]))
        dripped_kong = kong_util.apply_drip(kong, args[1], False)
        await send_image_binary(ctx, dripped_kong)

    @bot.command(help="Tells you a joke.", brief="Funny jokes left and right.")
    async def joke(ctx, *args):
        j = await Jokes()
        joke = await j.get_joke(blacklist=["racist", "religious", "political", "sexist", "nsfw",  "explicit"])
        if joke["type"] == "single": # Print the joke
            await ctx.channel.send(str(joke["joke"]))
        else:
            await ctx.channel.send(str(joke["setup"]))
            time.sleep(3)
            await ctx.channel.send(str(joke["delivery"]))

    @bot.command(help="Random selector.", brief="Randomly selects from a set.")
    async def pick(ctx, *args):
        pick_phrases = ["I pick", "And the winner is", "Fabulous performance", "WAGMI"]
        gotcha = ["jk lol", "he he, actually no", "got ya, not really", "nope lol, just messing with you"]

        trip_up_count = randint(1, 4)
        args_len = len(args)

        while trip_up_count > 0:
            winner = randint(0, args_len - 1)
            phrase_ix = randint(0, len(pick_phrases) - 1)
            gotcha_ix = randint(0, len(gotcha) - 1)

            await ctx.channel.send(f"{pick_phrases[phrase_ix]} {args[winner]}")
            time.sleep(3)
            await ctx.channel.send(f"{gotcha[gotcha_ix]}")

            trip_up_count -= 1
        time.sleep(1)

        winner = randint(0, args_len - 1)
        await ctx.channel.send(f"{pick_phrases[phrase_ix]} {args[winner]}")

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
