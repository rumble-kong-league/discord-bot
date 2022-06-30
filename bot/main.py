import os
from os.path import exists
import discord
from discord.ext import commands
from time import time, sleep

import bot.src.consts as consts
import bot.src.util as util
import bot.src.opensea as opensea
import bot.src.kong as kong_util


def initialize_bot():
    bot = commands.Bot(command_prefix="!", case_insensitive=True)
    register_commands(bot)
    bot.run(consts.DISCORD_TOKEN)


# TODO: remove these commands from here, they do not belong here
# TODO: main is purely an entrypoint
# Include chat commands within this function to ensure they are registered on startup
def register_commands(bot):

    # == !IAmKong ====================================================================
    @bot.command(help="I am Kong!", brief="I am Kong!")
    async def iamkong(ctx, *_args):
        gif = discord.File(os.path.join(consts.MEMES_PATH, "iamkong.gif"))
        await ctx.channel.send(file=gif)

    # == !Yes =========================================================================
    @bot.command(help="Yes.", brief="Yes.")
    async def yes(ctx, *_args):
        image = discord.File(os.path.join(consts.MEMES_PATH, "yes.png"))
        await ctx.channel.send(file=image)

    # == !Praise =======================================================================
    @bot.command(
        help="Give thanks to the RKL team members.",
        brief="name (string): Name of the team member to praise",
    )
    async def praise(ctx, *args):
        name = args[0]
        if name not in consts.STAFF:
            name = "team"

        gif = os.path.join(consts.STAFF_PATH, consts.STAFF[name])
        await ctx.channel.send(file=discord.File(gif))

    # == !Image =========================================================================
    @bot.command(
        help="Get the image of a Rumble Kong by id.",
        brief="id (number): Token ID of the Kong to display",
    )
    async def image(ctx, *args):
        id = args[0]

        image_string = "image_url"
        if len(args) > 1:
            if args[1] == "hd":
                image_string = "image_original_url"

        params = {"token_ids": id, "collection_slug": "rumble-kong-league"}
        kong_url = opensea.fetch_opensea_asset(consts.OPENSEA_ASSETS_URL, params)[
            "assets"
        ][0][image_string]
        await ctx.channel.send(str(kong_url))

    # == !Jersey ===========================================================================
    @bot.command(
        help="Rep your team's jersey on your Kong.",
        brief="id (number): Token ID of the Kong to display, team (string): Name of the team to use the jersey from",
    )
    async def jersey(ctx, *args):
        id_ = args[0]
        team_jersey = args[1]

        kong = kong_util.draw_naked_kong(int(id_))
        jersey_kong = kong_util.apply_drip(kong, team_jersey, True)
        jersey_kong.save(os.path.join(consts.TMP_PATH, "testkong.png"))

        image = discord.File(os.path.join(consts.TMP_PATH, "testkong.png"))
        await ctx.channel.send(file=image)

    # == !Drip =============================================================================
    @bot.command(
        help="Add some drip to your Kong.",
        brief="id (number): Token ID of the Kong to display, team (string): Name of the drip to apply",
    )
    async def drip(ctx, *args):
        id_ = args[0]
        drip_type = args[1]

        kong = kong_util.draw_naked_kong(int(id_))
        dripped_kong = kong_util.apply_drip(kong, drip_type, False)
        dripped_kong.save(os.path.join(consts.TMP_PATH, "testkong.png"))

        image = discord.File(os.path.join(consts.TMP_PATH, "testkong.png"))
        await ctx.channel.send(file=image)

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


if __name__ == "__main__":

    # TODO:
    # for collection in consts.COLLECTIONS:
    #     if exists(consts.CACHE_PATH + collection + "-asset-cache.json"):
    #         util.log(
    #             "Skipping caching assets for "
    #             + collection
    #             + " because file already exists"
    #         )

    #     else:
    #         success = opensea.initialize_asset_cache(collection)
    #         if success == False:
    #             break

    initialize_bot()

        # while True:
        #    opensea.update_asset_cache(collection)
        #    sleep(consts.CACHE_UPDATE_RATE)
