from copy import deepcopy

from aiogram import Router
from aiogram.filters import Command, CommandStart, Text
from aiogram.types import CallbackQuery, Message
from database.database import user_dict_template, user_db
from filters.filters import IsDelBookmarkCallbackData, IsDigitCallbackData
from keyboards.bookmarks_kb import (create_bookmarks_keyboard,
                                    create_edit_keyboard)
from keyboards.pagination_kb import createe_pagination_keyboard
from lexicon.lexicon import LEXICON
from services.file_handling import book

router: Router = Router()


# Цей хендлер буде спрацьовувати на команду "/start" -
# додавати користувача в базу даних, якщо його там ще не було
# і надсилати йому вітальне повідомлення
@router.message(CommandStart())
async def process_start_command(mesage: Message):
    await mesage.answer(LEXICON['/start'])
    if mesage.from_user.id not in user_db:
        user_db[mesage.from_user.id] = deepcopy(user_dict_template)


# Цей хендлер спрацьовуватиме на команду "/help"
# і надсилатиме користувачеві повідомлення зі списком доступних команд у боті
@router.message(Command(commands=['help']))
async def process_help_command(message: Message):
    await message.answer(LEXICON['/help'])


# Цей хендлер спрацьовуватиме на команду "/beginning"
# і відправляти користувачеві першу сторінку книги з кнопками пагінації
@router.message(Command(commands=['beginning']))
async def process_beginning_command(message: Message):
    user_db[message.from_user.id]['page'] = 1
    text = book[user_db[message.from_user.id]['page']]
    await message.answer(
        text=text,
        reply_markup=createe_pagination_keyboard(
            'backward',
            f'{user_db[message.from_user.id]["page"]}/{len(book)}',
            'forward'))


# Цей хендлер спрацьовуватиме на команду "/continue"
# і відправляти користувачеві сторінку книги, на якій користувач
# зупинився в процесі взаємодії з ботом
@router.message(Command(commands=['continue']))
async def process_continue_command(message: Message):
    text = book[user_db[message.from_user.id]['page']]
    await message.answer(
        text=text,
        reply_markup=createe_pagination_keyboard(
            'backward',
            f'{user_db[message.from_user.id]["page"]}/{len((book))}',
            'forward'))


# Цей хендлер спрацьовуватиме на команду "/bookmarks"
# і надсилатиме користувачеві список збережених закладок,
# якщо вони є або повідомлення про те, що закладок немає
@router.message(Command(commands=['bookmarks']))
async def process_bookmarks_command(message: Message):
    if user_db[message.from_user.id]["bookmarks"]:
        await message.answer(
            text=LEXICON[message.text],
            reply_markup=create_bookmarks_keyboard(
                *user_db[message.from_user.id]["bookmarks"]))
    else:
        await message.answer(text=LEXICON['no_bookmarks'])


# Цей хендлер буде спрацьовувати на натискання інлайн-кнопки "вперед"
# під час взаємодії користувача з повідомленням-книгою
@router.callback_query(Text(text='forward'))
async def process_forward_press(callback: CallbackQuery):
    if user_db[callback.from_user.id]['page'] < len(book):
        user_db[callback.from_user.id]['page'] += 1
        text = book[user_db[callback.from_user.id]['page']]
        await callback.message.edit_text(
            text=text,
            reply_markup=createe_pagination_keyboard(
                'backward',
                f'{user_db[callback.from_user.id]["page"]}/{len(book)}',
                'forward'))
    await callback.answer()


# Цей хендлер буде спрацьовувати на натискання інлайн-кнопки "назад"
# під час взаємодії користувача з повідомленням-книгою
@router.callback_query(Text(text='backward'))
async def process_backward_press(callback: CallbackQuery):
    if user_db[callback.from_user.id]['page'] > 1:
        user_db[callback.from_user.id]['page'] -= 1
        text = book[user_db[callback.from_user.id]['page']]
        await callback.message.edit_text(
            text=text,
            reply_markup=createe_pagination_keyboard(
                'backward',
                f'{user_db[callback.from_user.id]["page"]}/{len(book)}',
                'forward'))
    await callback.answer()


# Цей хендлер спрацьовуватиме на натискання інлайн-кнопки
# з номером поточної сторінки і додаватиме поточну сторінку в закладки
@router.callback_query(lambda x: '/' in x.data and x.data.replace('/', '').isdigit())
async def process_page_press(callback: CallbackQuery):
    user_db[callback.from_user.id]['bookmarks'].add(
        user_db[callback.from_user.id]['page'])
    await callback.answer('Сторінку додано в закладки!')


# Цей хендлер спрацьовуватиме на натискання інлайн-кнопки
# із закладкою зі списку закладок
@router.callback_query(IsDigitCallbackData())
async def process_bookmark_press(callback: CallbackQuery):
    text = book[int(callback.data)]
    user_db[callback.from_user.id]['page'] = int(callback.data)
    await callback.message.edit_text(
        text=text,
        reply_markup=createe_pagination_keyboard(
            'backward',
            f'{user_db[callback.from_user.id]["page"]}/{len(book)}',
            'forward'))
    await callback.answer()


# Цей хендлер буде спрацьовувати на натискання інлайн-кнопки
# "редагувати" під списком закладок
@router.callback_query(Text(text='edit_bookmarks'))
async def process_edit_press(callback: CallbackQuery):
    await callback.message.edit_text(
        text=LEXICON[callback.data],
        reply_markup=create_edit_keyboard(
            *user_db[callback.from_user.id]["bookmarks"]))
    await callback.answer()


# Цей хендлер буде спрацьовувати на натискання інлайн-кнопки
# "скасувати" під час роботи зі списком закладок (перегляд і редагування)
@router.callback_query(Text(text='cancel'))
async def process_cancel_press(callback: CallbackQuery):
    await callback.message.edit_text(text=LEXICON['cancel_text'])
    await callback.answer()


# Цей хендлер буде спрацьовувати на натискання інлайн-кнопки
# із закладкою зі списку закладок до видалення
@router.callback_query(IsDelBookmarkCallbackData())
async def process_del_bookmark_press(calback: CallbackQuery):
    user_db[calback.from_user.id]['bookmarks'].remove(int(calback.data[:-3]))
    if user_db[calback.from_user.id]['bookmarks']:
        await calback.message.edit_text(
            text=LEXICON['/bookmarks'],
            reply_markup=create_edit_keyboard(
                *user_db[calback.from_user.id]["bookmarks"]))
    else:
        await calback.message.edit_text(text=LEXICON['no_bookmarks'])
    await calback.answer()
