from aiogram.utils.callback_data import CallbackData

free_lessons_cb = CallbackData("/", "action", "value", "c_pg")
free_less_cat_cb = CallbackData("cat", "action", "value")
paid_lessons_cb = CallbackData("paid_les", "action", "value", "c_pg")
paid_less_cat_cb = CallbackData("paid_cat", "action", "value")
