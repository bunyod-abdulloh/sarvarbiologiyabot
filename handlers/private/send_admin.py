from aiogram import types
from aiogram.dispatcher import FSMContext
from magic_filter import F

from data.config import ADMINS
from keyboards.inline.user.main import image_or_text_ibtn
from loader import dp
from states.users import UsersStates
from utils.helpers import send_to_admin


@dp.callback_query_handler(F.data == "send_to_admin", state="*")
async def handle_send_to_admin_main(call: types.CallbackQuery, state: FSMContext):
    await state.finish()

    await call.message.edit_text(
        text=(
            "Faqat to'lov cheki rasmi yoki matnli xabarlar qabul qilinadi!\n\n"
            "Qaysi turdagi xabarni yubormoqchisiz?"
        ),
        reply_markup=image_or_text_ibtn()
    )


@dp.callback_query_handler(F.data == "purchase_receipt", state="*")
async def handle_purchase_receipt(call: types.CallbackQuery):
    await call.answer(text="Bo'lim hozircha ishlamayapti!", show_alert=True)

    # await call.message.edit_text(
    #     text="Chek rasmini yuboring\n\n(faqat rasm! Fayl ko'rinishida bo'lmasin)"
    # )
    # await UsersStates.PHOTO.set()


@dp.message_handler(state=UsersStates.PHOTO, content_types=types.ContentType.PHOTO)
async def handle_chek_photo(message: types.Message, state: FSMContext):
    file_id = message.photo[-1].file_id
    telegram_id = message.from_user.id

    await send_to_admin(
        admin_id=ADMINS[1],
        content=file_id,
        telegram_id=telegram_id,
        is_photo=True
    )

    await message.answer("Xabaringiz adminga yuborildi! Tez orada javob qaytaramiz!")
    await state.finish()


@dp.callback_query_handler(F.data == "text_message", state="*")
async def handle_text_message_main(call: types.CallbackQuery):
    await call.message.edit_text("Xabaringizni kiriting")
    await UsersStates.TEXT.set()


@dp.message_handler(state=UsersStates.TEXT, content_types=types.ContentType.TEXT)
async def handle_text_message_second(message: types.Message, state: FSMContext):
    text = message.text
    telegram_id = message.from_user.id

    await send_to_admin(
        admin_id=ADMINS[1],
        content=text,
        telegram_id=telegram_id,
        is_photo=False
    )

    await message.answer("Xabaringiz adminga yuborildi! Tez orada javob qaytaramiz!")
    await state.finish()
