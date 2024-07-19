import copy
import re
from typing import Union


def perform_key(key: str) -> str:
    """Метод оставляет в ключе только буквы и цифры, спец символы убираются"""
    new_key = re.sub(r'(\w+:)|(\W)', '', key)
    if new_key:
        return new_key
    return key


def camel_to_snake(name: str):
    """Переводит строку в snake"""
    name = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', name)
    return re.sub('([a-z0-9])([A-Z])', r'\1_\2', name).lower()


def camel_to_snake_dict(data):
    """Рекурсивно изменяет ключи словаря в snake"""
    _data = copy.deepcopy(data)
    new_data = {}
    if isinstance(_data, dict):
        for key, value in _data.items():
            key = perform_key(key)
            new_key = camel_to_snake(key)
            new_data[new_key] = camel_to_snake_dict(value)
        return new_data
    elif isinstance(_data, list):
        return [camel_to_snake_dict(item) for item in _data]
    else:
        return _data


def convert_str_to_int_or_float(num: str) -> Union[float, int]:
    if ',' or '.' in num:
        return float(num.replace(',', '.'))
    return int(num)
