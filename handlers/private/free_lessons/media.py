from aiogram import types
from aiogram.dispatcher import FSMContext

from handlers.private.free_lessons.pagination import change_page
from handlers.private.free_lessons.subcategories import start_free_subcategory
from keyboards.inline.user.callbacks import free_lessons_cb
from keyboards.inline.user.free import content_back_ikb
from loader import dp, lesdb


@dp.callback_query_handler(free_lessons_cb.filter(action="content"), state="*")
async def handle_no_slctd(call: types.CallbackQuery, callback_data: dict):
    await call.answer(cache_time=0)
    lesson_id = int(callback_data.get("value"))
    current_page = int(callback_data.get("c_pg"))
    lesson = await lesdb.get_lesson_by_lesson_id(lesson_id)

    subcategory_id = lesson[0]['subcategory_id']

    for media in lesson:
        if media['file_type'] == "video":
            await call.message.answer_video(
                video=media['file_id'],
                caption=media['caption'],
                protect_content=True,
                reply_markup=content_back_ikb(subcategory_id=subcategory_id, current_page=current_page)
            )
        elif media['file_type'] == "audio":
            await call.message.answer_audio(
                audio=media['file_id'],
                caption=media['caption'],
                protect_content=True,
                reply_markup=content_back_ikb(subcategory_id=subcategory_id, current_page=current_page)
            )
        elif media['file_type'] == "document":
            await call.message.answer_document(
                document=media['file_id'],
                caption=media['caption'],
                protect_content=True,
                reply_markup=content_back_ikb(subcategory_id=subcategory_id, current_page=current_page)
            )
        elif media['file_type'] == "voice":
            await call.message.answer_voice(
                voice=media['file_id'],
                caption=media['caption'],
                protect_content=True,
                reply_markup=content_back_ikb(subcategory_id=subcategory_id, current_page=current_page)
            )


@dp.callback_query_handler(free_lessons_cb.filter(action="next"))
@dp.callback_query_handler(free_lessons_cb.filter(action="prev"))
async def handle_free_lessons_prev(call: types.CallbackQuery, callback_data: dict):
    current_page = int(callback_data.get("c_pg"))
    action = callback_data.get("action")
    subcategory_id = int(callback_data.get("value"))

    await change_page(
        call=call, current_page=current_page, action=action, subcategory_id=subcategory_id
    )


@dp.callback_query_handler(free_lessons_cb.filter(action="alert"))
async def handle_free_lessons_alert(call: types.CallbackQuery, callback_data: dict):
    current_page = callback_data.get("c_pg")
    await call.answer(text=f"Siz {current_page} - sahifadasiz!", show_alert=True)


@dp.callback_query_handler(free_lessons_cb.filter(action="content_back"), state="*")
async def handle_content_back(call: types.CallbackQuery, state: FSMContext, callback_data: dict):
    await start_free_subcategory(call, state, callback_data, True)
