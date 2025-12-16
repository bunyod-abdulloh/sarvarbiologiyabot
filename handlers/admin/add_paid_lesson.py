from aiogram import types
from aiogram.dispatcher import FSMContext
from magic_filter import F

from keyboards.inline.admin.callbacks import yes_or_no_cb
from keyboards.inline.admin.main_ikbs import yes_or_no_ikb
from loader import dp, lesdb, pdb
from states.admin import AdminStates
from utils.lessons import get_file_id_caption


@dp.message_handler(F.text == "💰 Pullik dars qo'shish", state="*")
async def handle_add_paid_lessons(message: types.Message, state: FSMContext):
    categories = await lesdb.get_lessons_categories()

    categories_str = "Mavjud kategoriyalar:\n\n"

    for index, category in enumerate(categories, start=1):
        categories_str += f"{index}. {category['name']}\n"

    await message.answer(
        text=f"{categories_str}\nKategoriya nomini kiriting"
    )
    await AdminStates.CATEGORY.set()


@dp.message_handler(state=AdminStates.CATEGORY, content_types=types.ContentType.TEXT)
async def handle_add_lessons_second(message: types.Message, state: FSMContext):
    category_id = await pdb.add_to_categories(category_name=message.text)
    await state.update_data(category_id=category_id)
    await message.answer(
        text="Darsni yuboring"
    )
    await AdminStates.PAID_LESSONS_ONE.set()


@dp.message_handler(state=AdminStates.PAID_LESSONS_ONE, content_types=['audio', 'video', 'document', 'voice'])
async def handle_add_paid_lessons(message: types.Message, state: FSMContext):
    file_id, file_type, caption = get_file_id_caption(message)

    category_id = (await state.get_data()).get("category_id")

    lesson_id = await pdb.add_to_paid_lessons(category_id=category_id)

    await pdb.add_to_pd_lessons_files(
        lesson_id, file_id, file_type, caption
    )

    await state.update_data(lesson_id=lesson_id)

    await message.answer(
        text="Qabul qilindi!\n\nUshbu darsga qo'shimcha material bormi?",
        reply_markup=yes_or_no_ikb()
    )


@dp.callback_query_handler(yes_or_no_cb.filter(action="yes"), state="*")
async def handle_yes_add_lesson(call: types.CallbackQuery, state: FSMContext, callback_data: dict):
    await call.message.edit_text(
        text="Qo'shimcha materialni yuboring"
    )
    await AdminStates.PAID_LESSONS_TWO.set()


@dp.message_handler(state=AdminStates.PAID_LESSONS_TWO, content_types=['audio', 'video', 'document', 'voice'])
async def handle_add_second_paid(message: types.Message, state: FSMContext):
    data = await state.get_data()
    category_id = int(data.get("category_id"))
    lesson_id = int(data.get("lesson_id"))

    file_id, file_type, caption = get_file_id_caption(message)

    await pdb.add_to_pd_lessons_files(
        lesson_id, file_id, file_type, caption
    )

    await message.answer(
        text="Qabul qilindi!\n\nUshbu darsga qo'shimcha material bormi?",
        reply_markup=yes_or_no_ikb()
    )


@dp.callback_query_handler(yes_or_no_cb.filter(action="no"), state="*")
async def handle_no_add_lesson(call: types.CallbackQuery, state: FSMContext):
    await state.finish()
    await call.message.edit_text(
        text="Rahmat!"
    )
