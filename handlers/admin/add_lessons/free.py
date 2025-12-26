from aiogram import types
from aiogram.dispatcher import FSMContext
from magic_filter import F

from data.config import ADMINS, BASE_CHANNEL
from keyboards.inline.admin.callbacks import yes_no_cb
from keyboards.inline.admin.main_ikbs import yes_no_ikb
from loader import dp, lesdb, bot
from states.admin import AdminStates
from utils.lessons import extract_masala_number, get_file_id_caption, save_lesson_file


@dp.message_handler(F.text == "🆓 Bepul", state="*")
async def free_add_start(message: types.Message, state: FSMContext):
    await state.finish()

    await AdminStates.FREE_CATEGORY.set()
    categories = await lesdb.get_lessons_categories()
    text = "Mavjud kategoriyalar\n\n"
    for index, c in enumerate(categories, 1):
        text += f"{index}. {c['name']}\n"
    await message.answer(
        f"{text}\nKategoriya nomini kiriting"
    )


@dp.message_handler(state=AdminStates.FREE_CATEGORY, content_types=types.ContentType.TEXT)
async def free_set_category(message: types.Message, state: FSMContext):
    category_id = await lesdb.add_category(int(message.text))
    await state.update_data(category_id=int(category_id))

    subcategories = await lesdb.get_subcategories(category_id)

    if subcategories:
        subcategories_str = "Ushbu kategoriyaga tegishli subkategoriyalar\n\n"

        for index, s in enumerate(subcategories, 1):
            subcategories_str += f"{index}. {s['name']}\n"

        await message.answer(
            text=f"{subcategories_str}\nSubkategoriya nomini kiriting"
        )

        await AdminStates.FREE_SUBCATEGORY.set()
    else:
        await message.answer(text="Bu kategoriyada subkategoriyalar mavjud emas!")


@dp.message_handler(state=AdminStates.FREE_SUBCATEGORY, content_types=['text'])
async def free_set_subcategory(message: types.Message, state: FSMContext):
    await state.update_data(subcategory_name=message.text)
    await message.answer("Qo‘shimcha material bormi?", reply_markup=yes_no_ikb())


@dp.callback_query_handler(yes_no_cb.filter(action="no"), state="*")
async def free_no_extra(call: types.CallbackQuery):
    await call.message.edit_text("Birinchi dars ID ni yuboring")
    await AdminStates.FREE_LESSONS_ONE.set()


@dp.message_handler(state=AdminStates.FREE_LESSONS_ONE)
async def free_set_first_id(message: types.Message, state: FSMContext):
    await state.update_data(first_id=int(message.text))
    await message.answer("Oxirgi dars ID ni yuboring")
    await AdminStates.FREE_LESSONS_TWO.set()


@dp.message_handler(state=AdminStates.FREE_LESSONS_TWO)
async def free_add_by_range(message: types.Message, state: FSMContext):
    data = await state.get_data()
    category_id = data.get("category_id")
    subcategory_name = data.get("subcategory_name")

    for msg_id in range(data["first_id"], int(message.text) + 1):
        subcategory_id = await lesdb.add_subcategory(category_id, subcategory_name)
        lesson_id = await lesdb.add_lessons(subcategory_id)
        media = await bot.forward_message(
            chat_id=ADMINS[0],
            from_chat_id=BASE_CHANNEL,
            message_id=msg_id
        )
        await save_lesson_file(lesson_id, media, media.caption)

    await message.answer("Bepul darslar qo‘shildi")
    await state.finish()


@dp.callback_query_handler(yes_no_cb.filter(action="yes"), state="*")
async def free_yes_extra(call: types.CallbackQuery):
    await call.message.edit_text("Asosiy darsni yuboring")
    await AdminStates.FREE_LESSONS_THREE.set()


@dp.message_handler(
    state=AdminStates.FREE_LESSONS_THREE,
    content_types=['audio', 'video', 'document', 'voice']
)
async def free_add_main_file(message: types.Message, state: FSMContext):
    file_id, file_type, caption = get_file_id_caption(message)
    number = extract_masala_number(caption)

    await state.update_data(
        main=dict(file_id=file_id, file_type=file_type, caption=f"{number} - masala")
    )

    await message.answer("Qo‘shimcha materialni yuboring")
    await AdminStates.FREE_LESSONS_FOUR.set()


@dp.message_handler(
    state=AdminStates.FREE_LESSONS_FOUR,
    content_types=['audio', 'video', 'document', 'voice']
)
async def free_add_extra_file(message: types.Message, state: FSMContext):
    file_id, file_type, caption = get_file_id_caption(message)
    number = extract_masala_number(caption)

    await state.update_data(
        extra=dict(file_id=file_id, file_type=file_type, caption=f"{number} - masala")
    )

    await message.answer("Dars tartib raqamini kiriting")
    await AdminStates.FREE_LESSONS_FIVE.set()


@dp.message_handler(state=AdminStates.FREE_LESSONS_FIVE)
async def free_finalize(message: types.Message, state: FSMContext):
    data = await state.get_data()
    subcategory_name = data.get("subcategory_name")
    category_id = data.get("category_id")

    subcategory_id = await lesdb.add_subcategory(category_id, subcategory_name)

    lesson_id = await lesdb.add_lessons(subcategory_id)

    for part in ("main", "extra"):
        await lesdb.add_lesson_files(
            lesson_number=message.text,
            lesson_id=lesson_id,
            **data[part]
        )

    await message.answer("Bepul dars saqlandi")
    await state.finish()
