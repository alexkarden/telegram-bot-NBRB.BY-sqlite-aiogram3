import requests
import aiosqlite
import logging
from aiogram import Bot
import asyncio
import time
from datetime import datetime, timedelta
from config import DATABASE_NAME, SHORTLISTOFCURRENCY




# Функция для преобразования строковой даты из ответа сайта nbrb.by
def convert_str_to_date(date_str):
    try:
        # Преобразуем строку даты в объект datetime с указанным форматом
        date_object = datetime.strptime(date_str, "%Y-%m-%dT%H:%M:%S")
        # Приводим объект datetime к timestamp (количество секунд с 1 января 1970 года)
        return int(date_object.timestamp())
    except ValueError as e:  # Обрабатываем возможную ошибку преобразования строки
        # Выводим сообщение об ошибке, если строка не соответствует ожидаемому формату
        print(f"Ошибка преобразования строки даты: {e}")
        return None  # Возвращаем None в случае ошибки


# Функция для преобразования временной метки в строковую дату для получения валют на определенную дату nbrb.by
def convert_date_to_str(date_sec):
    try:
        # Преобразуем временную метку (timestamp) в объект time.struct_time в формате UTC
        date_object = time.gmtime(date_sec)
        # Форматируем объект time.struct_time в строку в формате "YYYY-MM-DD"
        time_str = time.strftime("%Y-%m-%d", date_object)
        return time_str  # Возвращаем отформатированную строку даты
    except Exception as e:  # Обрабатываем любые исключения, которые могут произойти
        # Выводим сообщение об ошибке, если произошла ошибка во время преобразования
        print(f"Ошибка преобразования даты: {e}")
        return None  # Возвращаем None в случае ошибки




# Функция для получения курсов валют с НБРБ
def get_exchange_rates():
    try:
        response = requests.get("https://api.nbrb.by/exrates/rates?periodicity=0")
        response.raise_for_status()  # Проверка на ошибки
        rates = response.json()
        return rates
    except Exception as e:
        print(f"Ошибка при получении курсов валют: {e}")
        return None

# Функция для получения курсов валют с НБРБ за определенную дату
def get_exchange_rates_for_date(date_int):
    date = convert_date_to_str(date_int)
    try:
        response = requests.get(f"https://api.nbrb.by/exrates/rates?ondate={date}&periodicity=0")
        response.raise_for_status()  # Проверка на ошибки
        rates = response.json()
        return rates
    except Exception as e:
        print(f"Ошибка при получении курсов валют: {e}")
        return None





# Инициализация базы данных
async def init_db():
    try:
        async with aiosqlite.connect(DATABASE_NAME) as db:
            # Создание таблицы users, если она еще не существует
            await db.execute(""
                             "CREATE TABLE IF NOT EXISTS users ("
                             "id INTEGER PRIMARY KEY, "
                             "user_id INTEGER UNIQUE, "
                             "first_name TEXT, "
                             "last_name TEXT, "
                             "username TEXT, "
                             "user_added INTEGER NOT NULL, "
                             "user_blocked INTEGER NOT NULL, "
                             "subscription_status TEXT, "
                             "time_of_add INTEGER)"
                             "")

            # Создание таблицы currency_rates, если она еще не существует
            await db.execute(""
                             "CREATE TABLE IF NOT EXISTS currency_rates ("
                             "id INTEGER PRIMARY KEY,"
                             "date INTEGER UNIQUE NOT NULL,"
                             "date_refresh INTEGER,"
                             "AUD_rate REAL, AUD_scale INTEGER , AUD_name TEXT, "
                             "AMD_rate REAL, AMD_scale INTEGER , AMD_name TEXT, "
                             "BGN_rate REAL, BGN_scale INTEGER , BGN_name TEXT, "
                             "BRL_rate REAL, BRL_scale INTEGER , BRL_name TEXT, "
                             "UAH_rate REAL, UAH_scale INTEGER , UAH_name TEXT, "
                             "DKK_rate REAL, DKK_scale INTEGER , DKK_name TEXT, "
                             "AED_rate REAL, AED_scale INTEGER , AED_name TEXT, "
                             "USD_rate REAL, USD_scale INTEGER , USD_name TEXT, "
                             "VND_rate REAL, VND_scale INTEGER , VND_name TEXT, "
                             "EUR_rate REAL, EUR_scale INTEGER , EUR_name TEXT, "
                             "PLN_rate REAL, PLN_scale INTEGER , PLN_name TEXT, "
                             "JPY_rate REAL, JPY_scale INTEGER , JPY_name TEXT, "
                             "INR_rate REAL, INR_scale INTEGER , INR_name TEXT, "
                             "IRR_rate REAL, IRR_scale INTEGER , IRR_name TEXT, "
                             "ISK_rate REAL, ISK_scale INTEGER , ISK_name TEXT, "
                             "CAD_rate REAL, CAD_scale INTEGER , CAD_name TEXT, "
                             "CNY_rate REAL, CNY_scale INTEGER , CNY_name TEXT, "
                             "KWD_rate REAL, KWD_scale INTEGER , KWD_name TEXT, "
                             "MDL_rate REAL, MDL_scale INTEGER , MDL_name TEXT, "
                             "NZD_rate REAL, NZD_scale INTEGER , NZD_name TEXT, "
                             "NOK_rate REAL, NOK_scale INTEGER , NOK_name TEXT, "
                             "RUB_rate REAL, RUB_scale INTEGER , RUB_name TEXT, "
                             "XDR_rate REAL, XDR_scale INTEGER , XDR_name TEXT, "
                             "SGD_rate REAL, SGD_scale INTEGER , SGD_name TEXT, "
                             "KGS_rate REAL, KGS_scale INTEGER , KGS_name TEXT, "
                             "KZT_rate REAL, KZT_scale INTEGER , KZT_name TEXT, "
                             "TRY_rate REAL, TRY_scale INTEGER , TRY_name TEXT, "
                             "GBP_rate REAL, GBP_scale INTEGER , GBP_name TEXT, "
                             "CZK_rate REAL, CZK_scale INTEGER , CZK_name TEXT, "
                             "SEK_rate REAL, SEK_scale INTEGER , SEK_name TEXT, "
                             "CHF_rate REAL, CHF_scale INTEGER , CHF_name TEXT)"
                             "")
            await db.commit()
    except aiosqlite.Error as e:
        logging.error(f"Ошибка при инициализации базы данных: {e}")


async def add_db():
    date_refresh = int(time.time())
    try:
        async with aiosqlite.connect(DATABASE_NAME) as db:

            for rate in get_exchange_rates():
                currency_date = convert_str_to_date(rate['Date'])

                currency_code = rate['Cur_Abbreviation']
                currency_scale = int(rate['Cur_Scale'])
                currency_rate = rate['Cur_OfficialRate']
                currency_name = rate['Cur_Name']
                #print(currency_code, currency_scale, currency_rate, currency_name)
                async with db.execute("SELECT * FROM currency_rates WHERE date = ?;", (currency_date,)) as cursor:
                    result = await cursor.fetchall()

                    if not result:  # Проверяем, пуст ли список
                        await db.execute(F"INSERT INTO currency_rates (date, date_refresh, {currency_code}_rate, {currency_code}_scale, {currency_code}_name ) VALUES (?,?,?,?,?);", (currency_date, date_refresh, currency_rate, currency_scale, currency_name))
                    else:
                        await db.execute(
                            f"UPDATE currency_rates SET date_refresh = ?, {currency_code}_rate = ?, {currency_code}_scale = ?, {currency_code}_name = ? WHERE date = ?;",
                            (date_refresh, currency_rate, currency_scale, currency_name, currency_date))

            await db.commit()  # Не забудьте зафиксировать изменения
    except aiosqlite.Error as e:
        logging.error(f"Ошибка при инициализации базы данных: {e}")


async def add_db_date(date_int):
    try:
        async with aiosqlite.connect(DATABASE_NAME) as db:

            for rate in get_exchange_rates_for_date(date_int):
                currency_date = convert_str_to_date(rate['Date'])
                currency_code = rate['Cur_Abbreviation']
                currency_scale = int(rate['Cur_Scale'])
                currency_rate = rate['Cur_OfficialRate']
                currency_name = rate['Cur_Name']
                print(currency_code, currency_scale, currency_rate, currency_name)
                async with db.execute("SELECT * FROM currency_rates WHERE date = ?;", (currency_date,)) as cursor:
                    result = await cursor.fetchall()

                    if not result:  # Проверяем, пуст ли список
                        await db.execute(F"INSERT INTO currency_rates (date, {currency_code}_rate, {currency_code}_scale, {currency_code}_name ) VALUES (?,?,?,?);", (currency_date, currency_rate, currency_scale, currency_name))
                    else:
                        await db.execute(
                            f"UPDATE currency_rates SET {currency_code}_rate = ?, {currency_code}_scale = ?, {currency_code}_name = ? WHERE date = ?;",
                            (currency_rate, currency_scale, currency_name, currency_date))

            await db.commit()  # Не забудьте зафиксировать изменения
    except aiosqlite.Error as e:
        logging.error(f"Ошибка при инициализации базы данных: {e}")





# Добавление пользователя в базу данных
async def add_user_db(user_id, first_name, last_name, username):
    time_of_add = int(time.time())
    try:
        async with aiosqlite.connect(DATABASE_NAME) as db:
            # Проверка, существует ли пользователь в базе данных
            async with db.execute("SELECT * FROM users WHERE user_id = ?", (user_id,)) as cursor:
                result = await cursor.fetchone()
                if result is not None:
                    # Если пользователь существует, можно обновить его данные
                    await db.execute("UPDATE users SET first_name = ?, last_name = ?, username = ?, user_added = ? WHERE user_id = ? ", (first_name, last_name, username, 1, user_id))
                    logging.info(f"Пользователь с ID {user_id} обновлен в базе данных.")
                else:
                    # Если не существует, добавляем нового пользователя
                    await db.execute("INSERT INTO users (user_id, first_name, last_name, username, user_added, user_blocked, time_of_add, subscription_status) VALUES (?, ?, ?, ?, ?, ?, ?, ?)", (user_id, first_name, last_name, username, 1, 0, time_of_add,'none'))
                    logging.info(f"Пользователь с ID {user_id} добавлен в базу данных.")
                await db.commit()
    except aiosqlite.Error as e:
        logging.error(f"Ошибка при добавлении пользователя в базу данных: {e}")
    except Exception as e:
        logging.error(f"Произошла неожиданная ошибка: {e}")



#Получение статуса подписки
async def get_status_subscribed_user_db(user_id):
    try:
        async with aiosqlite.connect(DATABASE_NAME) as db:
            async with db.execute("SELECT subscription_status  FROM users WHERE user_id = ?", (user_id,)) as cursor:
                result = await cursor.fetchone()

                if result is None:
                    # Если пользователь не найден
                    logging.info(f"Пользователь с ID {user_id} не найден.")
                    return None  # Пользователь не найден


                return result[0]
    except aiosqlite.Error as e:
        # Обработка ошибок базы данных
        logging.error(f"Ошибка доступа к базе данных при получении статуса подписки пользователя {user_id}: {e}")
        return None  # В случае ошибки также можем вернуть None



# запись статуса подписки в базу
async def subscribed_user_db(user_id, status):
    try:
        async with aiosqlite.connect(DATABASE_NAME) as db:
            # Обновление статуса подписки

            cursor = await db.execute("UPDATE users SET subscription_status=? WHERE user_id = ?", (status, user_id))
            await db.commit()

            # Проверка количества обновленных строк
            if cursor.rowcount == 0:
                logging.warning(f"Пользователь с ID {user_id} не найден для подписки.")
    except aiosqlite.Error as e:
        logging.error(f"Ошибка базы данных при обработке подписки пользователя {user_id}: {e}")
    except Exception as e:
        logging.error(f"Произошла неожиданная ошибка обработки подписки пользователя {user_id}: {e}")




async def get_currency_db(kod):
    try:
        async with aiosqlite.connect(DATABASE_NAME) as db:
            async with db.execute(
                f"SELECT date, {kod}_rate AS rate, {kod}_scale AS scale, {kod}_name AS name, date_refresh FROM currency_rates ORDER BY date DESC LIMIT 1;"
            ) as cursor:
                result = await cursor.fetchone()  # Используйте fetchone для получения одной записи

                if result is None:  # Проверяем, пуст ли результат
                    return None
                else:
                    return result  # Возвращаем кортеж с результатом

    except aiosqlite.Error as e:
        logging.error(f"Ошибка при работе с базой данных: {e}")


async def all_kurs(currency_list):
    try:
        y = await get_currency_db('USD')
        # Конвертация времени Unix в datetime и добавление 3 часов
        date_object = datetime.utcfromtimestamp(y[0]) + timedelta(hours=3)
        date_str = date_object.strftime("%d.%m.%Y")

        date_refresh_object = datetime.utcfromtimestamp(y[4]) + timedelta(hours=3)
        date_refresh_str = date_refresh_object.strftime("%d.%m.%Y г. %H.%M.%S")

        text_bot = f'<b>Курсы валют на {date_str}:</b>\n<i>Обновлено: {date_refresh_str}</i>\n\n'

        # Получение и форматирование данных о валютах
        for currency in currency_list:
            x = await get_currency_db(currency)
            if x:  # Проверка на наличие данных
                text_bot += f"{get_flag(currency)} {x[2]} {currency} ({x[3]}): <b><code>{x[1]}</code></b> BYN\n"
            else:
                logging.warning(f"Нет данных для валюты: {currency}")
                print()

        return text_bot

    except aiosqlite.Error as e:
        logging.error(f"Ошибка при работе с базой данных: {e}")
    except Exception as e:
        logging.error(f"Возникла ошибка: {e}")




# Получение списка пользователей для рассылки
async def get_list_subscribed_user_db(period):
    try:
        async with aiosqlite.connect(DATABASE_NAME) as db:
            async with db.execute("SELECT user_id FROM users WHERE subscription_status = ?", (period,)) as cursor:
                subscribed_users = await cursor.fetchall()  # Здесь должен быть await для получения результата
                user_ids = [user[0] for user in subscribed_users]
                return user_ids
    except aiosqlite.Error as e:
        # Логируем ошибку или обрабатываем её как-то иначе
        logging.error(f"Произошла ошибка при получении списка пользователей: {e}")
        return []  # Возвращаем пустой список в случае ошибки













async def rassilka(bot: Bot,currency_list,status):
    try:
        text_bot = f'<b>Курсы валют на данный момент:</b>\n\n'

        # Получение и форматирование данных о валютах
        for currency in currency_list:
            x = await get_currency_db(currency)
            text_bot += f"{get_flag(currency)} {x[2]} {currency}: <b>{x[1]}</b> BYN\n"

        # Получение списка пользователей и отправка сообщений
        subscribed_users = await get_list_subscribed_user_db(status)
        for user_id in subscribed_users:
            try:
                await bot.send_message(user_id, text_bot, parse_mode='HTML')
                logging.info(f'Отправлено {user_id}')
            except Exception as e:
                logging.error(f'Не отправлено {user_id} - Ошибка: {e}')

    except aiosqlite.Error as e:
        logging.error(f"Ошибка при работе с базой данных: {e}")




def get_flag(currency):
    flags = {
        "AUD": "🇦🇺",  # Австралийский доллар
        "AMD": "🇦🇲",  # Армянский драм
        "BGN": "🇧🇬",  # Болгарский лев
        "BRL": "🇧🇷",  # Бразильский реал
        "UAH": "🇺🇦",  # Гривна
        "DKK": "🇩🇰",  # Датская крона
        "AED": "🇦🇪",  # Дирхам ОАЭ
        "USD": "🇺🇸",  # Доллар США
        "VND": "🇻🇳",  # Вьетнамский донг
        "EUR": "🇪🇺",  # Евро
        "PLN": "🇵🇱",  # Польский злотый
        "JPY": "🇯🇵",  # Японская иена
        "INR": "🇮🇳",  # Индийская рупия
        "IRR": "🇮🇷",  # Иранский риал
        "ISK": "🇮🇸",  # Исландская крона
        "CAD": "🇨🇦",  # Канадский доллар
        "CNY": "🇨🇳",  # Китайский юань
        "KWD": "🇰🇼",  # Кувейтский динар
        "MDL": "🇲🇹",  # Молдавский лей
        "NZD": "🇳🇿",  # Новозеландский доллар
        "NOK": "🇳🇴",  # Норвежская крона
        "RUB": "🇷🇺",  # Российский рубль
        "XDR": "🌐",  # СДР (Специальные права заимствования)
        "SGD": "🇸🇬",  # Сингапурский доллар
        "KGS": "🇰🇬",  # Киргизский сом
        "KZT": "🇰🇿",  # Казахстанский тенге
        "TRY": "🇹🇷",  # Турецкая лира
        "GBP": "🇬🇧",  # Фунт стерлингов
        "CZK": "🇨🇿",  # Чешская крона
        "SEK": "🇸🇪",  # Шведская крона
        "CHF": "🇨🇭"  # Швейцарский франк
    }
    return flags.get(currency, '')












# count = 0
# time_int=854146000
# while count < 10:
#     asyncio.run(add_db_date(time_int))
#     count += 1  # Увеличиваем значение count на 1 на каждой итерации
#     time_int= time_int - 86400



