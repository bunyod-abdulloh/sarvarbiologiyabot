from aiogram import types
from aiogram.dispatcher import FSMContext
from magic_filter import F

from filters.admins import IsBotAdminFilter
from handlers.admin.helpers import build_categories_text
from loader import dp, lesdb
from states.admin import AdminDeleteStates
from utils.helpers import number_text_alert


@dp.message_handler(IsBotAdminFilter(), F.text == "🗑 Kategoriya", state="*")
async def handle_delete_categories_main(message: types.Message, state: FSMContext):
    await state.finish()

    categories = await lesdb.get_lessons_categories()

    await message.answer(
        text=build_categories_text(categories) + "\nO'chirmoqchi bo'lgan kategoriya ID raqamini kiriting"
    )
    await AdminDeleteStates.FREE_CATEGORY.set()


@dp.message_handler(state=AdminDeleteStates.FREE_CATEGORY, content_types=['text'])
async def handle_delete_category_state(message: types.Message):
    if message.text.isdigit():
        category_id = int(message.text)
        check = await lesdb.check_category(category_id)

        if check:
            await lesdb.delete_category(category_id)
            await message.answer(
                text="O'chirildi!"
            )
            return
        else:
            await message.answer(text="Bu ID raqamli kategoriya yo'q!")
            return
    await number_text_alert(message)
