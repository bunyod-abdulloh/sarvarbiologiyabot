from aiogram import types
from aiogram.dispatcher import FSMContext
from magic_filter import F

from filters.admins import IsBotAdminFilter
from loader import dp, lesdb
from states.admin import AdminStates


@dp.message_handler(IsBotAdminFilter(), F.text == "Kategoriya o'chirish", state="*")
async def handle_delete_categories_main(message: types.Message, state: FSMContext):
    await state.finish()

    categories = await lesdb.get_categories()

    categories_str = "Kategoriyalar\n\n"

    for category in categories:
        categories_str += f"{category['id']}. {category['name']}\n"

    await message.answer(
        text=f"{categories_str}\nO'chirmoqchi bo'lgan kategoriya ID raqamini kiriting"
    )
    await AdminStates.DELETE_CATEGORY.set()


@dp.message_handler(state=AdminStates.DELETE_CATEGORY, content_types=['text'])
async def handle_delete_category_state(message: types.Message, state: FSMContext):
    if message.text.isdigit():
        category_id = int(message.text)
        await lesdb.delete_category(category_id)
        await message.answer(
            text="O'chirildi!"
        )
        return
    await message.answer(
        text="Faqat raqam kiritilishi lozim!"
    )
