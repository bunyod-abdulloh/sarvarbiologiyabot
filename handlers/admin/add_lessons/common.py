def build_categories_text(categories):
    text = "Mavjud kategoriyalar:\n\n"
    text += "\n".join(
        f"{i}. {c['name']}" for i, c in enumerate(categories, 1)
    )
    return text
