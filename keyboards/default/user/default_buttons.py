from aiogram.types import ReplyKeyboardMarkup


def user_main_dkb():
    kb = ReplyKeyboardMarkup(resize_keyboard=True)
    kb.row("🏡 Bosh sahifa")
    return kb
