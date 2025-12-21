import aiogram.utils.exceptions
from aiogram import types

from keyboards.inline.user.ibuttons import category_free_ibtn, view_free_lessons_ikb, category_paid_ibtn, \
    view_paid_lessons_ikb
from loader import lesdb
from utils.lessons import paginate_category


async def change_page(
        call: types.CallbackQuery,
        current_page: int,
        action: str,
        category_id: int,
        paid=False
):
    if paid:
        files = await lesdb.get_lessons_paid_by_category_id(category_id)
    else:
        files = await lesdb.get_lessons_by_category_id(category_id)
    items, total_pages = paginate_category(files)

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

    if paid:
        key = view_paid_lessons_ikb(
            items[new_page - 1], new_page, total_pages, category_id
        )
    else:
        key = view_free_lessons_ikb(
            items[new_page - 1], new_page, total_pages, category_id
        )

    try:
        await call.message.edit_text(
            text="Kerakli masalani tanlang", reply_markup=key
        )
    except aiogram.utils.exceptions.MessageNotModified:
        await call.answer(cache_time=0)
        pass
    except aiogram.utils.exceptions.BadRequest:
        await call.message.delete()
        await call.message.answer(
                    text="Kerakli masalani tanlang", reply_markup=key
                )

# =========================
# CATEGORY PAGINATION
# =========================

async def change_page_category(
        call: types.CallbackQuery,
        current_page: int,
        action: str,
        paid=False
):
    """
    Category ichidagi darslar uchun pagination
    """
    if paid:
        files = await lesdb.get_paid_lessons_by_category()
    else:
        files = await lesdb.get_free_lessons_by_category()
    items, total_pages = paginate_category(files)

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

    if paid:
        key = category_paid_ibtn(
            items=items[new_page - 1], current_page=new_page, all_pages=total_pages
        )
    else:
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
