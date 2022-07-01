from bot.src.discord_bot import initialize_bot


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
