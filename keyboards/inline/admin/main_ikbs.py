from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from keyboards.inline.admin.callbacks import check_cancel_cb, answer_cb, yes_or_no_cb, yes_no_cb


def check_or_cancel_ikb(telegram_id):
    btn = InlineKeyboardMarkup()
    btn.add(
        InlineKeyboardButton(
            text="❌ Rad etish", callback_data=check_cancel_cb.new(
                action="cancel", value=telegram_id
            )
        ),
        InlineKeyboardButton(
            text="✅ Tasdiqlash", callback_data=check_cancel_cb.new(
                action="confirmation", value=telegram_id
            )
        )
    )
    return btn


def send_answer_ikb(telegram_id):
    btn = InlineKeyboardMarkup()
    btn.add(
        InlineKeyboardButton(
            text="✅ Javob berish", callback_data=answer_cb.new(
                action="answer", value=telegram_id
            )
        )
    )
    return btn


def yes_or_no_ikb():
    btn = InlineKeyboardMarkup()
    btn.add(
        InlineKeyboardButton(
            text="❌ Yo'q", callback_data=yes_or_no_cb.new(
                action="no"
            )
        ),
        InlineKeyboardButton(
            text="✅ Ha", callback_data=yes_or_no_cb.new(
                action="yes"
            )
        )
    )
    return btn


def yes_no_ikb():
    btn = InlineKeyboardMarkup()
    btn.add(
        InlineKeyboardButton(
            text="❌ Yo'q", callback_data=yes_no_cb.new(
                action="no"
            )
        ),
        InlineKeyboardButton(
            text="✅ Ha", callback_data=yes_no_cb.new(
                action="yes"
            )
        )
    )
    return btn


