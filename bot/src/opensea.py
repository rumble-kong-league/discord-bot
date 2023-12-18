from sys import maxsize
from time import time, sleep
from discord import Embed, Color
from requests import request

import bot.src.consts as consts
import bot.src.util as util


def construct_headers():
    return {
        "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:47.0) Gecko/20100101 Firefox/47.0",
        "Accept": "application/json",
        "X-API-KEY": consts.OPENSEA_API_KEY,
    }


def fetch_opensea_asset(address, token_id):
    url = f"https://api.opensea.io/api/v2/chain/ethereum/contract/{address}/nfts/{token_id}"
    resp = request("GET", url, headers=construct_headers())
    resp_json = resp.json()
    return resp_json


def initialize_asset_cache(
    collection,
    rest_time=consts.DEFAULT_REST_TIME,
    max_attempts=consts.DEFAULT_MAX_ATTEMPTS,
):
    util.log("Initializing asset cache for collection: " + collection)

    timestamp = time()
    cursor = ""
    assets = {}
    num_listed = 0
    page_num = 0
    num_failed_attempts = 0
    params = {
        "collection_slug": consts.COLLECTIONS[collection]["slug"],
        "order_direction": "desc",
        "include_orders": "true",
        "limit": "50",
    }

    # Iterate through all pages of the API response saving info about the assets.
    while cursor != None:
        page = fetch_opensea_asset(consts.OPENSEA_ASSETS_URL, params)

        # Handle a failed API call, usually due to being rate-limited by OpenSea.
        if not "assets" in page:
            num_failed_attempts += 1
            util.log(
                "Failed to get page #"
                + str(page_num)
                + " - cursor: "
                + cursor
                + " - attempt: "
                + str(num_failed_attempts),
                1,
            )

            # Abort if MAX_ATTEMPTS has been exceeded, to prevent getting caught in a loop and spamming the API further.
            if num_failed_attempts > max_attempts:
                util.log(
                    "Error while trying to cache collection: "
                    + collection
                    + " - terminating bot",
                    2,
                )
                failed_asset_cache = {"cursor": cursor, "assets": assets}
                util.write_json(
                    consts.CACHE_PATH + collection + "-failed-asset-cache.json",
                    failed_asset_cache,
                )
                return False

        # Handle a successful API call by adding the returned information to the collection cache.
        else:
            num_failed_attempts = 0

            # Loop through and extract the relevant data from the assets in the page.
            for asset in page["assets"]:
                id = asset["token_id"]

                # If the asset has no sell orders, it is unlisted.
                listing_price = None
                if asset["sell_orders"]:
                    listing_price = asset["sell_orders"][0]["current_price"]
                    num_listed += 1

                assets[id] = {
                    "owner": asset["owner"]["address"],
                    "image": {
                        "url": asset["image_url"],
                        "original_url": asset["image_original_url"],
                    },
                    "traits": asset["traits"],
                    "num_sales": asset["num_sales"],
                    "last_sale": asset["last_sale"],
                    "listing_price": listing_price,
                }

            util.log(
                "Got assets for page #"
                + str(page_num)
                + " - listed: "
                + str(num_listed)
                + " - total: "
                + str(len(assets)),
                1,
            )

            # Update the call params with the new cursor, allowing the next page of results to be retrieved.
            cursor = page["next"]
            params["cursor"] = cursor
            page_num += 1

        # Be nice to the OpenSea API.
        # Be extra nice if previous API calls have failed, to try and wait out the rate-limit.
        rest_time = rest_time * (num_failed_attempts + 1)
        util.log("Sleeping for " + str(rest_time) + " seconds", 2)
        sleep(rest_time)

    util.log("Finished caching assets for " + collection, 1)
    asset_cache = {"updated": timestamp, "assets": assets}
    util.write_json(consts.CACHE_PATH + collection + "-asset-cache.json", asset_cache)
    return True


def update_asset_cache(collection):
    timestamp = time()
    path = consts.CACHE_PATH + collection + "-asset-cache.json"
    cache = util.read_json(path)

    params = {
        "collection_slug": consts.COLLECTIONS[collection]["slug"],
        "only_opensea": "true",
        "event_type": "created",
        "after": cache["updated"],
    }

    page = fetch_opensea_asset(consts.OPENSEA_EVENTS_URL, params)
    for event in page["asset_events"]:
        id = event["asset"]["token_id"]
        if id in cache["assets"]:
            cache["assets"][id]["listing_price"] = event["starting_price"]

    cache["updated"] = timestamp
    util.write_json(path, cache)
    return True


def calculate_floor_stats(assets):
    stats = {"Overall": {"floor_price": maxsize, "num_listed": 0}, "Boosts": {}}

    for id in assets:
        asset = assets[id]

        # Only consider assets with active listings when calculating floor stats.
        if asset["listing_price"]:
            new_global_floor = min(
                stats["Overall"]["floor_price"], float(asset["listing_price"])
            )
            stats["Overall"]["floor_price"] = new_global_floor
            stats["Overall"]["num_listed"] += 1

            boosts = 0
            traits = asset["traits"]

            for trait in traits:
                trait_type = trait["trait_type"]
                trait_value = trait["value"]

                if trait_type not in stats:
                    stats[trait_type] = {}

                if trait_type in consts.BOOST_TRAIT_TYPES:
                    boosts += trait_value

                else:
                    if trait_value not in stats[trait_type]:
                        stats[trait_type][trait_value] = {
                            "floor_price": float(asset["listing_price"]),
                            "num_listed": 1,
                        }

                    else:
                        stats_entry = stats[trait_type][trait_value]
                        new_floor = min(
                            stats_entry["floor_price"], float(asset["listing_price"])
                        )
                        stats_entry["floor_price"] = new_floor
                        stats_entry["num_listed"] += 1

            # If the asset has no boost level, it is not a Kong and we can skip adding this embed label.
            if boosts > 0:
                rounded = round(boosts / 10) * 10
                if rounded not in stats["Boosts"]:
                    stats["Boosts"][rounded] = {
                        "floor_price": float(asset["listing_price"]),
                        "num_listed": 1,
                    }

                else:
                    stats_entry = stats["Boosts"][rounded]
                    new_floor = min(
                        stats_entry["floor_price"], float(asset["listing_price"])
                    )
                    stats_entry["floor_price"] = new_floor
                    stats_entry["num_listed"] += 1

    return stats


def construct_floor_stats_embed(collection_name, assets, filter):
    floor_stats = calculate_floor_stats(assets)

    embed = Embed(
        title=consts.COLLECTIONS[collection_name]["verbose"],
        description="There can be up to a 10 minute delay",
        color=Color.blue(),
    )

    embed.set_thumbnail(url=consts.COLLECTIONS[collection_name]["image"])

    embed.add_field(
        name="Overall",
        value="Floor: "
        + str(util.from_wei(floor_stats["Overall"]["floor_price"]))
        + "Ξ\nListed: "
        + str(floor_stats["Overall"]["num_listed"]),
        inline=False,
    )

    if filter != "":
        for trait_value in floor_stats[filter]:
            stats_entry = floor_stats[filter][trait_value]
            embed.add_field(
                name=trait_value,
                value="Floor: "
                + str(util.from_wei(stats_entry["floor_price"]))
                + "Ξ\nListed: "
                + str(stats_entry["num_listed"]),
                inline=True,
            )

    return embed
