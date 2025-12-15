from aiogram import types
from aiogram.dispatcher import FSMContext

from handlers.private.free_lessons.pagination import change_page_category
from keyboards.inline.user.callbacks import free_less_cat_cb
from keyboards.inline.user.ibuttons import key_returner, main_page_ibtn
from loader import dp, lesdb
from utils.helpers import extracter
from utils.lessons import send_media


@dp.callback_query_handler(free_less_cat_cb.filter(action="category"), state="*")
async def open_free_category(call: types.CallbackQuery, callback_data: dict):
    """
    Kategoriya bosilganda:
    - shu kategoriya darslarini oladi
    - birinchi darsni ko‘rsatadi
    """
    await call.answer(cache_time=0)

    category_id = int(callback_data["value"])

    files = await lesdb.get_lessons_by_category_id(category_id)

    items = extracter(files, 10)

    if not items:
        await call.message.answer("Bu kategoriyada hozircha dars yo‘q.")
        return

    first = items[0][0]
    all_pages = len(items)

    key = key_returner(
        items=items[0],
        current_page=1,
        all_pages=all_pages,
        selected=first["row_number"]
    )

    await send_media(call.message, first, key)


@dp.callback_query_handler(free_less_cat_cb.filter(action="back"), state="*")
async def back_to_main_page(call: types.CallbackQuery, state: FSMContext):
    """
    Bosh sahifaga qaytish
    """
    await state.finish()

    await call.message.edit_text(
        text="Bosh sahifa", reply_markup=main_page_ibtn()
    )


@dp.callback_query_handler(free_less_cat_cb.filter(action="prev"))
@dp.callback_query_handler(free_less_cat_cb.filter(action="next"))
async def handle_free_less_cat_prev(call: types.CallbackQuery, callback_data: dict):
    current_page = int(callback_data.get("value"))
    action = callback_data.get("action")
    await change_page_category(
        call, current_page, action
    )


@dp.callback_query_handler(free_less_cat_cb.filter(action="alert"))
async def handle_free_les_cat_alert(call: types.CallbackQuery, callback_data: dict):
    current_page = callback_data.get("value")
    await call.answer(text=f"Siz {current_page} - sahifadasiz!", show_alert=True)
