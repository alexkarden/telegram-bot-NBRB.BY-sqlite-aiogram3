from aiogram.types import KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup
from script import get_status_subscribed_user_db, subscribed_user_db

start_keyboard_inline = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="По запросу", callback_data='По запросу'), InlineKeyboardButton(text="⚙️ Настройки", callback_data='Настройки')]
    ])

start_keyboard_reply = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text="💸 Курсы популярных валют"), KeyboardButton(text="📝 Все курсы")],
    [KeyboardButton(text="⚙️ Меню")]
    ], resize_keyboard=True)


async def create_dynamic_keyboard_select(tgid, status):
    # Получаем статус подписки пользователя из базы данных
    is_subscribed = await get_status_subscribed_user_db(tgid)

    # Определение текста кнопок на основе статуса подписки
    subscription_button_text1 = 'Один раз в день'
    subscription_button_text3 = 'Три раза в день'



    if is_subscribed == 'daily':
        if status == 'thrice':
            subscription_button_text1 = 'Один раз в день'
            subscription_button_text3 = '✅ Три раза в день'
            await subscribed_user_db(tgid, 'thrice')
        elif status == 'none':
            subscription_button_text1 = '✅ Один раз в день'
            subscription_button_text3 = 'Три раза в день'
        elif status == 'daily':
            subscription_button_text1 = 'Один раз в день'
            subscription_button_text3 = 'Три раза в день'
            await subscribed_user_db(tgid, 'none')
    elif is_subscribed == 'thrice':
        if status == 'daily':
            subscription_button_text1 = '✅ Один раз в день'
            subscription_button_text3 = 'Три раза в день'
            await subscribed_user_db(tgid, 'daily')
        elif status == 'none':
            subscription_button_text1 = 'Один раз в день'
            subscription_button_text3 = '✅ Три раза в день'
        elif status == 'thrice':
            subscription_button_text1 = 'Один раз в день'
            subscription_button_text3 = 'Три раза в день'
            await subscribed_user_db(tgid, 'none')

    elif is_subscribed == 'none':
        if status == 'daily':
            subscription_button_text1 = '✅ Один раз в день'
            subscription_button_text3 = 'Три раза в день'
            await subscribed_user_db(tgid, 'daily')
        elif status == 'thrice':
            subscription_button_text1 = 'Один раз в день'
            subscription_button_text3 = '✅ Три раза в день'
            await subscribed_user_db(tgid, 'thrice')
        elif status == 'none':
            subscription_button_text1 = 'Один раз в день'
            subscription_button_text3 = 'Три раза в день'

    else:
        await subscribed_user_db(tgid, 'none')

    # Создание динамической клавиатуры с учетом статуса подписки
    dynamic_keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=subscription_button_text1, callback_data='1 раз')],
        [InlineKeyboardButton(text=subscription_button_text3, callback_data='3 раза')],
        [InlineKeyboardButton(text='Помощь', callback_data='help')],
        [InlineKeyboardButton(text='🔙 Выйти из Меню', callback_data='exit')]
    ])

    return dynamic_keyboard
