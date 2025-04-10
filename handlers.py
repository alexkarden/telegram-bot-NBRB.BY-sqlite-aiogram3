from aiogram import Router, F
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart, Command

from aiogram.types import Message, CallbackQuery
from keyboards import start_keyboard_inline, start_keyboard_reply,create_dynamic_keyboard_select
from script import add_user_db, all_kurs
from config import LONGLISTOFCURRENCY, SHORTLISTOFCURRENCY



router = Router()
@router.message(CommandStart())
async def cmd_start(message: Message):
    await add_user_db(message.from_user.id, message.from_user.first_name, message.from_user.last_name,message.from_user.username)
    await message.answer('👋 <b>Добро пожаловать! </b> \nЭтот бот отправляет курсы валют НБРБ ежедневно или по запросу. Давайте его настроим чтобы вам было удобно.\n\nЕсли Вы хотите получать курсы валют по запросу, то нажмите <b>"По запросу"</b>\nЕсли хотите настроить периодичность получения курсов, то нажмите <b>"Настройки"</b>\n\nВ любой момент Вы сможете изменить настройки.', reply_markup= start_keyboard_inline, parse_mode=ParseMode.HTML)


@router.message(Command('help'))
async def cmd_help(message: Message):
    await message.answer('Это команда /help',
            reply_markup=start_keyboard_reply, parse_mode=ParseMode.HTML)


@router.message(Command('about'))
async def cmd_about(message: Message):
    await message.answer('<b>Alex Karden</b>\nhttps://github.com/alexkarden',
            reply_markup=start_keyboard_reply, parse_mode=ParseMode.HTML)


@router.message(Command('alexkarden'))
async def cmd_alexkarden(message: Message):
    await message.answer('<b>Алексей\n<a href="tel:+375297047262">+375-29-704-72-62</a></b>',
            reply_markup=start_keyboard_reply, parse_mode=ParseMode.HTML)


@router.message()
async def all_message(message: Message):
    text = message.text
    if text =='⚙️ Настройки':
        await message.answer(f"Как часто вы хотите получать уведомления о курсах валют в течение дня?\n\n1 раз в день :(14:30)\n3 раза в день :(10:00, 12:30, 15:00)\n\nПри выборе появляется ✅\nДля отмены выбора еще раз нажмите на кнопку.",
            reply_markup=await create_dynamic_keyboard_select(message.from_user.id, 'none'), parse_mode='HTML')
    elif text == 'alexkarden':
        await message.answer('<b>Алексей\n<a href="tel:+375297047262">+375-29-704-72-62</a></b>',
            reply_markup=start_keyboard_reply, parse_mode='HTML')
    elif text == '💸 Курсы популярных валют':
        await message.answer(f'{await all_kurs(SHORTLISTOFCURRENCY)}',
            reply_markup=start_keyboard_reply, parse_mode='HTML')
    elif text == '📝 Все курсы':
        await message.answer(f'{await all_kurs(LONGLISTOFCURRENCY)}',
            reply_markup=start_keyboard_reply, parse_mode='HTML')

    else:
        await message.answer('Воспользуйтесь клавиатурой ниже:',
            reply_markup=start_keyboard_reply, parse_mode='HTML')


@router.callback_query()
async def callback_query(callback: CallbackQuery):
    # Получаем данные из обратного запроса
    data = callback.data
    # Обрабатываем данные
    if data == 'По запросу':
        await callback.answer()
        # Удаляем сообщение с клавиатурой
        await callback.message.delete()
        await callback.message.answer("Воспользуйтесь клавиатурой внизу", reply_markup=start_keyboard_reply)
    elif data == 'Настройки':
        await callback.answer()
        await callback.message.edit_text(f"Как часто вы хотите получать уведомления о курсах валют в течение дня?\n\n1 раз в день: (14:30)\n3 раза в день: (10:00, 12:30, 15:00)\n\nПри выборе появляется ✅\nДля отмены выбора еще раз нажмите на кнопку.", reply_markup=await create_dynamic_keyboard_select(callback.from_user.id, 'none'), parse_mode='HTML')
    elif data == '1 раз':
        await callback.answer()
        await callback.message.edit_text(f"Как часто вы хотите получать уведомления о курсах валют в течение дня?\n\n1 раз в день: (14:30)\n3 раза в день: (10:00, 12:30, 15:00)\n\nПри выборе появляется ✅\nДля отмены выбора еще раз нажмите на кнопку.", reply_markup= await create_dynamic_keyboard_select(callback.from_user.id, 'daily'), parse_mode='HTML')
    elif data == '3 раза':
        await callback.answer()
        await callback.message.edit_text(f"Как часто вы хотите получать уведомления о курсах валют в течение дня?\n\n1 раз в день: (14:30)\n3 раза в день: (10:00, 12:30, 15:00)\n\nПри выборе появляется ✅\nДля отмены выбора еще раз нажмите на кнопку.", reply_markup=await create_dynamic_keyboard_select(callback.from_user.id, 'thrice'), parse_mode='HTML')
    elif data == 'exit':
        # Удаляем сообщение с клавиатурой
        await callback.message.delete()
        await callback.message.answer(f"Воспользуйтесь клавиатурой внизу", reply_markup=start_keyboard_reply, parse_mode='HTML')


