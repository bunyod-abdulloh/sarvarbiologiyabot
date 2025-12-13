import aiogram.utils.exceptions
from aiogram import types
from aiogram.dispatcher import FSMContext
from magic_filter import F

from keyboards.inline.user.callbacks import free_lessons_cb, free_less_cat_cb
from keyboards.inline.user.ibuttons import subscribe_ibtn, key_returner, category_free_ibtn
from loader import dp, lesdb
from utils.helpers import is_subscribed, extracter


@dp.callback_query_handler(F.data == "free_lessons", state="*")
async def handle_free_lessons_main(call: types.CallbackQuery, state: FSMContext):
    await state.finish()

    if await is_subscribed(call.from_user.id):
        text = ("Biz bilan birga ekanligingizdan xursandmiz! Marhamat darslarimizdan foydalanishingiz mumkin!\n\n"
                "Kerakli kategoriyani tanlang")

        files = await lesdb.get_free_lessons_by_category()

        items = extracter(files, 10)
        all_pages = len(items)

        key = category_free_ibtn(items[0], 1, all_pages)

        await call.message.edit_text(text=text, reply_markup=key)
    else:
        text = "Bepul darslarimizdan foydalanish uchun kanalimizga obuna bo'lishingiz lozim!"
        await call.message.edit_text(text=text, reply_markup=await subscribe_ibtn())


@dp.callback_query_handler(free_less_cat_cb.filter(action="category"), state="*")
async def handle_free_category_list(call: types.CallbackQuery, callback_data: dict):
    category_id = int(callback_data.get("value"))

    files = await lesdb.get_lessons_by_category_id(category_id)

    items = extracter(files, 10)

    file_type = items[0][0]['type']
    file_id = items[0][0]['file_id']
    caption = items[0][0]['caption']

    all_pages = len(items)

    key = key_returner(items=items[0], current_page=1, all_pages=all_pages, selected=1)

    if file_type == "video":
        await call.message.answer_video(
            video=file_id, caption=caption, reply_markup=key, protect_content=True
        )
    # elif file_type == "audio":
    #     await call.message.answer_audio(
    #         audio=file_id, caption=caption, reply_markup=key, protect_content=True
    #     )
    # elif file_type == "document":
    #     await call.message.answer_document(
    #         document=file_id, caption=caption, reply_markup=key, protect_content=True
    #     )
    # elif file_type == "photo":
    #     await call.message.answer_photo(
    #         photo=file_id, caption=caption, reply_markup=key, protect_content=True
    #     )


@dp.callback_query_handler(free_lessons_cb.filter(action="slctd"), state="*")
async def handle_free_slctd(call: types.CallbackQuery):
    await call.answer(cache_time=0)


@dp.callback_query_handler(free_lessons_cb.filter(action="no_slctd"), state="*")
async def handle_no_slctd(call: types.CallbackQuery, callback_data: dict):
    position = int(callback_data.get("value"))
    current_page = int(callback_data.get("c_pg"))

    files = await lesdb.get_lesson_free()

    extracted = extracter(files, 10)

    key = key_returner(items=extracted[current_page - 1], current_page=current_page, all_pages=len(extracted),
                       selected=position)

    lesson = await lesdb.get_lesson_by_position(position)

    file_type = lesson['type']
    file_id = lesson['file_id']
    caption = lesson['caption']

    if file_type == 'audio':
        await call.message.edit_media(
            media=types.InputMediaAudio(media=file_id, caption=caption),
            reply_markup=key
        )
    elif file_type == 'video':
        await call.message.edit_media(
            media=types.InputMediaVideo(media=file_id, caption=caption),
            reply_markup=key
        )


@dp.callback_query_handler(free_lessons_cb.filter(action="alert"), state="*")
async def handle_free_alert(call: types.CallbackQuery, callback_data: dict):
    current_page = callback_data.get("c_pg")
    await call.answer(
        text=f"Siz {current_page} - sahifadasiz!", show_alert=True
    )


@dp.callback_query_handler(free_lessons_cb.filter(action="prev"), state="*")
async def handle_free_prev(call: types.CallbackQuery, callback_data: dict):
    files = await lesdb.get_lesson_free()

    extracted = extracter(files, 10)

    all_pages = len(extracted)
    current_page = int(callback_data.get("c_pg"))
    try:
        if current_page == 1:
            current_page = all_pages
        else:
            current_page = current_page - 1

        position = extracted[current_page - 1][0]['position']

        key = key_returner(items=extracted[current_page - 1], current_page=current_page, all_pages=len(extracted),
                           selected=position)

        lesson = await lesdb.get_lesson_by_position(position)

        file_type = lesson['type']
        file_id = lesson['file_id']
        caption = lesson['caption']

        if file_type == 'audio':
            await call.message.edit_media(
                media=types.InputMediaAudio(media=file_id, caption=caption),
                reply_markup=key
            )
        elif file_type == 'video':
            await call.message.edit_media(
                media=types.InputMediaVideo(media=file_id, caption=caption),
                reply_markup=key
            )
    except aiogram.utils.exceptions.MessageNotModified:
        await call.answer(cache_time=0)


@dp.callback_query_handler(free_lessons_cb.filter(action="next"), state="*")
async def handle_free_prev(call: types.CallbackQuery, callback_data: dict):
    files = await lesdb.get_lesson_free()

    extracted = extracter(files, 10)

    all_pages = len(extracted)
    current_page = int(callback_data.get("c_pg"))

    if current_page == all_pages:
        current_page = 1
    else:
        current_page = current_page + 1

    try:
        position = extracted[current_page - 1][0]['position']

        key = key_returner(items=extracted[current_page - 1], current_page=current_page, all_pages=len(extracted),
                           selected=position)

        lesson = await lesdb.get_lesson_by_position(position)

        file_type = lesson['type']
        file_id = lesson['file_id']
        caption = lesson['caption']

        if file_type == 'audio':
            await call.message.edit_media(
                media=types.InputMediaAudio(media=file_id, caption=caption),
                reply_markup=key
            )
        elif file_type == 'video':
            await call.message.edit_media(
                media=types.InputMediaVideo(media=file_id, caption=caption),
                reply_markup=key
            )
    except aiogram.utils.exceptions.MessageNotModified:
        await call.answer(cache_time=0)
