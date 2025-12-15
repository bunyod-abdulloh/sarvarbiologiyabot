from aiogram.utils.callback_data import CallbackData

check_cancel_cb = CallbackData("/", "action", "value")
answer_cb = CallbackData("--", "action", "value")
yes_or_no_cb = CallbackData("yno", "action")
yes_no_cb = CallbackData("yesno", "action")
