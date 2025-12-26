from aiogram import types
from aiogram.dispatcher import FSMContext
from magic_filter import F

from keyboards.inline.user.free import category_free_ibtn
from keyboards.inline.user.main import subscribe_ibtn
from loader import dp, lesdb
from utils.helpers import is_subscribed
from utils.lessons import paginate_category


@dp.callback_query_handler(F.data == "free_lessons", state="*")
async def free_lessons_main(call: types.CallbackQuery, state: FSMContext):
    await state.finish()

    if not await is_subscribed(call.from_user.id):
        await call.message.edit_text(
            "Bepul darslarimizdan foydalanish uchun kanalga obuna bo‘ling!",
            reply_markup=await subscribe_ibtn()
        )
        return

    files = await lesdb.get_free_categories()

    if files:
        items, pages = paginate_category(files)

        await call.message.edit_text(
            text="Kerakli kategoriyani tanlang",
            reply_markup=category_free_ibtn(items[0], 1, pages)
        )
    else:
        await call.answer(
            text="Hozircha darslar joylanmadi!", show_alert=True
        )
