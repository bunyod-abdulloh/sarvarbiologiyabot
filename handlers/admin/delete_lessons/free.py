# handlers/admin/delete_lessons/free.py

from aiogram import types
from aiogram.dispatcher import FSMContext
from magic_filter import F

from filters.admins import IsBotAdminFilter
from loader import dp, lesdb
from states.admin import AdminStates
from .common import build_categories_text, build_lessons_text


@dp.message_handler(IsBotAdminFilter(), F.text == "Dars o'chirish (bepul)", state="*")
async def free_delete_start(message: types.Message, state: FSMContext):
    await state.finish()
    categories = await lesdb.get_categories()

    await message.answer(
        build_categories_text(categories) +
        "\nKerakli kategoriya ID raqamini kiriting"
    )
    await AdminStates.DELETE_LESSON_ONE.set()


@dp.message_handler(state=AdminStates.DELETE_LESSON_ONE)
async def free_select_category(message: types.Message):
    if not message.text.isdigit():
        await message.answer("Faqat raqam kiritilishi lozim!")
        return

    lessons = await lesdb.get_lessons_by_category_id(int(message.text))
    if not lessons:
        await message.answer("Bu kategoriyada bepul darslar yo‘q!")
        return

    await message.answer(
        build_lessons_text(lessons) +
        "\nO'chirmoqchi bo'lgan masala ID raqamini kiriting"
    )
    await AdminStates.DELETE_LESSON_TWO.set()


@dp.message_handler(state=AdminStates.DELETE_LESSON_TWO)
async def free_delete_lesson(message: types.Message, state: FSMContext):
    if not message.text.isdigit():
        await message.answer("Faqat raqam kiritilishi lozim!")
        return

    await lesdb.delete_lesson_free(int(message.text))
    await message.answer("Bepul dars o'chirildi!")
    await state.finish()
