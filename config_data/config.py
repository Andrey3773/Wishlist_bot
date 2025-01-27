from dataclasses import dataclass
from environs import Env

@dataclass
class TgBot:
    token: str
    admins: list

@dataclass
class Config:
    bot: TgBot

##### ЗАГРУЗКА КОНФИГУРАЦИИ БОТА В КОД #####
def load_config(path: str) -> Config:
    env = Env()
    env.read_env(path)
    return Config(
        bot=TgBot(
            token=env('BOT_TOKEN'),
            admins=list(map(int, env.list('ADMINS_ID')))
        )
    )
