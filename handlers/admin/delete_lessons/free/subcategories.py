from aiogram import types
from aiogram.dispatcher import FSMContext
from magic_filter import F

from filters.admins import IsBotAdminFilter
from handlers.admin.helpers import build_categories_text, build_subcategories_text
from loader import dp, lesdb
from states.admin import AdminDeleteStates
from utils.helpers import number_text_alert


@dp.message_handler(IsBotAdminFilter(), F.text == "🗑 Subkategoriya", state="*")
async def delete_subcategory_start(message: types.Message, state: FSMContext):
    await state.finish()

    categories = await lesdb.get_lessons_categories()

    await message.answer(
        text=build_categories_text(categories) + "\nKerakli kategoriya ID raqamini kiriting"
    )
    await AdminDeleteStates.FREE_SUBCATEGORY_ONE.set()


@dp.message_handler(state=AdminDeleteStates.FREE_SUBCATEGORY_ONE, content_types=['text'])
async def delete_subcategory_category(message: types.Message, state: FSMContext):
    if message.text.isdigit():
        category_id = int(message.text)
        await state.update_data(category_id=category_id)

        check = await lesdb.check_category(category_id)

        if check:
            subcategories = await lesdb.get_subcategories(category_id)
            if subcategories:
                await message.answer(
                    text=build_subcategories_text(
                        subcategories) + "\nO'chirmoqchi bo'lgan subkategoriya ID raqamini kiriting"
                )
                await AdminDeleteStates.FREE_SUBCATEGORY_TWO.set()
            else:
                await message.answer(text="Subkategoriyalar yo'q!")
                await state.finish()
        else:
            await message.answer(
                text="Bu ID raqamli kategoriya yo'q!"
            )
    else:
        await number_text_alert(message)


@dp.message_handler(state=AdminDeleteStates.FREE_SUBCATEGORY_TWO, content_types=['text'])
async def delete_subcategory_end(message: types.Message, state: FSMContext):
    if message.text.isdigit():
        data = await state.get_data()
        category_id = data.get("category_id")
        subcategory_id = int(message.text)
        check = await lesdb.check_subcategory(category_id, subcategory_id)

        if check:
            await lesdb.delete_subcategory(subcategory_id)
            await message.answer(text="O'chirildi!")
            await state.finish()
        else:
            await message.answer(
                text="Bu ID raqamda subkategoriya yo'q!"
            )
    else:
        await number_text_alert(message)
