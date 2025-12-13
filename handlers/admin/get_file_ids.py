from aiogram import types
from aiogram.dispatcher import FSMContext

from loader import dp


@dp.message_handler(state="*", content_types=types.ContentType.ANY)
async def handle_file_id(message: types.Message, state: FSMContext):
    await message.answer(
        text=f"<code>{message.video.file_id}</code>"
    )
