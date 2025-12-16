from aiogram import types

from handlers.private.free_lessons.pagination import change_page
from keyboards.inline.user.callbacks import paid_lessons_cb
from keyboards.inline.user.ibuttons import category_paid_ibtn, \
    content_paid_back_ikb
from loader import dp, lesdb
from utils.lessons import paginate


@dp.callback_query_handler(paid_lessons_cb.filter(action="paid_content"), state="*")
async def handle_no_slctd(call: types.CallbackQuery, callback_data: dict):
    await call.answer(cache_time=0)
    lesson_id = int(callback_data.get("value"))
    current_page = int(callback_data.get("c_pg"))
    lesson = await lesdb.get_paid_lesson(lesson_id)

    for media in lesson:
        if media['file_type'] == "video":
            await call.message.answer_video(
                video=media['file_id'],
                caption=media['caption'],
                protect_content=True,
                reply_markup=content_paid_back_ikb(category_id=lesson_id, current_page=current_page)
            )


@dp.callback_query_handler(paid_lessons_cb.filter(action="pd_next"))
@dp.callback_query_handler(paid_lessons_cb.filter(action="pd_prev"))
async def handle_free_lessons_prev(call: types.CallbackQuery, callback_data: dict):
    current_page = int(callback_data.get("c_pg"))
    action = callback_data.get("action")
    category_id = int(callback_data.get("value"))

    await change_page(
        call=call, current_page=current_page, action=action, category_id=category_id, paid=True
    )


@dp.callback_query_handler(paid_lessons_cb.filter(action="pd_alert"))
async def handle_paid_lessons_alert(call: types.CallbackQuery, callback_data: dict):
    current_page = callback_data.get("c_pg")
    await call.answer(text=f"Siz {current_page} - sahifadasiz!", show_alert=True)


@dp.callback_query_handler(paid_lessons_cb.filter(action="pd_back"))
async def handle_paid_lessons_back(call: types.CallbackQuery):
    files = await lesdb.get_paid_lessons_by_category()
    items, pages = paginate(files)

    await call.message.edit_text(
        text="Kerakli kategoriyani tanlang",
        reply_markup=category_paid_ibtn(items[0], 1, pages)
    )


@dp.callback_query_handler(paid_lessons_cb.filter(action="paid_content_back"), state="*")
async def handle_content_back_paid(call: types.CallbackQuery, callback_data: dict):
    current_page = int(callback_data.get("c_pg"))
    lesson_id = int(callback_data.get("value"))

    category_id = await lesdb.get_paid_categories(lesson_id)

    await change_page(
        call=call, current_page=current_page, action="next", category_id=category_id, paid=True
    )
