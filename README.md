**Бот Дэнни** - бот, позволяющий получать актуальную информацию о курсе рубля через ЦБ России. Стек: aiogram,
redis (aioredis), aiohttp (для отправки запросов)

## Команды

- /start - выводит приветственное сообщение и список всех команд
- /rates - получает список всех текущих котировок и выводит их пользователю
- /exchange ВАЛЮТА КОЛ-ВО - переводит указанное кол-во указанной валюты в рубли и возвращает пользователю

## Локальный запуск
Cоздайте файл .env и перенесите данные из .env.example в него, выставив свои значения.

Далее нужно установить все зависимости посредством команды: 
```
pip install -r requirements.txt
```


Приложение запускается при помощи команды (убедитесь что у вас запущен redis):
```
python app/main.py
```
Принудительно запустить таску по парсингу биржи ЦБ РФ можно при помощи команды:
```
python app/tasks/get_currency_task.py
```

Для запуска с помощью Docker используйте команды:
```
docker-compose build
docker-compose up
```


