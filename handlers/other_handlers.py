from aiogram import Router
from aiogram.types import Message

router: Router = Router()


# Цей хендлер буде реагувати на любі повідомлення користувача,
# не передбачені логікою бота
@router.message()
async def send_echo(message: Message):
    await message.answer(f"Вибачте, але я не розумію команди {message.text}. Будь ласка, спробуйте ще раз або скористайтесь командою /help для отримання додаткової інформації про доступні команди.")