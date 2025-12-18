def build_categories_text(categories):
    text = "Kategoriyalar\n\n"
    for c in categories:
        text += f"{c['id']}. {c['name']}\n"
    return text


def build_lessons_text(lessons):
    text = "Masalalar ro'yxati\n\n"
    for l in lessons:
        text += f"{l['file_row_id']}. {l['caption']}\n"
    return text
