def build_categories_text(categories):
    text = "Kategoriyalar\n\n"

    for c in categories:
        text += f"{c['id']}. {c['name']}\n"
    return text


def build_subcategories_text(subcategories):
    text = "Subkategoriyalar\n\n"
    for s in subcategories:
        text += f"{s['id']}. {s['name']}\n"
    return text


def build_lessons_text(lessons):
    text = "Masalalar ro'yxati\n\n"
    for l in lessons:
        text += f"{l['file_row_id']}. {l['caption']}\n"
    return text


def build_lessons_text_admin(lessons, delete=False):
    text = "Masalalar ro'yxati\n\n"

    if delete:
        for l in lessons:
            text += f"ID: {l['ls_id']}\nMasala tartib raqami: {l['lesson_number']}\nTa'rifi: {l['caption']}\n\n"
    else:
        for l in lessons:
            text += f"ID: {l['lesson_id']}\nMasala tartib raqami: {l['lesson_number']}\nTa'rifi: {l['caption']}\n\n"
    return text
