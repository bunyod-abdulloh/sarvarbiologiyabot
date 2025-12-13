from aiogram import types
from aiogram.dispatcher import FSMContext
from magic_filter import F

from loader import dp, bot
from states.admin import AdminStates


@dp.callback_query_handler(F.data.startswith("cancel_"), state="*")
async def handle_user_cancel_message(call: types.CallbackQuery, state: FSMContext):
    telegram_id = call.data.split("_")[1]
    await state.update_data(
        user_telegram_id=telegram_id
    )
    await call.message.edit_text(
        text="Rad etilish sababini kiriting"
    )
    await AdminStates.CANCEL_MESSAGE.set()


@dp.message_handler(state=AdminStates.CANCEL_MESSAGE, content_types=types.ContentType.TEXT)
async def handle_cancel_message_second(message: types.Message, state: FSMContext):
    telegram_id = (await state.get_data()).get("user_telegram_id")
    text = f"So'rovingiz rad etildi! Admin xabari:\n\n{message.text}"

    try:
        await bot.send_message(
            chat_id=telegram_id,
            text=text
        )
    except Exception:
        pass

    await message.answer(
        text="Xabaringiz yetkazildi!"
    )
    await state.finish()


@dp.callback_query_handler(F.data.startswith("confirmation_"), state="*")
async def handle_user_cancel_message(call: types.CallbackQuery, state: FSMContext):
    telegram_id = call.data.split("_")[1]

    try:
        await bot.send_message(
            chat_id=telegram_id,
            text="To'lovingiz admin tomonidan tasdiqlandi! Marhamat darslarimizdan foydalanishingiz mumkin!",
            reply_markup=None
        )
        await call.message.edit_text(
            text="Tasdiq xabari foydalanuvchiga yuborildi!"
        )
    except Exception as err:
        await call.message.answer(
            text=f"XATOLIK:\n\n{err}"
        )
