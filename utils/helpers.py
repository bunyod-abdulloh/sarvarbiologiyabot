from aiogram import types

from data.config import CHANNELS
from keyboards.inline.admin.main_ikbs import check_or_cancel_ikb, send_answer_ikb
from loader import bot
from utils.db_functions import send_media_group_to_users


async def is_subscribed(user_id: int) -> bool:
    member = await bot.get_chat_member(chat_id=CHANNELS[0], user_id=user_id)
    return member.status in ['member', 'creator', 'administrator', 'owner']


async def send_to_admin(
        admin_id: int,
        content,
        telegram_id: int,
        is_photo: bool = False
):
    """Universal funksiya: matn yoki rasmni adminlarga yuboradi."""

    if is_photo:
        await bot.send_photo(
            chat_id=admin_id,
            photo=content,
            caption="#chek\n\nYangi chek qabul qilindi!",
            reply_markup=check_or_cancel_ikb(telegram_id)
        )
    else:
        await bot.send_message(
            chat_id=admin_id,
            text=content,
            reply_markup=send_answer_ikb(telegram_id)
        )


def extracter(all_medias, delimiter):
    empty_list = []
    for e in range(0, len(all_medias), delimiter):
        empty_list.append(all_medias[e:e + delimiter])
    return empty_list


async def number_text_alert(message: types.Message):
    text = "Faqat raqam kiritilishi lozim!"
    await message.answer(text=text)


from collections import defaultdict
import asyncio

albums = defaultdict(list)
album_tasks = {}


async def finalize_album(gid, message, state):
    try:
        # 🔴 REAL HAYOTDA ISHONCHLI VAQT
        await asyncio.sleep(0.8)
    except asyncio.CancelledError:
        return

    album = albums.pop(gid, [])
    album_tasks.pop(gid, None)

    if not album:
        return

    await state.finish()
    await message.answer("Xabar yuborish boshlandi...")

    media_group = types.MediaGroup()
    for obj in album:
        if obj.photo:
            file_id = obj.photo[-1].file_id
        else:
            file_id = obj[obj.content_type].file_id

        media_group.attach({
            "media": file_id,
            "type": obj.content_type,
            "caption": obj.caption}
        )
        await asyncio.sleep(0.05)
    await send_media_group_to_users(media_group)
