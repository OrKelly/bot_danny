import json
from typing import Union

import aioredis
from core import config


class RedisClient:
    """Класс для взаимодействия с Redis и его данными"""
    REDIS_URL = config.REDIS_URL

    def __init__(self):
        self.redis_client = aioredis.from_url(self.REDIS_URL)

    async def set_currency(self, currency: str, value: str):
        """Метод добавляет новую запись с валютой в Redis"""
        # редис не может принимать словарь как значение, конвертирует в json строку
        value = json.dumps(value, ensure_ascii=False)
        await self.redis_client.set(currency, value)

    async def get_currency(self, currency: str) -> Union[int, float]:
        """Метод получает валюту по ключу"""
        currency_data = await self.redis_client.get(currency)
        # конвертируем json строку в словарь
        currency_data = json.loads(currency_data)
        currency_value = float(currency_data['value'].replace(',', '.'))
        return currency_value

    async def transfer_currency(self, currency_to_transfer: str, amount: int) -> Union[float, int]:
        """Метод конвертирует рубли в выбранную валюту по актуальному курсу"""
        currency_price = await self.get_currency(currency_to_transfer.upper())
        total_amount = currency_price * amount
        return total_amount

    async def get_all_rates(self):
        """Метод получает все котировки"""
        rates_msg = []
        keys = await self.redis_client.keys()
        for key in keys:
            try:
                currency_data = await self.redis_client.get(key)
                currency_data = json.loads(currency_data)
                rates_msg.append(f'{currency_data["name"]} ({currency_data["char_code"]}) - '
                                 f'{currency_data["value"]} рублей')
            except Exception:
                continue
        return rates_msg

    async def get_all_currency_names(self):
        """Метод возвращает список имен всех валют"""
        keys = await self.redis_client.keys()
        return list(map(lambda x: x.decode('utf-8'), keys))
