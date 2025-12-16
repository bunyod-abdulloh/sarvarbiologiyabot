from aiogram import types

from keyboards.inline.user.ibuttons import key_returner
from loader import lesdb


def paginate(files, per_page=50):
    from utils.helpers import extracter
    items = extracter(files, per_page)
    return items, len(items)


async def open_lesson(
        call: types.CallbackQuery,
        position: int,
        page: int,
        category_id: int | None = None
):
    if category_id:
        files = await lesdb.get_lessons_by_category_id(category_id)
    else:
        files = await lesdb.get_lesson_free()

    items, total_pages = paginate(files)

    lesson = await lesdb.get_lesson_by_position(position)

    key = key_returner(
        items=items[page - 1],
        current_page=page,
        all_pages=total_pages,
        selected=position
    )

    for l in lesson:
        await send_media(call.message, l, key)


async def send_media(message, lesson, reply_markup):
    file_type = lesson["file_type"]

    if file_type == "audio":
        await message.edit_media(
            media=types.InputMediaAudio(
                media=lesson["file_id"],
                caption=lesson["caption"]
            ),
            reply_markup=reply_markup
        )

    elif file_type == "video":
        await message.edit_media(
            media=types.InputMediaVideo(
                media=lesson["file_id"],
                caption=lesson["caption"]
            ),
            reply_markup=reply_markup
        )


def get_file_id_caption(message: types.Message):
    file_id = None
    file_type = None

    if message.video:
        file_id = message.video.file_id
        file_type = "video"
    elif message.audio:
        file_id = message.audio.file_id
        file_type = "audio"
    elif message.document:
        file_id = message.document.file_id
        file_type = "document"
    elif message.voice:
        file_id = message.voice.file_id
        file_type = "voice"

    caption = message.caption

    return file_id, file_type, caption
