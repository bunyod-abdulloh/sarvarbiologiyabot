from aiogram import types
from aiogram.dispatcher import FSMContext
from magic_filter import F

from filters.admins import IsBotAdminFilter
from loader import dp, lesdb
from states.admin import AdminStates
from .common import build_categories_text, build_lessons_text, extract_media_data


@dp.message_handler(IsBotAdminFilter(), F.text == "Dars o'zgartirish (bepul)", state="*")
async def free_edit_start(message: types.Message, state: FSMContext):
    await state.finish()
    categories = await lesdb.get_categories()

    await message.answer(
        build_categories_text(categories) +
        "\nKerakli kategoriya ID raqamini kiriting"
    )
    await AdminStates.EDIT_FREE_LESSON_ONE.set()


@dp.message_handler(state=AdminStates.EDIT_FREE_LESSON_ONE)
async def free_select_category(message: types.Message, state: FSMContext):
    if not message.text.isdigit():
        await message.answer("Faqat raqam kiritilishi lozim!")
        return

    category_id = int(message.text)
    lessons = await lesdb.get_lessons_by_category_id(category_id)

    if not lessons:
        await message.answer("Pullik kategoriya ID kiritdingiz!")
        return

    await state.update_data(category_id=category_id)

    await message.answer(
        build_lessons_text(lessons) +
        "\nO'zgartirmoqchi bo'lgan masala ID raqamini kiriting"
    )
    await AdminStates.EDIT_FREE_LESSON_TWO.set()


@dp.message_handler(state=AdminStates.EDIT_FREE_LESSON_TWO)
async def free_select_lesson(message: types.Message, state: FSMContext):
    if not message.text.isdigit():
        await message.answer("Faqat raqam kiritilishi lozim!")
        return

    await state.update_data(lesson_id=int(message.text))
    await message.answer("Masala tartib raqamini yuboring")
    await AdminStates.EDIT_FREE_LESSON_THREE.set()


@dp.message_handler(state=AdminStates.EDIT_FREE_LESSON_THREE)
async def free_set_lesson_number(message: types.Message, state: FSMContext):
    await state.update_data(lesson_number=message.text)
    await message.answer("Masala faylini matni bilan yuboring")
    await AdminStates.EDIT_FREE_LESSON_FOUR.set()


@dp.message_handler(
    state=AdminStates.EDIT_FREE_LESSON_FOUR,
    content_types=['audio', 'video', 'voice', 'document']
)
async def free_update_lesson(message: types.Message, state: FSMContext):
    file_id, file_type, caption = extract_media_data(message)
    data = await state.get_data()

    ok = await lesdb.check_free_lesson_category_exists(
        lesson_file_id=data["lesson_id"],
        category_id=data["category_id"]
    )

    if not ok:
        await message.answer("Xatolik!")
        return

    await lesdb.set_free_lesson(
        file_id=file_id,
        file_type=file_type,
        caption=caption,
        lesson_number=data["lesson_number"],
        lesson_id=data["lesson_id"]
    )

    await message.answer("Bepul dars o'zgartirildi!")
    await state.finish()
