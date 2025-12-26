from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from data.config import CHANNELS
from loader import bot


def main_page_ibtn():
    btn = InlineKeyboardMarkup()
    btn.add(
        InlineKeyboardButton(
            text="📘 Bepul darslar", callback_data="free_lessons"
        )
    )
    btn.add(
        InlineKeyboardButton(
            text="💎 Pullik darslar", callback_data="paid_lessons"
        )
    )
    btn.add(
        InlineKeyboardButton(
            text="📲 Adminga xabar", callback_data="send_to_admin"
        )
    )
    return btn


async def subscribe_ibtn():
    channel = await bot.get_chat(CHANNELS[0])
    btn = InlineKeyboardMarkup(row_width=1)
    btn.add(
        InlineKeyboardButton(text=channel.full_name, url=f"https://t.me/{channel.username}"),
        InlineKeyboardButton(text="✅ A'zo bo'ldim!", callback_data="subscribed")
    )
    return btn


def image_or_text_ibtn():
    btn = InlineKeyboardMarkup()
    btn.add(
        InlineKeyboardButton(
            text="Chek rasmi", callback_data="purchase_receipt"
        ),
        InlineKeyboardButton(
            text="Matnli", callback_data="text_message"
        )
    )
    return btn
