import middlewares, filters, handlers

from aiogram import executor
from loader import dp
from utils.notify_admins import notify


async def on_startup(dispatcher):
    await notify(dispatcher, True)


async def on_shutdown(dispatcher):
    await notify(dispatcher, False)





if __name__ == '__main__':
    executor.start_polling(dp, on_startup = on_startup, on_shutdown = on_shutdown)
