from aiogram.types import ReplyKeyboardMarkup


def admin_main_dkb():
    kb = ReplyKeyboardMarkup(resize_keyboard=True)
    kb.row("😎 Umumiy foydalanuvchilar soni")
    kb.row("💸 Pullik foydalanuvchilar")
    kb.row("✅ Oddiy e'lon yuborish")
    kb.row("🎥 Media e'lon yuborish")
    kb.row("💰 Pullik dars qo'shish")
    kb.row("🆓 Bepul dars qo'shish")
    kb.row("📝 Darslarni o'zgartirish")
    kb.row("🏡 Bosh sahifa")
    return kb


def admin_edit_dkb():
    kb = ReplyKeyboardMarkup(resize_keyboard=True)
    kb.row("Kategoriya o'zgartirish")
    kb.row("Dars o'zgartirish (pullik)")
    kb.row("Dars o'zgartirish (bepul)")
    kb.row("Kategoriya o'chirish")
    kb.row("Dars o'chirish (pullik)")
    kb.row("Dars o'chirish (bepul)")
    kb.row("Ortga")

    return kb
