import asyncio
from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

from config_reader import config

from src.ather.data_session_collector import DataSessionCollector
from src.handlers import main_handler, random_fact_handler, quiz_handler, talk_gpt_handler, talk_fp_gpt_handler, dictionary_handler, job_handler


async def main():
    bot = Bot(token = config.bot_token.get_secret_value(), default= DefaultBotProperties(parse_mode= ParseMode.MARKDOWN_V2))
    dp = Dispatcher()
    data_session_collector = DataSessionCollector()  # вспомогательная сущность для хранения данных сеанса

    dp.include_router(main_handler.router)
    dp.include_router(random_fact_handler.router)
    dp.include_router(quiz_handler.router)
    dp.include_router(talk_gpt_handler.router)
    dp.include_router(talk_fp_gpt_handler.router)
    dp.include_router(job_handler.router)
    dp.include_router(dictionary_handler.router)

    await dp.start_polling(bot, data_session_collector = data_session_collector)


if __name__ == '__main__':
    asyncio.run(main())
