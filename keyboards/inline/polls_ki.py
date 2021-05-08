import os

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from data.config import POLLS_PATH


def create_polls(group):
	polls = InlineKeyboardMarkup(row_width = 1)

	for poll_file in os.listdir(POLLS_PATH):
		if poll_file.endswith('.json') and not(poll_file.startswith('contact')):
			poll_name = poll_file.split('.')[0]
			poll_btn = InlineKeyboardButton(text = poll_name, callback_data = f'pl:{poll_name}:{group}')

			polls.insert(poll_btn)

	poll_btn = InlineKeyboardButton(text = '❌ Отмена', callback_data = 'cancel')

	polls.insert(poll_btn)

	return polls
