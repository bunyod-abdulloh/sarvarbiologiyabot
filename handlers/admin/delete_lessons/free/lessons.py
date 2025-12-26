from aiogram import types
from aiogram.dispatcher import FSMContext
from magic_filter import F

from filters.admins import IsBotAdminFilter
from handlers.admin.helpers import build_categories_text, build_subcategories_text, build_lessons_text_admin
from loader import dp, lesdb
from states.admin import AdminDeleteStates
from utils.helpers import number_text_alert


@dp.message_handler(IsBotAdminFilter(), F.text == "🗑 Dars", state="*")
async def delete_lesson_start(message: types.Message, state: FSMContext):
    await state.finish()

    categories = await lesdb.get_lessons_categories()

    await message.answer(
        text=build_categories_text(categories) + "\nKerakli kategoriyani tanlang"
    )
    await AdminDeleteStates.FREE_LESSON_ONE.set()


@dp.message_handler(state=AdminDeleteStates.FREE_LESSON_ONE, content_types=['text'])
async def delete_lesson_category(message: types.Message, state: FSMContext):
    if message.text.isdigit():
        category_id = int(message.text)

        check = await lesdb.check_category(category_id)

        if check:
            await state.update_data(category_id=category_id)
            subcategories = await lesdb.get_subcategories(category_id)

            if subcategories:
                await message.answer(
                    text=build_subcategories_text(subcategories) + "\nKerakli subkategoriya ID raqamini kiriting"
                )
                await AdminDeleteStates.FREE_LESSON_TWO.set()
            else:
                await message.answer(
                    text="Bu ID raqamda subkategoriya yo'q!"
                )
        else:
            await message.answer(
                text="Bu ID raqamda kategoriya yo'q!"
            )
    else:
        await number_text_alert(message)


@dp.message_handler(state=AdminDeleteStates.FREE_LESSON_TWO, content_types=['text'])
async def delete_lesson_subcategory(message: types.Message, state: FSMContext):
    if message.text.isdigit():
        data = await state.get_data()
        category_id = data.get("category_id")
        subcategory_id = int(message.text)

        check = await lesdb.check_subcategory(category_id, subcategory_id)

        if check:
            await state.update_data(subcategory_id=subcategory_id)

            lessons = await lesdb.get_free_lessons(subcategory_id)

            if lessons:
                await message.answer(
                    text=build_lessons_text_admin(lessons, True) + "\nO'chirmoqchi bo'lgan masala ID raqamini kiriting"
                )
                await AdminDeleteStates.FREE_LESSON_THREE.set()
            else:
                await message.answer(
                    text="Bu subkategoriyada masalalar yo'q!"
                )
        else:
            await message.answer(
                text="Bu ID raqamda subkategoriya yo'q!"
            )
    else:
        await number_text_alert(message)


@dp.message_handler(state=AdminDeleteStates.FREE_LESSON_THREE, content_types=['text'])
async def delete_lesson_end(message: types.Message, state: FSMContext):
    if message.text.isdigit():
        lesson_id = int(message.text)
        await lesdb.delete_lesson(lesson_id)
        await message.answer(text="O'chirildi!")
        await state.finish()
    else:
        await number_text_alert(message)
