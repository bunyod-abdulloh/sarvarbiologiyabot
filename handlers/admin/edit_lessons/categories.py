from aiogram import types
from aiogram.dispatcher import FSMContext
from magic_filter import F

from filters.admins import IsBotAdminFilter
from handlers.admin.helpers import build_categories_text
from loader import dp, lesdb
from states.admin import EditStates
from utils.helpers import number_text_alert


@dp.message_handler(IsBotAdminFilter(), F.text == "♻️ Kategoriya", state="*")
async def handle_edit_categories(message: types.Message, state: FSMContext):
    await state.finish()

    categories = await lesdb.get_lessons_categories()

    await message.answer(
        text=build_categories_text(categories) + "\nO'zgartirmoqchi bo'lgan kategoriyangizni ID raqamini kiriting"
    )
    await EditStates.FREE_CATEGORY_ONE.set()


@dp.message_handler(state=EditStates.FREE_CATEGORY_ONE, content_types=['text'])
async def handle_edit_category(message: types.Message, state: FSMContext):
    if message.text.isdigit():
        category_id = int(message.text)
        category = await lesdb.check_category(category_id)

        if category:

            await state.update_data(category_id=category_id)
            await message.answer(text="Kategoriya uchun yangi nom kiriting")
            await EditStates.FREE_CATEGORY_TWO.set()
            return
        else:
            await message.answer(
                text="Bu ID raqamda kategoriya yo'q!"
            )
            return
    await number_text_alert(message)


@dp.message_handler(state=EditStates.FREE_CATEGORY_TWO, content_types=['text'])
async def handle_edit_category_second(message: types.Message, state: FSMContext):
    new_category_name = message.text

    data = await state.get_data()
    category_id = data.get("category_id")

    await lesdb.set_category_name(new_category_name, category_id)

    await message.answer(
        text="O'zgartirildi!"
    )
    await state.finish()
