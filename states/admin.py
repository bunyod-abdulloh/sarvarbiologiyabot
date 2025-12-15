from aiogram.dispatcher.filters.state import StatesGroup, State


class AdminStates(StatesGroup):
    SEND_MEDIA_TO_USERS = State()
    SEND_TO_USERS = State()
    CANCEL_MESSAGE = State()
    ANSWER_MESSAGE = State()
    CATEGORY = State()
    PAID_LESSONS_ONE = State()
    PAID_LESSONS_TWO = State()
    FREE_CATEGORY = State()
    FREE_LESSONS_ONE = State()
    FREE_LESSONS_TWO = State()
