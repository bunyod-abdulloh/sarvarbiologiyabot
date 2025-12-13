from aiogram import types
from aiogram.dispatcher import FSMContext
from magic_filter import F

from loader import dp, lesdb


@dp.message_handler(F.text == "add_lessons", state="*")
async def handle_add_lessons(message: types.Message, state: FSMContext):
    await message.answer(
        text="Faylni yuboring"
    )
    await state.set_state("add_lesson")


@dp.message_handler(state="add_lesson", content_types=types.ContentType.ANY)
async def handle_add_lessons_second(message: types.Message, state: FSMContext):
    file_id = message.video.file_id
    caption = message.caption

    await lesdb.add_lesson("video", file_id, caption)
    await message.answer(text="Qo'shildi!")
