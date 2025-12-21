from aiogram import types

from handlers.private.free_lessons.pagination import change_page
from keyboards.inline.user.callbacks import free_lessons_cb
from keyboards.inline.user.ibuttons import category_free_ibtn, content_back_ikb
from loader import dp, lesdb
from utils.lessons import paginate_category


@dp.callback_query_handler(free_lessons_cb.filter(action="content"), state="*")
async def handle_no_slctd(call: types.CallbackQuery, callback_data: dict):
    await call.answer(cache_time=0)
    lesson_id = int(callback_data.get("value"))
    current_page = int(callback_data.get("c_pg"))
    lesson = await lesdb.get_lesson_by_lesson_id(lesson_id)

    for media in lesson:
        if media['file_type'] == "video":
            await call.message.answer_video(
                video=media['file_id'],
                caption=media['caption'],
                protect_content=True,
                reply_markup=content_back_ikb(category_id=lesson_id, current_page=current_page)
            )
        elif media['file_type'] == "audio":
            await call.message.answer_audio(
                audio=media['file_id'],
                caption=media['caption'],
                protect_content=True,
                reply_markup=content_back_ikb(category_id=lesson_id, current_page=current_page)
            )
        elif media['file_type'] == "document":
            await call.message.answer_document(
                document=media['file_id'],
                caption=media['caption'],
                protect_content=True,
                reply_markup=content_back_ikb(category_id=lesson_id, current_page=current_page)
            )
        elif media['file_type'] == "voice":
            await call.message.answer_voice(
                voice=media['file_id'],
                caption=media['caption'],
                protect_content=True,
                reply_markup=content_back_ikb(category_id=lesson_id, current_page=current_page)
            )


@dp.callback_query_handler(free_lessons_cb.filter(action="next"))
@dp.callback_query_handler(free_lessons_cb.filter(action="prev"))
async def handle_free_lessons_prev(call: types.CallbackQuery, callback_data: dict):
    current_page = int(callback_data.get("c_pg"))
    action = callback_data.get("action")
    category_id = int(callback_data.get("value"))

    await change_page(
        call=call, current_page=current_page, action=action, category_id=category_id
    )


@dp.callback_query_handler(free_lessons_cb.filter(action="alert"))
async def handle_free_lessons_alert(call: types.CallbackQuery, callback_data: dict):
    current_page = callback_data.get("c_pg")
    await call.answer(text=f"Siz {current_page} - sahifadasiz!", show_alert=True)


@dp.callback_query_handler(free_lessons_cb.filter(action="back"))
async def handle_free_lessons_back(call: types.CallbackQuery):
    files = await lesdb.get_free_lessons_by_category()
    items, pages = paginate_category(files)

    await call.message.edit_text(
        text="Kerakli kategoriyani tanlang",
        reply_markup=category_free_ibtn(items[0], 1, pages)
    )


@dp.callback_query_handler(free_lessons_cb.filter(action="content_back"), state="*")
async def handle_content_back(call: types.CallbackQuery, callback_data: dict):
    current_page = int(callback_data.get("c_pg"))
    lesson_id = int(callback_data.get("value"))

    category_id = await lesdb.get_lesson_category_id_by_lesson_id(lesson_id)

    await change_page(
        call=call, current_page=current_page, action="next", category_id=category_id
    )
