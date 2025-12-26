from aiogram import types
from aiogram.dispatcher import FSMContext
from magic_filter import F

from loader import dp


@dp.callback_query_handler(F.data == "paid_lessons", state="*")
async def user_paid_lessons_start(call: types.CallbackQuery, state: FSMContext):
    await state.finish()
    await call.answer(text="Bo'lim ishga tushmadi!", show_alert=True)
