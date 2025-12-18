from aiogram import types
from aiogram.dispatcher import FSMContext
from magic_filter import F

from data.config import ADMINS, BASE_CHANNEL
from keyboards.inline.admin.callbacks import yes_or_no_cb
from keyboards.inline.admin.main_ikbs import yes_or_no_ikb
from loader import dp, lesdb, pdb, bot
from states.admin import AdminStates
from utils.lessons import save_paid_lesson_file, extract_masala_number, get_file_id_caption
from .common import build_categories_text


@dp.message_handler(F.text == "💰 Pullik dars qo'shish", state="*")
async def paid_add_start(message: types.Message, state: FSMContext):
    await state.finish()
    categories = await lesdb.get_lessons_categories()
    await message.answer(
        build_categories_text(categories) + "\n\nKategoriya nomini kiriting"
    )
    await AdminStates.CATEGORY.set()


@dp.message_handler(state=AdminStates.CATEGORY, content_types=types.ContentType.TEXT)
async def paid_set_category(message: types.Message, state: FSMContext):
    category_id = await pdb.add_to_categories(message.text)
    await state.update_data(category_id=int(category_id))

    await message.answer("Qo‘shimcha material bormi?", reply_markup=yes_or_no_ikb())


@dp.callback_query_handler(yes_or_no_cb.filter(action="no"), state="*")
async def paid_no_extra(call: types.CallbackQuery):
    await call.message.edit_text("Birinchi dars ID ni yuboring")
    await AdminStates.PAID_LESSONS_ONE.set()


@dp.message_handler(state=AdminStates.PAID_LESSONS_ONE)
async def paid_set_first_id(message: types.Message, state: FSMContext):
    await state.update_data(first_id=int(message.text))
    await message.answer("Oxirgi dars ID ni yuboring")
    await AdminStates.PAID_LESSONS_TWO.set()


@dp.message_handler(state=AdminStates.PAID_LESSONS_TWO)
async def paid_add_by_range(message: types.Message, state: FSMContext):
    data = await state.get_data()

    for msg_id in range(data["first_id"], int(message.text) + 1):
        lesson_id = await pdb.add_to_paid_lessons(data["category_id"])
        media = await bot.forward_message(
            chat_id=ADMINS[0],
            from_chat_id=BASE_CHANNEL,
            message_id=msg_id
        )
        await save_paid_lesson_file(lesson_id, media, media.caption)

    await message.answer("Pullik darslar qo‘shildi")
    await state.finish()


@dp.callback_query_handler(yes_or_no_cb.filter(action="yes"), state="*")
async def paid_yes_extra(call: types.CallbackQuery):
    await call.message.edit_text("Asosiy darsni yuboring")
    await AdminStates.PAID_LESSONS_THREE.set()


@dp.message_handler(
    state=AdminStates.PAID_LESSONS_THREE,
    content_types=['audio', 'video', 'document', 'voice']
)
async def paid_add_main_file(message: types.Message, state: FSMContext):
    file_id, file_type, caption = get_file_id_caption(message)
    number = extract_masala_number(caption)

    await state.update_data(
        main=dict(file_id=file_id, file_type=file_type, caption=f"{number} - masala")
    )

    await message.answer("Qo‘shimcha materialni yuboring")
    await AdminStates.PAID_LESSONS_FOUR.set()


@dp.message_handler(
    state=AdminStates.PAID_LESSONS_FOUR,
    content_types=['audio', 'video', 'document', 'voice']
)
async def paid_add_extra_file(message: types.Message, state: FSMContext):
    file_id, file_type, caption = get_file_id_caption(message)
    number = extract_masala_number(caption)

    await state.update_data(
        extra=dict(file_id=file_id, file_type=file_type, caption=f"{number} - masala")
    )

    await message.answer("Dars tartib raqamini kiriting")
    await AdminStates.PAID_LESSONS_FIVE.set()


@dp.message_handler(state=AdminStates.PAID_LESSONS_FIVE)
async def paid_finalize(message: types.Message, state: FSMContext):
    data = await state.get_data()
    lesson_id = await pdb.add_to_paid_lessons(data["category_id"])

    for part in ("main", "extra"):
        await pdb.add_to_pd_lessons_files(
            lesson_number=message.text,
            lesson_id=lesson_id,
            **data[part]
        )

    await message.answer("Pullik dars saqlandi")
    await state.finish()
