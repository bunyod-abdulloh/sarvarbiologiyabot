from aiogram.types import ReplyKeyboardMarkup


def admin_main_dkb():
    kb = ReplyKeyboardMarkup(resize_keyboard=True)
    kb.row("😎 Umumiy foydalanuvchilar soni")
    kb.row("💸 Pullik foydalanuvchilar")
    kb.row("✅ Oddiy e'lon yuborish")
    kb.row("🎥 Media e'lon yuborish")
    kb.row("💰 Pullik dars qo'shish")
    kb.row("🆓 Bepul dars qo'shish")
    # kb.row("📝 Darslarni o'zgartirish")
    kb.row("🏡 Bosh sahifa")
    return kb
