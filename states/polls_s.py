from aiogram.dispatcher.filters.state import StatesGroup, State


class Poll(StatesGroup):
	questions = State()
