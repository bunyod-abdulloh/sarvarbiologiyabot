from aiogram import types
from magic_filter import F

from loader import dp
from utils.helpers import is_subscribed


@dp.callback_query_handler(F.data == "subscribed")
async def subscribe_callback(call: types.CallbackQuery):
    if not await is_subscribed(call.from_user.id):
        await call.answer(
            text="Kanalimizga obuna bo'lishingiz lozim!",
            show_alert=True
        )
    else:
        text = "Biz bilan birga ekanligingizdan xursandmiz! Marhamat darslarimizdan foydalanishingiz mumkin!"
        await call.message.edit_text(text=text)
