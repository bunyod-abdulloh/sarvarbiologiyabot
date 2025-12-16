from aiogram import types
from aiogram.dispatcher import FSMContext
from magic_filter import F

from keyboards.inline.user.ibuttons import category_paid_ibtn
from loader import dp, pdb, lesdb
from utils.lessons import paginate


@dp.callback_query_handler(F.data == "paid_lessons", state="*")
async def handle_paid_lessons_main(call: types.CallbackQuery, state: FSMContext):
    await state.finish()
    user = await pdb.check_paid_user(call.from_user.id)

    if user:
        files = await lesdb.get_paid_lessons_by_category()
        items, pages = paginate(files)

        await call.message.edit_text(
            text="Kerakli kategoriyani tanlang",
            reply_markup=category_paid_ibtn(items[0], 1, pages)
        )
    else:
        await call.message.edit_text(
            text="Ushbu darslarimizdan foydalanish uchun quyidagi kartamizga to'lov qilishingiz lozim:"
                 "\n\n<code>123456789</code>\n\n<b>FALONCHI FALONCHIYEV</b>\n\nTo'lov qilib bo'lganingizdan so'ng chekni "
                 "skrin qilib <b>Adminga xabar</b> bo'limiga yuboring. Admin to'lovni tekshirib tasdiqlasa, Sizga darslarni "
                 "ochib qo'yadi"
        )
