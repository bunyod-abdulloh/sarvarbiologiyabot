from aiogram import types
from aiogram.dispatcher import FSMContext
from magic_filter import F

from data.config import ADMINS
from keyboards.inline.admin.callbacks import yes_no_cb
from keyboards.inline.admin.main_ikbs import yes_no_ikb
from keyboards.inline.user.callbacks import free_lessons_cb
from loader import dp, lesdb, pdb, bot
from states.admin import AdminStates
from utils.lessons import extract_masala_number, get_file_id_caption


@dp.message_handler(F.text == "🆓 Bepul dars qo'shish", state="*")
async def handle_add_free_lessons(message: types.Message, state: FSMContext):
    categories = await lesdb.get_lessons_categories()

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
        text="Qo'shmoqchi bo'lgan darslaringizni qo'shimcha materiallari bormi?",
        reply_markup=yes_no_ikb()
    )


@dp.callback_query_handler(yes_no_cb.filter(action="no"), state="*")
async def handle_no_free_add(call: types.CallbackQuery):
    await call.message.edit_text(
        text="Birinchi dars ID raqamini yuboring"
    )
    await AdminStates.FREE_LESSONS_ONE.set()


@dp.callback_query_handler(free_lessons_cb.filter(action="yes_add_free"), state="*")
async def handle_yes_free_add(call: types.CallbackQuery):
    await call.message.edit_text(
        text="Birinchi dars ID raqamini yuboring"
    )
    await AdminStates.FREE_LESSONS_ONE.set()


@dp.message_handler(state=AdminStates.FREE_LESSONS_ONE, content_types=['text'])
async def handle_add_free_lessons(message: types.Message, state: FSMContext):
    await state.update_data(first_id=message.text)
    await message.answer(
        text="Oxirgi dars ID raqamini yuboring"
    )
    await AdminStates.FREE_LESSONS_TWO.set()


@dp.message_handler(state=AdminStates.FREE_LESSONS_TWO, content_types=['text'])
async def handle_add_second_free_(message: types.Message, state: FSMContext):
    data = await state.get_data()

    first_id = int(data.get("first_id"))
    second_id = int(message.text)
    category_id = data.get("category_id")

    file_type = "video"

    for n in range(first_id, second_id + 1):
        lesson_id = await lesdb.add_to_free_lessons(category_id=category_id)
        media = await bot.forward_message(
            chat_id=ADMINS[0],
            from_chat_id=-1002932868497,
            message_id=n
        )

        file_id = media.video.file_id
        raw_caption = media.caption or ""

        lesson_number = extract_masala_number(raw_caption)

        if not lesson_number:
            continue

        await lesdb.add_to_free_lessons_files(
            lesson_number=lesson_number,
            lesson_id=lesson_id,
            file_id=file_id,
            file_type=file_type,
            caption=f"{lesson_number} - masala"
        )


@dp.callback_query_handler(yes_no_cb.filter(action="yes"), state="*")
async def handle_yes_add_lesson_free(call: types.CallbackQuery):
    await call.message.edit_text(
        text="Darsni yuboring"
    )
    await AdminStates.FREE_LESSONS_THREE.set()


@dp.message_handler(state=AdminStates.FREE_LESSONS_THREE, content_types=['audio', 'video', 'document', 'voice'])
async def handle_add_lesson_free_three(message: types.Message, state: FSMContext):
    file_id, file_type, caption = get_file_id_caption(message)

    await state.update_data(
        file_id=file_id, file_type=file_type, caption=caption
    )

    await message.answer(
        text="Qo'shimcha materialni yuboring"
    )
    await AdminStates.FREE_LESSONS_FOUR.set()


@dp.message_handler(state=AdminStates.FREE_LESSONS_FOUR, content_types=['audio', 'video', 'document', 'voice'])
async def handle_free_lesson_four(message: types.Message, state: FSMContext):
    file_id, file_type, caption = get_file_id_caption(message)

    await state.update_data(
        q_file_id=file_id, q_file_type=file_type, q_caption=caption
    )
    await message.answer(
        text="Dars tartib raqamini kiriting"
    )
    await AdminStates.FREE_LESSONS_FIVE.set()


@dp.message_handler(state=AdminStates.FREE_LESSONS_FIVE, content_types=['text'])
async def handle_add_free_lesson_five(message: types.Message, state: FSMContext):
    data = await state.get_data()

    first_file_id = data.get("file_id")
    first_file_type = data.get("file_type")
    first_caption = data.get("caption")
    second_file_id = data.get("q_file_id")
    second_file_type = data.get("q_file_type")
    second_caption = data.get("q_caption")

    lesson_number = message.text

    category_id = int(data.get("category_id"))

    lesson_id = await lesdb.add_to_free_lessons(category_id=category_id)

    await lesdb.add_to_free_lessons_files(
        lesson_number=lesson_number, lesson_id=lesson_id,
        file_id=first_file_id, file_type=first_file_type, caption=first_caption
    )

    await lesdb.add_to_free_lessons_files(
        lesson_number=lesson_number, lesson_id=lesson_id,
        file_id=second_file_id, file_type=second_file_type, caption=second_caption
    )

    await message.answer(
        text="Qabul qilindi!"
    )
    await state.finish()
