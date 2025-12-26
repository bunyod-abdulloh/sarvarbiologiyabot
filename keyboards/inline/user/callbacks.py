from aiogram.utils.callback_data import CallbackData


free_less_cat_cb = CallbackData("cat", "action", "value")
free_subcat_cb = CallbackData('frsub', 'action', 'value', 'cat_id')
free_lessons_cb = CallbackData("/", "action", "value", "c_pg")

paid_lessons_cb = CallbackData("paid_les", "action", "value", "c_pg")
paid_subcat_cb = CallbackData('pdsub', 'action', 'value', 'cat_id')
paid_less_cat_cb = CallbackData("paid_cat", "action", "value")
