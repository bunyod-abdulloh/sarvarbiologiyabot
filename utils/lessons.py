from aiogram import types


def paginate(files, per_page=50):
    from utils.helpers import extracter
    items = extracter(files, per_page)
    return items, len(items)


def get_file_id_caption(message: types.Message):
    file_id = None
    file_type = None

    if message.video:
        file_id = message.video.file_id
        file_type = "video"
    elif message.audio:
        file_id = message.audio.file_id
        file_type = "audio"
    elif message.document:
        file_id = message.document.file_id
        file_type = "document"
    elif message.voice:
        file_id = message.voice.file_id
        file_type = "voice"

    caption = message.caption

    return file_id, file_type, caption


import re
import unicodedata

DIGIT_MAP = {
    "0️⃣": "0", "1️⃣": "1", "2️⃣": "2", "3️⃣": "3", "4️⃣": "4",
    "5️⃣": "5", "6️⃣": "6", "7️⃣": "7", "8️⃣": "8", "9️⃣": "9",
}

def extract_masala_number(text: str) -> str | None:
    if not text:
        return None

    # Unicode normallashtirish
    text = unicodedata.normalize("NFKD", text)

    # 👉 faqat OXIRGI bo‘sh bo‘lmagan qator
    lines = [l.strip() for l in text.splitlines() if l.strip()]
    last_line = lines[-1] if lines else ""

    # emoji raqamlarni oddiy raqamga aylantiramiz
    for k, v in DIGIT_MAP.items():
        last_line = last_line.replace(k, v)

    # tirelarni normallashtiramiz
    last_line = last_line.replace("➖", "-").replace("–", "-").replace("—", "-")

    # ===============================
    # 1️⃣ ORALIQ (33-35-MASALA)
    # ===============================
    range_match = re.search(r"(\d+)\s*-\s*(\d+)", last_line)
    if range_match:
        return f"{range_match.group(1)}-{range_match.group(2)}"

    # ===============================
    # 2️⃣ BITTA SON yoki O‘NLIK
    # ===============================
    left = last_line.split("-", 1)[0]
    digits = re.findall(r"\d", left)

    if not digits:
        return None

    # bitta raqam + ➖  → 40
    if len(digits) == 1 and "-" in last_line:
        return digits[0] + "0"

    # oddiy holat: 42
    return "".join(digits)
