from aiogram import types


def paginate(files, per_page=50):
    from utils.helpers import extracter
    items = extracter(files, per_page)
    return items, len(items)


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
