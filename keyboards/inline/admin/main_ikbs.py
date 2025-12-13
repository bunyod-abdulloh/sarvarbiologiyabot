from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def check_or_cancel_ikb(telegram_id):
    btn = InlineKeyboardMarkup()
    btn.add(
        InlineKeyboardButton(
            text="❌ Rad etish", callback_data=f"cancel_{telegram_id}"
        ),
        InlineKeyboardButton(
            text="✅ Tasdiqlash", callback_data=f"confirmation_{telegram_id}"
        )
    )
    return btn
