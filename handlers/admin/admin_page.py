import asyncio

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command
from magic_filter import F

from filters.admins import IsBotAdminFilter
from handlers.private.start import bot_start
from keyboards.default.admin.main import admin_main_dkb
from loader import dp, udb, admdb
from states.admin import AdminStates
from utils.db_functions import send_message_to_users
from utils.helpers import album_tasks, albums, finalize_album
from utils.misc import rate_limit

WARNING_TEXT = (
    "Xabar yuborishdan oldin postingizni yaxshilab tekshirib oling!\n\n"
    "Imkoni bo'lsa postingizni oldin tayyorlab olib keyin yuboring.\n\n"
    "Xabaringizni kiriting:"
)

ALERT_TEXT = "Xabar yuborish jarayoni yoqilgan! Hisobot kelganidan so'ng xabar yuborishingiz mumkin!"


@dp.message_handler(IsBotAdminFilter(), F.text == "◀️ Ortga", state="*")
@dp.message_handler(IsBotAdminFilter(), F.text == "🔙 Ortga", state="*")
@dp.message_handler(IsBotAdminFilter(), F.text == "⬅️ Ortga", state="*")
@dp.message_handler(IsBotAdminFilter(), Command(commands="admin"), state="*")
async def admin_main_page(message: types.Message, state: FSMContext):
    await state.finish()
    await message.answer("Admin panel", reply_markup=admin_main_dkb())


@dp.message_handler(IsBotAdminFilter(), F.text == "🏡 Bosh sahifa", state="*")
async def back_to_main_page(message: types.Message, state: FSMContext):
    await bot_start(message, state)


@dp.message_handler(IsBotAdminFilter(), F.text == "😎 Foydalanuvchilar soni")
async def user_count(message: types.Message):
    count = await udb.count_users()
    await message.answer(f"Umumiy foydalanuvchilar soni: {count}")


@dp.message_handler(IsBotAdminFilter(), F.text == "✅ Oddiy e'lon yuborish", state="*")
async def send_to_bot_users(message: types.Message, state: FSMContext):
    await state.finish()
    send_status = await admdb.get_send_status()
    if send_status is True:
        await message.answer(ALERT_TEXT)
    else:
        await message.answer(text=WARNING_TEXT)
        await AdminStates.SEND_TO_USERS.set()


@dp.message_handler(state=AdminStates.SEND_TO_USERS, content_types=types.ContentTypes.ANY)
async def send_to_bot_users_two(message: types.Message, state: FSMContext):
    await state.finish()
    await message.answer(text="Xabar yuborish boshlandi...", reply_markup=types.ReplyKeyboardRemove())
    success, failed = await send_message_to_users(message=message)
    await message.answer(text=f"Xabar yuborildi!\n\nYuborildi: {success}\nYuborilmadi: {failed}")


@dp.message_handler(IsBotAdminFilter(), F.text == "🎥 Media e'lon yuborish", state="*")
async def send_media_to_bot(message: types.Message, state: FSMContext):
    await state.finish()
    send_status = await admdb.get_send_status()
    if send_status is True:
        await message.answer(ALERT_TEXT)
    else:
        await message.answer(text=WARNING_TEXT)
        await AdminStates.SEND_MEDIA_TO_USERS.set()


@dp.message_handler(
    state=AdminStates.SEND_MEDIA_TO_USERS,
    content_types=types.ContentTypes.ANY
)
@rate_limit(0)
async def collect_album(message: types.Message, state: FSMContext):
    if not message.media_group_id:
        await message.answer("Media group yuboring")
        return

    gid = message.media_group_id
    albums[gid].append(message)

    # Agar oldingi task bo‘lsa — bekor qilamiz
    if gid in album_tasks:
        album_tasks[gid].cancel()

    album_tasks[gid] = asyncio.create_task(
        finalize_album(gid, message, state)
    )
