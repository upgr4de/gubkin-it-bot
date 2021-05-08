from aiogram.types import Message, ContentTypes
from aiogram.dispatcher.filters.builtin import CommandHelp
from loader import dp
from .start import commands_info, help_text
from aiogram.dispatcher import FSMContext
from data.config import ADMINS


@dp.message_handler(CommandHelp(), state = None)
async def bot_help(message: Message):
	await message.answer(help_text + '\n\n' + commands_info)


@dp.message_handler(state = None, content_types = ContentTypes.ANY)
async def bot_echo_none(message: Message):
    await message.answer(f'Я Вас не понимаю (\n\n{help_text}\n\n{commands_info}')


@dp.message_handler(state = '*', content_types = ContentTypes.ANY)
async def bot_echo_all(message: Message, state: FSMContext):
	state = await state.get_state()

	for admin in ADMINS:
		await dp.bot.send_message(admin, f'Что-то пошло не так... Состояние:\n<code>{state}</code>\n\n'
								  f'Сообщение:\n<code>{message}</code>')
	
	await message.answer(f'Что-то пошло не так... Состояние:\n<code>{state}</code>')
	await message.answer(f'{help_text}\n\n{commands_info}')
