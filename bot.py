import asyncio
import logging

from aiogram import Bot, Dispatcher
from config_data.config import Config, load_config
from handlers import other_handlers, user_handlers
from keyboards.main_menu import set_main_menu

# Ініціалізуєм логер
logger = logging.getLogger(__name__)


# Функція конфігуріровання і запуску бота
async def main():
    # Конфігуріруєм логування
    logging.basicConfig(
        level=logging.INFO,
        format='%(filename)s:%(lineno)d #%(levelname)-8s '
               '[%(asctime)s] - %(name)s - %(message)s')

    # Виводим в консоль інформацію про початок запуску бота
    logger.info('Starting bot')

    # Загружаєм конфіг в змінну config
    config: Config = load_config()

    # Ініціалізуєм бот і диспетчер
    bot: Bot = Bot(token=config.tg_bot.token,
                   parse_mode='HTML')
    dp: Dispatcher = Dispatcher()

    # Налаштовуєм головне меню бота
    await set_main_menu(bot)

    # Реєструєм роутери в диспетчері
    dp.include_router(user_handlers.router)
    dp.include_router(other_handlers.router)

    # Пропускаєм накопичені апдейти і запускаєм polling
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())
