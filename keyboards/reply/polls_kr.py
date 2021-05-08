from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


command_texts = ['Отлично! Начать', 'Пропустить', 'Завершить']


def create_command(command_text):
	command = ReplyKeyboardMarkup(
		keyboard = [[
			KeyboardButton(text = command_text)
		]],
		resize_keyboard = True
	)

	return command


def create_choices(choices_count, required):
	choices = ReplyKeyboardMarkup(resize_keyboard = True, row_width = 2)

	for i in range(choices_count):
		choices_btn = KeyboardButton(text = f'{i + 1}')
		choices.insert(choices_btn)
	
	if not(required):
		skip_btn = KeyboardButton(text = command_texts[1])
		choices.insert(skip_btn)
	
	return choices
