from data.config import CHANNELS
from keyboards.inline.admin.main_ikbs import check_or_cancel_ikb, send_answer_ikb
from loader import bot


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