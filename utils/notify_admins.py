import logging

from aiogram import Dispatcher
from data.config import ADMINS


async def notify(dp: Dispatcher, flag):
    for admin in ADMINS:
        try:
            if flag:
                await dp.bot.send_message(admin, "Бот запущен")
            else:
                await dp.bot.send_message(admin, "Бот остановлен")

        except Exception as err:
            logging.exception(err)
