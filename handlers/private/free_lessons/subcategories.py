from aiogram import types
from aiogram.dispatcher import FSMContext

from handlers.private.free_lessons.main import free_lessons_main
from handlers.private.free_lessons.pagination import change_page_subcategory
from keyboards.inline.user.callbacks import free_subcat_cb, free_lessons_cb
from keyboards.inline.user.free import view_free_lessons_ikb, view_free_subcategories_ikb
from keyboards.inline.user.paid import view_paid_subcategories_ikb
from loader import dp, lesdb
from utils.helpers import extracter
from utils.lessons import paginate_category


@dp.callback_query_handler(free_subcat_cb.filter(action="subcategory"), state="*")
async def start_free_subcategory(call: types.CallbackQuery, state: FSMContext, callback_data: dict, back_content=False):
    await state.finish()



    subcategory_id = int(callback_data.get("value"))

    lessons = await lesdb.get_free_lessons(subcategory_id)

    items = extracter(lessons, 10)

    if not items:
        await call.answer(text="Bu subkategoriyada hozircha masala yo‘q.", show_alert=True)
        return

    await call.answer(cache_time=0)

    all_pages = len(items)

    key = view_free_lessons_ikb(
        items[0], 1, all_pages, subcategory_id
    )

    text = "Kerakli masalani tanlang"

    if back_content:
        await call.message.delete()
        await call.message.answer(
            text=text, reply_markup=key
        )
    else:
        await call.message.edit_text(
            text=text, reply_markup=key
        )


@dp.callback_query_handler(free_subcat_cb.filter(action="back"), state="*")
async def free_subcat_back(call: types.CallbackQuery, state: FSMContext):
    await state.finish()

    await free_lessons_main(call, state)


@dp.callback_query_handler(free_subcat_cb.filter(action="prev"))
@dp.callback_query_handler(free_subcat_cb.filter(action="next"))
async def free_subcat_prev_next(call: types.CallbackQuery, callback_data: dict):
    current_page = int(callback_data.get("value"))
    action = callback_data.get("action")
    category_id = int(callback_data.get("cat_id"))

    await change_page_subcategory(
        call, current_page, action, category_id
    )


@dp.callback_query_handler(free_subcat_cb.filter(action="alert"), state="*")
async def free_subcategory_alert(call: types.CallbackQuery, state: FSMContext, callback_data: dict):
    await state.finish()
    current_page = callback_data.get("value")
    await call.answer(text=f"Siz {current_page} - sahifadasiz!", show_alert=True)


@dp.callback_query_handler(free_lessons_cb.filter(action="back"), state="*")
async def free_subcategory_back(call: types.CallbackQuery, callback_data: dict, paid=False):
    subcategory_id = int(callback_data.get("value"))
    files = await lesdb.get_related_subcategories(subcategory_id)

    category_id = files[0]['category_id']
    items, pages = paginate_category(files)

    if paid:
        key = view_paid_subcategories_ikb(
            items[0], 1, pages, category_id
        )
    else:
        key = view_free_subcategories_ikb(
            items[0], 1, pages, category_id
        )

    await call.message.edit_text(
        text="Kerakli subkategoriyani tanlang",
        reply_markup=key
    )
