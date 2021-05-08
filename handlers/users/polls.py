import json

from loader import dp
from aiogram.dispatcher.filters import Command
from keyboards.inline.polls_ki import create_polls
from aiogram.types import Message, CallbackQuery, ReplyKeyboardRemove
from keyboards.inline.callback_data import poll_callback
from aiogram.dispatcher import FSMContext
from states.polls_s import Poll
from aiogram.dispatcher.filters.state import State
from keyboards.reply.polls_kr import create_choices, create_command, command_texts
from data.config import POLLS_PATH, INCORRECT_INPUT, ADMINS
from google_forms.read_write import write_form
from .start import commands_info, help_text


async def fill_data(poll_name, message, state):
	with open(f'{POLLS_PATH}{poll_name}.json', 'r') as poll_file:
		await state.update_data({
			'poll_data': json.load(poll_file),
			'answers': {},
			'i': -1,
			'j': -1
		})

	await message.answer('🔔 Перед завершением, вы сможете менять ответы, редактируя сообщения', 
						 reply_markup = create_command(command_texts[0]))
	await Poll.questions.set()


async def get_answer(data, poll_data, i, j, message, state):
	answer = message.text
	item_type = poll_data['items'][j]['type']
	required = poll_data['items'][j]['isRequired']

	if not(required) and answer == command_texts[1]:
		if item_type == 'CHECKBOX':
			answer = []
		else:
			answer = ''
	elif item_type == 'CHECKBOX' or item_type == 'LIST' or item_type == 'MULTIPLE_CHOICE':
			choices_list = poll_data['items'][j]['choices']

			if item_type == 'CHECKBOX':
				answer_list = answer.split(' ')
				answer = []

				for k in answer_list:
					if k.isdigit() and len(k) == 1 and int(k) > 0 and int(k) <= len(choices_list):
						answer.append(choices_list[int(k) - 1])
					else:
						await message.answer(INCORRECT_INPUT)

						return False
			else:
				if answer.isdigit() and len(answer) == 1 and int(answer) > 0 and int(answer) <= len(choices_list):
					answer = choices_list[int(answer) - 1]
				else:
					await message.answer(INCORRECT_INPUT)

					return False

	data['answers'].update({
		message.message_id: {
			'answer': answer, 
			'i': i, 
			'j': j
		}
	})

	await state.update_data(data)

	return True


@dp.message_handler(Command('contact'), state = None)
async def contact(message: Message, state: FSMContext):
	await fill_data('contact', message, state)


@dp.message_handler(Command('polls'), state = None)
async def show_polls(message: Message):
	await message.answer('Выберите опрос', 
						 reply_markup = create_polls('take'))


@dp.callback_query_handler(poll_callback.filter(gr = 'take'), state = None)
async def choose_poll(call: CallbackQuery, callback_data: dict, state: FSMContext):
	await call.answer(cache_time = 60)
	await fill_data(callback_data.get('nm'), call.message, state)


@dp.message_handler(state = Poll.questions)
async def get_answers(message: Message, state: FSMContext):
	data = await state.get_data()
	poll_data, i, j = data['poll_data'], data['i'], data['j']
	items_count = poll_data['metadata']['count']

	if i == -1:
		if message.text != command_texts[0]:
			await message.answer(INCORRECT_INPUT)

			return

		item_title = poll_data['metadata']['title']
		item_help = poll_data['metadata']['description']
		item_head = item_title + '\n' + item_help if item_help else item_title
		required_legend = ''

		for k in range(items_count):
			if poll_data['items'][k].get('isRequired') != None:
				if poll_data['items'][k]['isRequired']:
					required_legend = 'Поле с 📍 обязательное'

					break

		await message.answer(item_head + '\n\n' + required_legend, 
							 reply_markup = ReplyKeyboardRemove())
	else:
		if j == items_count:
			if message.text != command_texts[2]:
				await message.answer(INCORRECT_INPUT)

				return

			form_url = poll_data['metadata']['editUrl']
			answers = []

			[answers.append(dict['answer']) for dict in list(data['answers'].values())]
			
			await message.answer('Пожалуйста подождите...')

			result, error =  write_form(form_url, answers)
	
			if result:
				await message.answer('Ответы приняты', 
									 reply_markup = ReplyKeyboardRemove())
			else:
				for admin in ADMINS:
					await dp.bot.send_message(admin, f'❗️ Произошла ошибка:\n<code>{error}</code>\n\n'
											  f'Сообщение:\n<code>{message}</code>\n\n')
				
				form_url = poll_data['metadata']['publishedUrl']

				await message.answer(f'❗️ Произошла ошибка:\n<code>{error}</code>\n\n'
									 f'Вы можете перейти по ссылке:\n{form_url}\n'
									 f'и проставить свои ответы по порядку:\n<code>{answers}</code>\n'
									 'Приносим свои извинения')
				await message.answer(f'{help_text}\n\n{commands_info}')
			
			await state.reset_state()

			return

		if not(await get_answer(data, poll_data, i, j, message, state)):
			return

		if j == items_count - 1:
			j += 1

			await message.answer('🔔 Перед завершением, вы можете изменить ответы, редактируя сообщения', 
								 reply_markup = create_command(command_texts[2]))
			await state.update_data(j = j)

			return

		setattr(Poll(), f'questions', State(f'questions', 'Poll'))

	while j < items_count - 1:
		j += 1
		item_type = poll_data['items'][j]['type']
		item_title = poll_data['items'][j]['title']
		item_help = poll_data['items'][j]['helpText']
		item_head = item_title + '\n' + item_help if item_help else item_title

		if item_type == 'SECTION_HEADER':
			await message.answer(item_head)
		else:
			i += 1
			options = ''
			comment = ''
			required = poll_data['items'][j]['isRequired']

			if required:
				item_title += ' 📍'
				item_head = item_title + '\n' + item_help if item_help else item_title
				reply_kbd = ReplyKeyboardRemove()
			else:
				reply_kbd = create_command(command_texts[1])

			if item_type == 'PARAGRAPH_TEXT':
				comment = 'Дайте развернутый ответ'
			elif item_type == 'LIST' or item_type == 'MULTIPLE_CHOICE' or item_type == 'CHECKBOX':
				choices_list = poll_data['items'][j]['choices']
				
				for choice in choices_list:
					options += f'  {choices_list.index(choice) + 1}) {choice}\n'

				options += '\n'

				if item_type == 'CHECKBOX':
					comment = 'Введите один или несколько вариантов цифрами через пробел'
				else:
					comment = 'Выберите один вариант'
				
					reply_kbd = create_choices(len(choices_list), required)

			await message.answer(f'{i + 1}. {item_head}\n\n{options}{comment}', 
								 reply_markup = reply_kbd)

			break

	await state.update_data(i = i, j = j)


@dp.edited_message_handler(state = Poll.questions)
async def edit_answers(message: Message, state: FSMContext):
	data = await state.get_data()
	poll_data = data['poll_data']
	i, j = data['answers'][message.message_id]['i'], data['answers'][message.message_id]['j']

	if not(await get_answer(data, poll_data, i, j, message, state)):
		await message.answer('Ответ не примет изменений')

		return
