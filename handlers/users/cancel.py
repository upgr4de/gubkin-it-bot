from aiogram.types import Message, ReplyKeyboardRemove, CallbackQuery
from aiogram.dispatcher.filters import Command
from loader import dp
from .start import commands_info
from aiogram.dispatcher import FSMContext


@dp.message_handler(Command('cancel'), state = None)
async def bot_cancel_none(message: Message):
	await message.answer('Нет действия для отмены\n\n' + commands_info)


@dp.message_handler(Command('cancel'), state = '*')
async def bot_cancel_state(message: Message, state: FSMContext):
	await state.reset_state()
	await message.answer('Действие отменено. Что еще я могу сделать для Вас?\n\n' + commands_info, 
						reply_markup = ReplyKeyboardRemove())


@dp.callback_query_handler(text = "cancel", state = None)
async def cancel_buying(call: CallbackQuery):
    await call.message.answer("Вы отменили выбор")

    await call.message.edit_reply_markup(reply_markup = None)
