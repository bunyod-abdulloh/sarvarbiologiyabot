from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from data.config import CHANNELS
from keyboards.inline.user.callbacks import free_lessons_cb, free_less_cat_cb, paid_less_cat_cb, paid_lessons_cb
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


def category_free_ibtn(items, current_page, all_pages):
    btn = InlineKeyboardMarkup(row_width=1)
    for category in items:
        btn.add(
            InlineKeyboardButton(
                text=category['name'],
                callback_data=free_less_cat_cb.new(
                    action="category", value=category['id']
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
    btn.add(
        InlineKeyboardButton(
            text="⬅️ Ortga", callback_data=free_less_cat_cb.new(
                action="back", value="1"
            )
        )
    )
    return btn


def category_paid_ibtn(items, current_page, all_pages):
    btn = InlineKeyboardMarkup(row_width=1)
    for category in items:
        btn.add(
            InlineKeyboardButton(
                text=category['name'],
                callback_data=paid_less_cat_cb.new(
                    action="paid_category", value=category['id']
                )
            )
        )
    btn.row(
        InlineKeyboardButton(
            text="◀️",
            callback_data=paid_less_cat_cb.new(
                action="paid_prev", value=current_page
            )
        ),
        InlineKeyboardButton(
            text=f"{current_page}/{all_pages}",
            callback_data=paid_less_cat_cb.new(
                action="paid_alert", value=current_page
            )
        ),
        InlineKeyboardButton(
            text="▶️",
            callback_data=paid_less_cat_cb.new(
                action="paid_next", value=current_page
            )
        )
    )
    btn.add(
        InlineKeyboardButton(
            text="⬅️ Ortga", callback_data=paid_less_cat_cb.new(
                action="paid_back", value="1"
            )
        )
    )
    return btn


def view_free_lessons_ikb(items, current_page, all_pages, category_id):
    btn = InlineKeyboardMarkup(row_width=5)

    for n in items:
        btn.insert(
            InlineKeyboardButton(
                text=n['lesson_number'], callback_data=free_lessons_cb.new(
                    action="content", value=n['lesson_id'], c_pg=current_page
                )
            )
        )
    btn.row(
        InlineKeyboardButton(
            text="◀️",
            callback_data=free_lessons_cb.new(
                action="prev", value=category_id, c_pg=current_page
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
                action="next", value=category_id, c_pg=current_page
            )
        )
    )
    btn.add(
        InlineKeyboardButton(
            text="⬅️ Ortga", callback_data=free_lessons_cb.new(
                action="back", value="1", c_pg="1"
            )
        )
    )
    return btn


def content_back_ikb(category_id, current_page):
    btn = InlineKeyboardMarkup(row_width=1)
    btn.add(
        InlineKeyboardButton(
            text="⬅️ Ortga", callback_data=free_lessons_cb.new(
                action="content_back", value=category_id, c_pg=current_page
            )
        )
    )
    return btn


def view_paid_lessons_ikb(items, current_page, all_pages, category_id):
    btn = InlineKeyboardMarkup(row_width=5)

    for n in items:
        btn.insert(
            InlineKeyboardButton(
                text=n['row_number'], callback_data=paid_lessons_cb.new(
                    action="paid_content", value=n['lesson_id'], c_pg=current_page
                )
            )
        )
    btn.row(
        InlineKeyboardButton(
            text="◀️",
            callback_data=paid_lessons_cb.new(
                action="pd_prev", value=category_id, c_pg=current_page
            )
        ),
        InlineKeyboardButton(
            text=f"{current_page}/{all_pages}",
            callback_data=paid_lessons_cb.new(
                action="pd_alert", value="0", c_pg=current_page
            )
        ),
        InlineKeyboardButton(
            text="▶️",
            callback_data=paid_lessons_cb.new(
                action="pd_next", value=category_id, c_pg=current_page
            )
        )
    )
    btn.add(
        InlineKeyboardButton(
            text="⬅️ Ortga", callback_data=paid_lessons_cb.new(
                action="pd_back", value="1", c_pg="1"
            )
        )
    )
    return btn


def content_paid_back_ikb(category_id, current_page):
    btn = InlineKeyboardMarkup(row_width=1)
    btn.add(
        InlineKeyboardButton(
            text="⬅️ Ortga", callback_data=paid_lessons_cb.new(
                action="paid_content_back", value=category_id, c_pg=current_page
            )
        )
    )
    return btn


def select_free_lesson_type_ikb():
    btn = InlineKeyboardMarkup(row_width=2)
    btn.row(
        InlineKeyboardButton(
            text="❌ Yo'q", callback_data=free_lessons_cb.new(
                action="no_add_free", value="0", c_pg="0"
            )
        ),
        InlineKeyboardButton(
            text="✅ Bor", callback_data=free_lessons_cb.new(
                action="yes_add_free", value="0", c_pg="0"
            )
        )
    )
    return btn
