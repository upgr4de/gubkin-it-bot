from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandStart
from loader import dp


help_text = "Если у Вас возникли вопросы, или Вы обнаружили ошибку/проблему при использовании бота, свяжитесь с @emilaflatunov"
commands_info = ('Список команд:\n'
				 '/help - справка\n'
				 '/polls - список опросов\n'
				 '/contact - связаться с нами\n'
				 '/cancel - отмена\n')


@dp.message_handler(CommandStart(), state = None)
async def bot_start(message: types.Message):
	await message.answer(f'Рад Вас видеть, {message.from_user.full_name}, начнем!\n\n' + commands_info)
