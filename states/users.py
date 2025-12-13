from aiogram.dispatcher.filters.state import StatesGroup, State


class UsersStates(StatesGroup):
    PHOTO = State()
    TEXT = State()
