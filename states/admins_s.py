from aiogram.dispatcher.filters.state import StatesGroup, State


class Downloading(StatesGroup):
	question = State()
