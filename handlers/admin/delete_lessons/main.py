from aiogram import types
from aiogram.dispatcher import FSMContext
from magic_filter import F

from filters.admins import IsBotAdminFilter
from keyboards.default.admin.main import admin_delete_dkb
from loader import dp


@dp.message_handler(IsBotAdminFilter(), F.text == "🗑 Dars o'chirish", state="*")
async def admin_delete_main(message: types.Message, state: FSMContext):
    await state.finish()
    await message.answer(text=message.text, reply_markup=admin_delete_dkb())
