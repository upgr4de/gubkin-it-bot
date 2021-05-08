import os

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from data.config import POLLS_PATH


menu = InlineKeyboardMarkup(
	inline_keyboard = [[
		InlineKeyboardButton(text = 'Загрузить', callback_data = 'download')
	],[
		InlineKeyboardButton(text = 'Удалить', callback_data = 'delete')
	],[
		InlineKeyboardButton(text = '❌ Отмена', callback_data = 'cancel')
	]]
)
