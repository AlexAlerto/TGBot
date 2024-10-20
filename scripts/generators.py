import os
from telegram import InlineKeyboardButton


# Функция для генерации клавиатуры
def keyboard_generator(path: str, base_path="files/"):
    keyboard = []
    new_path = base_path

    # Построение нового пути на основе переданного индекса
    path_parts = path.split('/')
    for number in path_parts:
        if number.isdigit():
            files2 = os.listdir(new_path)
            if int(number) < len(files2):
                selected_item = files2[int(number)]
                new_path += selected_item

                # Проверка, что это папка, прежде чем добавлять "/"
                if os.path.isdir(new_path):
                    new_path += "/"
                else:
                    break  # Если это файл, прерываем цикл, чтобы не добавлять дальше

    # Получаем список файлов и директорий, если это папка
    files = os.listdir(new_path) if os.path.isdir(new_path) else []

    # Добавляем файлы и папки на клавиатуру
    for index, file in enumerate(files):
        full_path = os.path.join(new_path, file)

        if os.path.isfile(full_path):  # Это файл
            keyboard.append([InlineKeyboardButton(file, callback_data=f"{path}{index}/{file}")])
        elif os.path.isdir(full_path):  # Это папка
            keyboard.append([InlineKeyboardButton(file, callback_data=f"{path}{index}/")])

    # Добавляем кнопку "Назад", если мы не в корневой папке
    if path != '':
        keyboard.append([InlineKeyboardButton("◀️ Главное меню", callback_data="back_to_main")])

    return keyboard

def convert_relative_to_full_path(relative_path: str, base_path="files/"):
    new_path = base_path
    path_parts = relative_path.split('/')  # Разбиваем относительный путь на части (индексы)

    for number in path_parts[:-1]:  # Проходим по всем частям пути, кроме последней (файл)
        if number.isdigit():
            files = os.listdir(new_path)  # Получаем список файлов и папок в текущей директории
            if int(number) < len(files):  # Проверяем, что индекс допустим
                selected_item = files[int(number)]
                new_path = os.path.join(new_path, selected_item)  # Строим новый путь

    # Обработка последней части пути - файла
    last_part = path_parts[-1]  # Имя файла или папки
    if last_part and os.path.isdir(new_path):  # Проверяем, что это директория
        files = os.listdir(new_path)
        if last_part in files:
            new_path = os.path.join(new_path, last_part)

    # Нормализуем путь для корректной работы на Windows (замена обратных слэшей)
    return os.path.normpath(new_path)
