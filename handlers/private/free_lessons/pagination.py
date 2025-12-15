import aiogram.utils.exceptions
from aiogram import types

from keyboards.inline.user.ibuttons import category_free_ibtn
from loader import lesdb
from utils.lessons import paginate, open_lesson


async def change_page(
        call: types.CallbackQuery,
        current_page: int,
        action: str
):
    """
    Free lessons pagination
    """
    files = await lesdb.get_lesson_free()
    items, total_pages = paginate(files)

    if not items:
        await call.answer("Darslar topilmadi", show_alert=True)
        return

    if action == "prev":
        new_page = current_page - 1
    else:
        new_page = current_page + 1

    if new_page < 1:
        new_page = total_pages
    elif new_page > total_pages:
        new_page = 1

    lesson = items[new_page - 1][0]
    try:
        await open_lesson(call, lesson["position"], new_page)
    except aiogram.utils.exceptions.MessageNotModified:
        await call.answer(cache_time=0)
        pass


# =========================
# CATEGORY PAGINATION
# =========================

async def change_page_category(
        call: types.CallbackQuery,
        current_page: int,
        action: str
):
    """
    Category ichidagi darslar uchun pagination
    """

    files = await lesdb.get_free_lessons_by_category()
    items, total_pages = paginate(files)

    if not items:
        await call.answer("Bu kategoriyada darslar yo‘q", show_alert=True)
        return

    if action == "prev":
        new_page = current_page - 1
    else:
        new_page = current_page + 1

    if new_page < 1:
        new_page = total_pages
    elif new_page > total_pages:
        new_page = 1

    key = category_free_ibtn(
        items=items[new_page - 1], current_page=new_page, all_pages=total_pages
    )

    try:
        await call.message.edit_text(
            text="Kerakli kategoriyani tanlang", reply_markup=key
        )
    except aiogram.utils.exceptions.MessageNotModified:
        await call.answer(cache_time=0)
        pass
