import asyncpg.exceptions
from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import CommandStart
from magic_filter import F

from keyboards.default.user.default_buttons import user_main_dkb
from keyboards.inline.user.ibuttons import main_page_ibtn
from loader import dp, udb
from utils.helpers import is_subscribed


@dp.message_handler(CommandStart(), state="*")
async def bot_start(message: types.Message, state: FSMContext):
    await state.finish()

    try:
        await udb.add_user(telegram_id=message.from_user.id)
    except asyncpg.exceptions.UniqueViolationError:
        pass

    await message.answer(
        text="Assalomu alaykum!\n\nBotimizga xush kelibsiz!",
        reply_markup=user_main_dkb()
    )
    await message.answer(
        text="Kerakli bo'limni tanlang", reply_markup=main_page_ibtn()
    )


@dp.message_handler(F.text == "🏡 Bosh sahifa", state="*")
async def handle_main_page(message: types.Message, state: FSMContext):
    await state.finish()

    if await is_subscribed(message.from_user.id):
        await bot_start(message, state)
    else:
        await message.answer(
            text="Botdan to'liq foydalanish uchun kanalimizga a'zo bo'ling!"
        )
