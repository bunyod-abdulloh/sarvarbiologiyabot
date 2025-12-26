from aiogram.types import ReplyKeyboardMarkup


def admin_main_dkb():
    kb = ReplyKeyboardMarkup(resize_keyboard=True)
    kb.row("😎 Foydalanuvchilar soni")
    kb.row("✅ Oddiy e'lon yuborish")
    kb.row("🎥 Media e'lon yuborish")
    kb.row("✅ Dars qo'shish", "♻️ Dars o'zgartirish")
    kb.row("🗑 Dars o'chirish")
    kb.row("🏡 Bosh sahifa")
    return kb


def admin_add_dkb():
    kb = ReplyKeyboardMarkup(resize_keyboard=True)
    kb.row("🆓 Bepul")
    kb.row("⬅️ Ortga")
    return kb


def admin_edit_dkb():
    kb = ReplyKeyboardMarkup(resize_keyboard=True)
    kb.row("♻️ Kategoriya", "♻️ Subkategoriya")
    kb.row("♻️ Dars")
    kb.row("🔙 Ortga")
    return kb


def admin_delete_dkb():
    kb = ReplyKeyboardMarkup(resize_keyboard=True)
    kb.row("🗑 Kategoriya", "🗑 Subkategoriya")
    kb.row("🗑 Dars")
    kb.row("◀️ Ortga")
    return kb
