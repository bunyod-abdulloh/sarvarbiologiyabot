from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from keyboards.inline.user.callbacks import paid_lessons_cb, paid_less_cat_cb, paid_subcat_cb


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


def view_paid_subcategories_ikb(items, current_page, all_pages, category_id):
    btn = InlineKeyboardMarkup(row_width=1)
    for subcategory in items:
        btn.add(
            InlineKeyboardButton(
                text=subcategory['name'],
                callback_data=paid_subcat_cb.new(
                    action="subcategory", value=subcategory['id'], cat_id=0
                )
            )
        )
    btn.row(
        InlineKeyboardButton(
            text="◀️",
            callback_data=paid_subcat_cb.new(
                action="prev", value=current_page, cat_id=category_id
            )
        ),
        InlineKeyboardButton(
            text=f"{current_page}/{all_pages}",
            callback_data=paid_subcat_cb.new(
                action="alert", value=current_page, cat_id=0
            )
        ),
        InlineKeyboardButton(
            text="▶️",
            callback_data=paid_subcat_cb.new(
                action="next", value=current_page, cat_id=category_id
            )
        )
    )
    btn.add(
        InlineKeyboardButton(
            text="⬅️ Ortga", callback_data=paid_subcat_cb.new(
                action="back", value="1", cat_id=0
            )
        )
    )
    return btn


def view_paid_lessons_ikb(items, current_page, all_pages, subcategory_id):
    btn = InlineKeyboardMarkup(row_width=5)

    for n in items:
        btn.insert(
            InlineKeyboardButton(
                text=n['lesson_number'], callback_data=paid_lessons_cb.new(
                    action="paid_content", value=n['lesson_id'], c_pg=current_page
                )
            )
        )
    btn.row(
        InlineKeyboardButton(
            text="◀️",
            callback_data=paid_lessons_cb.new(
                action="pd_prev", value=subcategory_id, c_pg=current_page
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
                action="pd_next", value=subcategory_id, c_pg=current_page
            )
        )
    )
    btn.add(
        InlineKeyboardButton(
            text="⬅️ Ortga", callback_data=paid_lessons_cb.new(
                action="pd_back", value=subcategory_id, c_pg="1"
            )
        )
    )
    return btn


def content_paid_back_ikb(subcategory_id, current_page):
    btn = InlineKeyboardMarkup(row_width=1)
    btn.add(
        InlineKeyboardButton(
            text="⬅️ Ortga", callback_data=paid_lessons_cb.new(
                action="paid_content_back", value=subcategory_id, c_pg=current_page
            )
        )
    )
    return btn
