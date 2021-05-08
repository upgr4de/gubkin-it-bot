import os

from aiogram.types import Message, CallbackQuery
from aiogram.dispatcher.filters import Command, Filter
from loader import dp
from data.config import ADMINS, POLLS_PATH, INCORRECT_INPUT
from keyboards.inline.admins_ki import menu
from keyboards.inline.polls_ki import  create_polls
from keyboards.inline.callback_data import poll_callback
from states.admins_s import Downloading
from aiogram.dispatcher import FSMContext
from google_forms.read_write import read_form


@dp.message_handler(Command('admins'), state = None)
async def detect_admins(message: Message):
	if str(message.from_user.id) in ADMINS:
		await message.answer('Выберите действие для опросов', 
							 reply_markup = menu)
		

@dp.callback_query_handler(text = 'download', state = None)
async def load_poll(call: CallbackQuery):
	await call.answer(cache_time = 60)
	await call.message.answer('Введите ссылку на Google форму вида https:...edit')
	await Downloading.question.set()


@dp.message_handler(state = Downloading.question)
async def get_answers(message: Message, state: FSMContext):
	form_url = message.text

	if not(form_url.startswith('https://docs.google.com/forms/') and form_url.endswith('/edit')):
		await message.answer(INCORRECT_INPUT)

		return

	await message.answer('Пожалуйста подождите...')

	result, error = read_form(form_url)
	
	if result:
		await message.answer('Форма загружена')
	else:
		await message.answer(f'❗️ Произошла ошибка:\n<code>{error}</code>')

	await state.reset_state()


@dp.callback_query_handler(text = 'delete', state = None)
async def show_polls(call: CallbackQuery):
	await call.answer(cache_time = 60)
	await call.message.answer('Выберите опрос для удаления', 
							  reply_markup = create_polls('del'))


@dp.callback_query_handler(poll_callback.filter(gr = 'del'), state = None)
async def remove_poll(call: CallbackQuery, callback_data: dict):
	await call.answer(cache_time = 60)
	poll_name = callback_data.get('nm')
	os.remove(f'{POLLS_PATH}{poll_name}.json')
	await call.message.edit_reply_markup(reply_markup = None)
	await call.message.answer('Опрос удален')
