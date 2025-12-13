from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from data.config import CHANNELS
from keyboards.inline.user.callbacks import free_lessons_cb, free_less_cat_cb
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


def category_free_ibtn(items, current_page, all_pages):
    btn = InlineKeyboardMarkup(row_width=1)
    for category in items:
        btn.add(
            InlineKeyboardButton(
                text=category['category_name'],
                callback_data=free_less_cat_cb.new(
                    action="category", value=category['category_id']
                )
            )
        )
    btn.row(
        InlineKeyboardButton(
            text="◀️",
            callback_data=free_less_cat_cb.new(
                action="prev", value=current_page
            )
        ),
        InlineKeyboardButton(
            text=f"{current_page}/{all_pages}",
            callback_data=free_less_cat_cb.new(
                action="alert", value=current_page
            )
        ),
        InlineKeyboardButton(
            text="▶️",
            callback_data=free_less_cat_cb.new(
                action="next", value=current_page
            )
        )
    )
    return btn


def key_returner(items, current_page, all_pages, selected):
    btn = InlineKeyboardMarkup(row_width=10)
    for item in items:
        if selected == item['position']:
            btn.insert(
                InlineKeyboardButton(
                    text=f"[ {item['position']} ]",
                    callback_data=free_lessons_cb.new(
                        action="slctd", value=item['id'], c_pg=current_page
                    )
                )
            )
        else:
            btn.insert(
                InlineKeyboardButton(
                    text=f"{item['position']}",
                    callback_data=free_lessons_cb.new(
                        action="no_slctd", value=item['id'], c_pg=current_page
                    )
                )
            )
    btn.row(
        InlineKeyboardButton(
            text="◀️",
            callback_data=free_lessons_cb.new(
                action="prev", value=items[0]['id'], c_pg=current_page
            )
        ),
        InlineKeyboardButton(
            text=f"{current_page}/{all_pages}",
            callback_data=free_lessons_cb.new(
                action="alert", value="0", c_pg=current_page
            )
        ),
        InlineKeyboardButton(
            text="▶️",
            callback_data=free_lessons_cb.new(
                action="next", value=items[0]['id'], c_pg=current_page
            )
        )
    )
    return btn
