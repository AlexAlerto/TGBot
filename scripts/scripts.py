from telegram.ext import ContextTypes

from konspect_bot import send_log
from scripts import messages, conf


async def check_if_user_in_black_white_list(update, context: ContextTypes.DEFAULT_TYPE, user_name) -> bool:
    # Если человек в "стоп" лист, то он не может заходить в бота
    if user_name in conf.get_black_list():
        await send_log(context, message=messages.get_log("tap_on_start_but_user_in_black_list", user_name))
        await update.message.reply_text(messages.get_message("user_in_black_list"))
        return False

    # Если человека нет в белом лист, то он не может заходить в бота
    elif user_name not in conf.get_white_list():
        await send_log(context, message=messages.get_log("tap_on_start_but_user_not_in_white_list", user_name))
        await update.message.reply_text(messages.get_message("user_not_in_white_list"))
        return False

    else:
        return True
