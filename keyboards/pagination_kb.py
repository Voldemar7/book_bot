from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder
from lexicon.lexicon import LEXICON


# Функція, яка генерує клавіатуру для сторінки книги
def createe_pagination_keyboard(*buttons: str) -> InlineKeyboardMarkup:
    # Ініціалізуєм білдер
    kb_builder: InlineKeyboardBuilder = InlineKeyboardBuilder()
    # Добавляєм в білдер ряд з кнопками
    kb_builder.row(*[InlineKeyboardButton(
        text=LEXICON[button] if button in LEXICON else button,
        callback_data=button) for button in buttons])
    # Повертаєм обєкт інлайн клавіатури
    return kb_builder.as_markup()
