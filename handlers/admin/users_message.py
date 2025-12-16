from aiogram import types
from aiogram.dispatcher import FSMContext

from keyboards.inline.admin.callbacks import check_cancel_cb, answer_cb
from loader import dp, bot, pdb
from states.admin import AdminStates


@dp.callback_query_handler(check_cancel_cb.filter(action="cancel"), state="*")
async def handle_user_cancel_message(call: types.CallbackQuery, state: FSMContext, callback_data: dict):
    telegram_id = callback_data.get("value")
    await state.update_data(
        user_telegram_id=telegram_id
    )
    await call.answer(cache_time=0)
    await call.message.answer(
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


@dp.callback_query_handler(check_cancel_cb.filter(action="confirmation"), state="*")
async def handle_user_cancel_message(call: types.CallbackQuery, callback_data: dict):
    telegram_id = int(callback_data.get("value"))

    try:
        await bot.send_message(
            chat_id=telegram_id,
            text="To'lovingiz admin tomonidan tasdiqlandi! Darslarimizdan foydalanishingiz mumkin!",
            reply_markup=None
        )
        await pdb.add_to_paid_users(telegram_id)
        await call.answer(cache_time=0)
        await call.message.answer(
            text="Tasdiq xabari foydalanuvchiga yuborildi!"
        )
    except Exception as err:
        await call.message.answer(
            text=f"XATOLIK:\n\n{err}"
        )


@dp.callback_query_handler(answer_cb.filter(action="answer"), state="*")
async def handle_send_answer(call: types.CallbackQuery, callback_data: dict, state: FSMContext):
    telegram_id = callback_data.get("value")
    await state.update_data(user_telegram=telegram_id)
    await call.message.answer(
        text="Javob xabaringizni kiriting"
    )
    await AdminStates.ANSWER_MESSAGE.set()


@dp.message_handler(state=AdminStates.ANSWER_MESSAGE, content_types=types.ContentType.TEXT)
async def handle_answer_text_message(message: types.Message, state: FSMContext):
    telegram_id = (await state.get_data()).get("user_telegram")

    try:
        await bot.send_message(
            chat_id=telegram_id,
            text=f"Savolingizga admin javobi:\n\n{message.text}"
        )
        await message.answer(
            text="Xabar foydalanuvchiga yuborildi!"
        )
    except Exception as err:
        await message.answer(
            text=f"Xatolik:\n\n{err}"
        )
    await state.finish()
