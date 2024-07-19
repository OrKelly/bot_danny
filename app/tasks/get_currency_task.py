import asyncio

import aiohttp
import xmltodict
from core import config
from redis_client import RedisClient
from utils import camel_to_snake_dict


async def get_currency_rates():
    async with aiohttp.ClientSession() as session:
        async with session.get(config.URL_TO_PARSE) as resp:
            result = await resp.text()

    redis = RedisClient()
    parsed_response_data = xmltodict.parse(result)
    performed_dict = camel_to_snake_dict(parsed_response_data)
    valutes_data = performed_dict['val_curs']['valute']

    for valute in valutes_data:
        await redis.set_currency(valute['char_code'], valute)
