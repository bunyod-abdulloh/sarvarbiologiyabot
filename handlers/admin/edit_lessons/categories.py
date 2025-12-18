from aiogram import types
from aiogram.dispatcher import FSMContext
from magic_filter import F

from filters.admins import IsBotAdminFilter
from loader import dp, lesdb
from states.admin import AdminStates


@dp.message_handler(IsBotAdminFilter(), F.text == "Kategoriya o'zgartirish", state="*")
async def handle_edit_categories(message: types.Message, state: FSMContext):
    await state.finish()

    categories = await lesdb.get_categories()

    categories_str = "Mavjud kategoriyalar\n\n"

    for category in categories:
        categories_str += f"{category['id']}. {category['name']}\n"

    await message.answer(
        text=f"{categories_str}\nO'zgartirmoqchi bo'lgan kategoriyangizni ID raqamini kiriting"
    )
    await AdminStates.EDIT_CATEGORY.set()


@dp.message_handler(state=AdminStates.EDIT_CATEGORY, content_types=['text'])
async def handle_edit_category(message: types.Message, state: FSMContext):
    if message.text.isdigit():
        category_id = int(message.text)
        await state.update_data(category_id=category_id)
        await message.answer(text="Kategoriya uchun yangi nom kiriting")
        await AdminStates.EDIT_CATEGORY_SECOND.set()
        return
    await message.answer(
        text="Faqat raqam kiritilishi lozim!"
    )


@dp.message_handler(state=AdminStates.EDIT_CATEGORY_SECOND, content_types=['text'])
async def handle_edit_category_second(message: types.Message, state: FSMContext):
    new_category_name = message.text

    data = await state.get_data()
    category_id = data.get("category_id")

    await lesdb.set_category_name(new_category_name, category_id)

    await message.answer(
        text="O'zgartirildi!"
    )
    await state.finish()
