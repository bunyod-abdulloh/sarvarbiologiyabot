from aiogram.dispatcher.handler import CancelHandler
from aiogram.dispatcher.middlewares import BaseMiddleware
from aiogram import types

from keyboards.inline.user.main import subscribe_ibtn
from utils.helpers import is_subscribed

class SubscriptionMiddleware(BaseMiddleware):
    async def on_pre_process_message(self, message: types.Message, data: dict):
        if not await is_subscribed(message.from_user.id):
            await message.answer(
                text="❗ Botdan foydalanish uchun kanalga a'zo bo‘ling.",
                reply_markup=await subscribe_ibtn()
            )
            raise CancelHandler()
