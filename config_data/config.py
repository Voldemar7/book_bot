from dataclasses import dataclass

from environs import Env


@dataclass
class TgBot:
    token: str  # токен для доступа до телеграм бота
    admin_ids: list[int]  # список ID адміністраторів бота


@dataclass
class Config:
    tg_bot: TgBot


# Створюєм функцію, яка буде зчитувати файл .env і повертати
#екземпляр класса Config з заповненими полями token і admin_ids
def load_config(path: str | None = None) -> Config:
    env = Env()
    env.read_env(path)
    return Config(tg_bot=TgBot(
        token=env('BOT_TOKEN'),
        admin_ids=list(map(int, env.list('ADMIN_IDS')))))
