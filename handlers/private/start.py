import asyncpg.exceptions
from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import CommandStart

from keyboards.inline.user.ibuttons import main_page_ibtn
from loader import dp, udb


@dp.message_handler(CommandStart(), state="*")
async def bot_start(message: types.Message, state: FSMContext):
    await state.finish()

    try:
        await udb.add_user(telegram_id=message.from_user.id)
    except asyncpg.exceptions.UniqueViolationError:
        pass

    await message.answer(
        text="Assalomu alaykum!\n\nBotimizga xush kelibsiz!\n\nKerakli bo'limni tanlang",
        reply_markup=main_page_ibtn()
    )
