import datetime

from aiogram import Router, types
from aiogram.filters import Command, CommandObject
from redis_client import RedisClient
from utils import convert_str_to_int_or_float

router = Router()


@router.message(Command('start'))
async def startup(message: types.Message):
    await message.answer('Привет! Меня зовут Дэнни (от слова деньги) и я готов помочь вам с курсом валют!\n\n'
                         'Давайте начнём?\n\n'
                         'Вводите команду /rates, чтобы получить все котировки\n\n'
                         'Вводите команду /exchange "ВАЛЮТА" "КОЛ-ВО" чтобы получить стоимость такого количества этой'
                         'валюты в рублях!')


@router.message(Command('rates'))
async def get_rates(message: types.Message):
    rates = await RedisClient().get_all_rates()
    text = '\n- '.join(rates)
    await message.answer(f'Котировки валют на {datetime.date.today()}:\n\n- {text}')


@router.message(Command('exchange'))
async def get_exchanged_amount(message: types.Message, command: CommandObject):
    try:
        currency, amount = command.args.split()
    except (AttributeError, ValueError):
        await message.answer('Команда была указана неверно!\nКоманда должна быть указана следующим образом:'
                             ' /exchange "валюта" "количество валюты" (пример: /exchange USD 20)')
    else:
        if not amount.isdigit():
            await message.answer('Необходимо указать количество валюты целым или дробным числом!')

        amount = convert_str_to_int_or_float(amount)
        redis_client = RedisClient()
        try:
            transfered_amount = await redis_client.transfer_currency(currency, amount)
        except TypeError:
            all_currency = await redis_client.get_all_currency_names()
            await message.answer(f'Валюта не найдена! Вы должны ввести валюту из этого списка:\n\n '
                                 f'{", ".join(all_currency)}')
        else:
            await message.answer(f'На {datetime.date.today()} {amount} {currency} в рублях равно {transfered_amount}')
