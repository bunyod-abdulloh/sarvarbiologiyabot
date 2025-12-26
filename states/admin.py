from aiogram.dispatcher.filters.state import StatesGroup, State


class AdminStates(StatesGroup):
    SEND_MEDIA_TO_USERS = State()
    SEND_TO_USERS = State()
    CANCEL_MESSAGE = State()
    ANSWER_MESSAGE = State()
    FREE_CATEGORY = State()
    FREE_SUBCATEGORY = State()
    FREE_LESSONS_ONE = State()
    FREE_LESSONS_TWO = State()
    FREE_LESSONS_THREE = State()
    FREE_LESSONS_FOUR = State()
    FREE_LESSONS_FIVE = State()


class EditStates(StatesGroup):
    FREE_CATEGORY_ONE = State()
    FREE_CATEGORY_TWO = State()
    FREE_SUBCATEGORY_ONE = State()
    FREE_SUBCATEGORY_TWO = State()
    FREE_SUBCATEGORY_THREE = State()
    FREE_LESSON_ONE = State()
    FREE_LESSON_TWO = State()
    FREE_LESSON_THREE = State()
    FREE_LESSON_FOUR = State()
    FREE_LESSON_FIVE = State()


class AdminDeleteStates(StatesGroup):
    FREE_CATEGORY = State()
    FREE_SUBCATEGORY_ONE = State()
    FREE_SUBCATEGORY_TWO = State()
    FREE_LESSON_ONE = State()
    FREE_LESSON_TWO = State()
    FREE_LESSON_THREE = State()
