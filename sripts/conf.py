import configparser, csv, datetime

config = configparser.ConfigParser()

config.read("Configs/Conf.ini")
TOKEN = config["Settings"]["TOKEN"]

def get_white_list() -> list:
    config.read("Configs/Lists.ini")
    return config["Lists"]["white_list"].split(",")

def get_admin_list() -> list:
    config.read("Configs/Lists.ini")
    return config["Lists"]["admin_list"].split(",")

def add_black_list(username):
    config.read("Configs/Lists.ini")
    new_black_list = set(config["Lists"]["black_list"].split(","))
    new_black_list.add(str(username))
    config.set('Lists', 'black_list', str(new_black_list).replace('\'', '').replace('{', '').replace('}', '').replace(' ', ''))
    with open('Configs/Lists.ini', 'w') as configfile:
        config.write(configfile)

def get_black_list() -> list:
    config.read("Configs/Lists.ini")
    return config["Lists"]["black_list"].split(",")


def get_user_ids():
    user_ids = set()
    # чтение user_id в csv файле
    with open("DB.csv", newline="", encoding="utf-8") as csvfile:
        reader = csv.DictReader(csvfile, delimiter=",")
        for row in reader:
            user_ids.add(int(row["user_id"]))

    return user_ids

def get_user_names():
    user_names = set()
    # чтение user_name в csv файле
    with open("DB.csv", newline="", encoding="utf-8") as csvfile:
        reader = csv.DictReader(csvfile, delimiter=",")
        for row in reader:
            user_names.add(row["user_name"])

    return user_names

def save_user(user_id, user_name):
    user_ids = get_user_ids()
    user_names = set()

    # Сохранение id и name в csv файле
    if user_id not in user_ids:
        user_ids.add(int(user_id))
        user_names.add(user_name)
        with open("DB.csv", mode="a") as csvfile2:
            file_writer = csv.writer(csvfile2, delimiter=",", lineterminator="\r")
            file_writer.writerow([int(user_id), user_name, datetime.datetime.now()])