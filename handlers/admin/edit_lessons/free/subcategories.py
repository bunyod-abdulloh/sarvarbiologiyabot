from aiogram import types
from aiogram.dispatcher import FSMContext
from magic_filter import F

from filters.admins import IsBotAdminFilter

from handlers.admin.helpers import build_subcategories_text, build_categories_text
from loader import dp, lesdb
from states.admin import EditStates
from utils.helpers import number_text_alert


@dp.message_handler(IsBotAdminFilter(), F.text == "♻️ Subkategoriya", state="*")
async def start_edit_subcategory(message: types.Message, state: FSMContext):
    await state.finish()

    categories = await lesdb.get_lessons_categories()

    await message.answer(text=build_categories_text(categories) + "\nKerakli kategoriya ID raqamini kiriting")

    await EditStates.FREE_SUBCATEGORY_ONE.set()


@dp.message_handler(state=EditStates.FREE_SUBCATEGORY_ONE, content_types=['text'])
async def edit_subcategory_get_category_id(message: types.Message, state: FSMContext):
    if message.text.isdigit():
        category_id = int(message.text)

        category = await lesdb.check_category(category_id)

        if category:
            subcategories = await lesdb.get_subcategories(category_id)
            await state.update_data(category_id=category_id)

            await message.answer(
                text=build_subcategories_text(
                    subcategories) + "\nO'zgartirmoqchi bo'lgan subkategoriya ID raqamini kiriting"
            )
            await EditStates.FREE_SUBCATEGORY_TWO.set()
        else:
            await message.answer(
                text="Bu ID raqamda kategoriya yo'q!"
            )

    else:
        await number_text_alert(message)


@dp.message_handler(state=EditStates.FREE_SUBCATEGORY_TWO, content_types=['text'])
async def edit_subcategory_get_subcategory_id(message: types.Message, state: FSMContext):
    if message.text.isdigit():
        subcategory_id = int(message.text)
        data = await state.get_data()
        category_id = data.get("category_id")
        subcategory = await lesdb.check_subcategory(category_id, subcategory_id)

        if subcategory:
            await state.update_data(subcategory_id=subcategory_id)
            await message.answer(text="Subkategoriya uchun yangi nom kiriting")
            await EditStates.FREE_SUBCATEGORY_THREE.set()
        else:
            await message.answer(
                text="Bu ID raqamda subkategoriya yo'q!"
            )
    else:
        await number_text_alert(message)


@dp.message_handler(state=EditStates.FREE_SUBCATEGORY_THREE, content_types=['text'])
async def edit_sub_set_subcategory_name(message: types.Message, state: FSMContext):
    data = await state.get_data()

    subcategory_id = data.get("subcategory_id")
    subcategory_name = message.text

    await lesdb.set_subcategory_name(subcategory_name, subcategory_id)
    await message.answer(text="O'zgartirildi!")
    await state.finish()
