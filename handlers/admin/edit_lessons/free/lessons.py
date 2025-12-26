from aiogram import types
from aiogram.dispatcher import FSMContext
from magic_filter import F

from filters.admins import IsBotAdminFilter
from handlers.admin.helpers import build_categories_text, build_subcategories_text, build_lessons_text_admin
from loader import dp, lesdb
from states.admin import EditStates
from utils.helpers import number_text_alert
from utils.lessons import get_file_id_caption


@dp.message_handler(IsBotAdminFilter(), F.text == "♻️ Dars", state="*")
async def free_edit_start(message: types.Message, state: FSMContext):
    await state.finish()
    categories = await lesdb.get_lessons_categories()

    await message.answer(
        build_categories_text(categories) +
        "\nKerakli kategoriya ID raqamini kiriting"
    )
    await EditStates.FREE_LESSON_ONE.set()


@dp.message_handler(state=EditStates.FREE_LESSON_ONE)
async def free_select_category(message: types.Message, state: FSMContext):
    if not message.text.isdigit():
        await message.answer("Faqat raqam kiritilishi lozim!")
        return

    category_id = int(message.text)
    check = await lesdb.check_category(category_id)

    if check:
        subcategories = await lesdb.get_subcategories(category_id)

        if subcategories:
            await state.update_data(category_id=category_id)

            await message.answer(
                build_subcategories_text(subcategories) +
                "\nKerakli subkategoriya ID raqamini kiriting"
            )
            await EditStates.FREE_LESSON_TWO.set()
        else:
            await message.answer(text="Bu kategoriyada subkategoriyalar yo'q")
    else:
        await message.answer(text="Bunday ID raqamli kategoriya yo'q!")


@dp.message_handler(state=EditStates.FREE_LESSON_TWO)
async def free_select_lesson(message: types.Message, state: FSMContext):
    if not message.text.isdigit():
        await number_text_alert(message)
        return

    subcategory_id = int(message.text)

    data = await state.get_data()
    category_id = data.get("category_id")
    check = await lesdb.check_subcategory(category_id, subcategory_id)

    if check:
        lessons = await lesdb.get_free_lessons(subcategory_id)

        if lessons:
            await state.update_data(subcategory_id=subcategory_id)
            await message.answer(
                text=build_lessons_text_admin(lessons) + "O'zgartirmoqchi bo'lgan masala ID raqamini yuboring")
            await EditStates.FREE_LESSON_THREE.set()
        else:
            await message.answer(text="Bu subkategoriyada masalalar yo'q!")
    else:
        await message.answer(text="Bu ID raqamda subkategoriya mavjud emas!")


@dp.message_handler(state=EditStates.FREE_LESSON_THREE, content_types=['text'])
async def free_set_lesson_number(message: types.Message, state: FSMContext):
    if message.text.isdigit():
        data = await state.get_data()
        subcategory_id = data.get("subcategory_id")
        lesson_id = int(message.text)

        check = await lesdb.lesson_file_exists(lesson_id, subcategory_id)

        if check:
            await state.update_data(lesson_id=int(message.text))
            await message.answer(text="Masala tartib raqamini kiriting")
            await EditStates.FREE_LESSON_FOUR.set()
            return

        await message.answer(text="Bunday ID raqamli masala mavjud emas!")
    else:
        await number_text_alert(message)


@dp.message_handler(state=EditStates.FREE_LESSON_FOUR, content_types=['text'])
async def free_get_lesson_number(message: types.Message, state: FSMContext):
    if message.text.isdigit():
        lesson_number = message.text
        await state.update_data(lesson_number=lesson_number)
        await message.answer("Masala faylini matni bilan yuboring")
        await EditStates.FREE_LESSON_FIVE.set()
    else:
        await number_text_alert(message)


@dp.message_handler(state=EditStates.FREE_LESSON_FIVE,
                    content_types=['audio', 'document', 'video', 'voice'])
async def free_update_datas(message: types.Message, state: FSMContext):
    file_id, file_type, caption = get_file_id_caption(message)
    data = await state.get_data()
    lesson_number = data.get("lesson_number")
    lesson_id = data.get("lesson_id")

    await lesdb.set_free_lesson(
        file_id=file_id,
        file_type=file_type,
        caption=caption,
        lesson_number=lesson_number,
        lesson_id=lesson_id
    )

    await message.answer("Bepul dars o'zgartirildi!")
    await state.finish()
