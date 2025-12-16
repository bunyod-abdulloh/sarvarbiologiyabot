from aiogram import types
from aiogram.dispatcher import FSMContext
from magic_filter import F

from keyboards.inline.admin.callbacks import yes_no_cb
from keyboards.inline.admin.main_ikbs import yes_or_no_ikb, yes_no_ikb
from loader import dp, lesdb, pdb
from states.admin import AdminStates
from utils.lessons import get_file_id_caption


@dp.message_handler(F.text == "🆓 Bepul dars qo'shish", state="*")
async def handle_add_free_lessons(message: types.Message, state: FSMContext):
    categories = await lesdb.get_free_lessons_by_category()

    categories_str = "Mavjud kategoriyalar:\n\n"

    for index, category in enumerate(categories, start=1):
        categories_str += f"{index}. {category['name']}\n"

    await message.answer(
        text=f"{categories_str}\nKategoriya nomini kiriting"
    )
    await AdminStates.FREE_CATEGORY.set()


@dp.message_handler(state=AdminStates.FREE_CATEGORY, content_types=types.ContentType.TEXT)
async def handle_add_lessons_second_free(message: types.Message, state: FSMContext):
    category_id = await pdb.add_to_categories(category_name=message.text)
    await state.update_data(category_id=category_id)
    await message.answer(
        text="Darsni yuboring"
    )
    await AdminStates.FREE_LESSONS_ONE.set()


@dp.message_handler(state=AdminStates.FREE_LESSONS_ONE, content_types=['audio', 'video', 'document', 'voice'])
async def handle_add_free_lessons(message: types.Message, state: FSMContext):
    file_id, file_type, caption = get_file_id_caption(message)

    category_id = (await state.get_data()).get("category_id")

    lesson_id = await lesdb.add_to_free_lessons(category_id=category_id)

    # for n in range(100):
    await lesdb.add_to_free_lessons_files(
        lesson_id, file_id, file_type, caption
    )

    await state.update_data(lesson_id=lesson_id)

    await message.answer(
        text="Qabul qilindi!\n\nUshbu darsga qo'shimcha material bormi?",
        reply_markup=yes_no_ikb()
    )


@dp.callback_query_handler(yes_no_cb.filter(action="yes"), state="*")
async def handle_yes_add_lesson_free(call: types.CallbackQuery):
    await call.message.edit_text(
        text="Qo'shimcha materialni yuboring"
    )
    await AdminStates.FREE_LESSONS_TWO.set()


@dp.message_handler(state=AdminStates.FREE_LESSONS_TWO, content_types=['audio', 'video', 'document', 'voice'])
async def handle_add_second_free_(message: types.Message, state: FSMContext):
    data = await state.get_data()

    lesson_id = int(data.get("lesson_id"))

    file_id, file_type, caption = get_file_id_caption(message)

    await lesdb.add_to_free_lessons_files(
        lesson_id, file_id, file_type, caption
    )

    await message.answer(
        text="Qabul qilindi!\n\nUshbu darsga qo'shimcha material bormi?",
        reply_markup=yes_or_no_ikb()
    )


@dp.callback_query_handler(yes_no_cb.filter(action="no"), state="*")
async def handle_no_add_lesson_free(call: types.CallbackQuery, state: FSMContext):
    await state.finish()
    await call.message.edit_text(
        text="Rahmat!"
    )
