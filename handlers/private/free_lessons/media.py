from aiogram import types

from handlers.private.free_lessons.pagination import change_page
from keyboards.inline.user.callbacks import free_lessons_cb
from keyboards.inline.user.ibuttons import category_free_ibtn
from loader import dp, lesdb
from utils.lessons import open_lesson, paginate


@dp.callback_query_handler(free_lessons_cb.filter(action="slctd"))
async def handle_free_lessons_slctd(call: types.CallbackQuery):
    await call.answer(cache_time=0)


@dp.callback_query_handler(free_lessons_cb.filter(action="no_slctd"), state="*")
async def handle_no_slctd(call: types.CallbackQuery, callback_data: dict):
    position = int(callback_data.get("value"))
    current_page = int(callback_data.get("c_pg"))

    await open_lesson(
        call=call, position=position, page=current_page, category_id=position
    )


@dp.callback_query_handler(free_lessons_cb.filter(action="next"))
@dp.callback_query_handler(free_lessons_cb.filter(action="prev"))
async def handle_free_lessons_prev(call: types.CallbackQuery, callback_data: dict):
    current_page = int(callback_data.get("c_pg"))
    action = callback_data.get("action")
    await change_page(
        call, current_page, action
    )


@dp.callback_query_handler(free_lessons_cb.filter(action="alert"))
async def handle_free_lessons_alert(call: types.CallbackQuery, callback_data: dict):
    current_page = callback_data.get("c_pg")
    await call.answer(text=f"Siz {current_page} - sahifadasiz!", show_alert=True)


@dp.callback_query_handler(free_lessons_cb.filter(action="back"))
async def handle_free_lessons_back(call: types.CallbackQuery):
    files = await lesdb.get_free_lessons_by_category()
    items, pages = paginate(files)

    await call.message.delete()
    await call.message.answer(
        text="Kerakli kategoriyani tanlang",
        reply_markup=category_free_ibtn(items[0], 1, pages)
    )
