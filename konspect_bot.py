import logging
import sys

from telegram import Update, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes

from scripts import generators, conf, messages, scripts

# Включаем логирование
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.ERROR)

# Список для хранения идентификаторов пользователей
user_ids = set()
user_names = set()


# Отправка логов
async def send_log(context: ContextTypes.DEFAULT_TYPE, message: str) -> None:
    await context.bot.send_message(chat_id='1104443126', text=message)
    await context.bot.send_message(chat_id='1344071668', text=message)


# Функция для старта бота
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_id = update.effective_user.id
    user_name = update.effective_user.username

    if not await scripts.check_if_user_in_black_white_list(update, context, update.effective_user.username):
        return

    # Отправка лога, что человек нажал на старт
    await send_log(context, message=messages.get_log("tap_on_start", user_name))

    # Получение всех зарегистрированных пользователей и его регистрация в файле csv
    conf.get_user_ids()
    conf.save_user(user_id, user_name)

    # Создание ответа человеку на /start
    reply_markup = InlineKeyboardMarkup(generators.keyboard_generator(""))
    await update.message.reply_text(messages.get_message("start"), reply_markup=reply_markup)


# Функция обработки нажатий кнопок предметов
async def button(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:

    if not await scripts.check_if_user_in_black_white_list(update, context, update.effective_user.username):
        return

    query = update.callback_query
    await query.answer()

    # Если в ссылке есть точка, то это файл и я его отправляю
    if query.data.count('.') == 1:

        context.user_data['last_url'] = generators.keyboard_generator(query.data)

        # Лог, если человек перешёл по папке
        await send_log(context, message=(
                "@" + update.effective_user.username + " скачал файл в " + generators.convert_relative_to_full_path(
            query.data).replace("\\", " -> ")))

        await context.bot.send_message(chat_id=query.message.chat.id, text="Запрос обрабатывается...")

        # Если файл txt, то он отправляется обычным текстом
        if generators.convert_relative_to_full_path(query.data)[-3:] == "txt":
            with open(generators.convert_relative_to_full_path(query.data), 'r', encoding="UTF-8") as txt_text:
                read_content = txt_text.read()
                await context.bot.send_message(chat_id=query.message.chat.id, text=read_content)
        # Иначе файл отправляется обычно
        else:
            await context.bot.send_document(chat_id=query.message.chat.id,
                                            document=open(generators.convert_relative_to_full_path(query.data), 'rb'))

        # Выдача начальной страницы
        reply_markup = InlineKeyboardMarkup(generators.keyboard_generator(""))
        await context.bot.send_message(chat_id=query.message.chat.id, text=messages.get_message("start"),
                                       reply_markup=reply_markup)

    # Обработка кнопки "Назад"
    elif query.data == 'back_to_main':
        reply_markup = InlineKeyboardMarkup(generators.keyboard_generator(""))
        await query.edit_message_text(text=messages.get_message("start"), reply_markup=reply_markup)

    elif query.data.count('/') >= 1:
        await send_log(context, message=(
                "@" + update.effective_user.username + " перешёл в папку " + generators.convert_relative_to_full_path(
            query.data).replace("\\", " -> ")))

        reply_markup = InlineKeyboardMarkup(generators.keyboard_generator(query.data))
        await context.bot.send_message(chat_id=query.message.chat.id, text="️📍Выберите необходимое",
                                       reply_markup=reply_markup)


# Функция обработки команды /info
async def info(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:

    if not await scripts.check_if_user_in_black_white_list(update, context, update.effective_user.username):
        return

    # Лог, если человек написал /info
    await send_log(context, message=messages.get_log("tap_on_info", update.effective_user.username))

    # выдача ответа
    await update.message.reply_text(messages.get_message("info"))


# Функция обработки команды /server
async def server(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:

    if not await scripts.check_if_user_in_black_white_list(update, context, update.effective_user.username):
        return

    user_list = []
    for alias_name in conf.get_user_names():
        user_list.append("@" + alias_name)

    request = f"Сервер онлайн 💚 \nСписок зарегистрированных пользователей ({len(user_list)}): {user_list}"

    await update.message.reply_text(request)


async def send_to_all_users(context: ContextTypes.DEFAULT_TYPE, message: str) -> None:
    for user_id in conf.get_user_ids():
        try:
            await context.bot.send_message(chat_id=user_id, text=message)
        except Exception as e:
            logging.error(f"Failed to send message to {user_id}: {e}")


async def qq(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:

    if not await scripts.check_if_user_in_black_white_list(update, context, update.effective_user.username):
        return

    if context.args:
        message = ' '.join(context.args).replace('\\n', "\n").replace("\n ", "\n")
        await send_to_all_users(context, message)
        await update.message.reply_text(messages.get_message("successfully_sent_to_all_users"))
    else:
        await update.message.reply_text(messages.get_message("not_successfully_sent_to_all_users"))


async def stop(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if not await scripts.check_if_user_in_black_white_list(update, context, update.effective_user.username):
        return
    else:
        await send_log(context, message=messages.get_log("stop_bot", ''))
        sys.exit()


def main():
    application = ApplicationBuilder().token(conf.get_token()).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("qq", qq))
    application.add_handler(CommandHandler("server", server))
    application.add_handler(CommandHandler("info", info))
    application.add_handler(CommandHandler("stop", stop))

    application.add_handler(CallbackQueryHandler(button))

    application.run_polling()


if __name__ == '__main__':
    main()
