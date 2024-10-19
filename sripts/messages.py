import configparser

config = configparser.ConfigParser()


def get_message(message) -> str:
    config.read("Configs/Messages.ini", encoding="utf-8")
    return config["Messages"][message].replace('\\n',"\n")

def get_log(log, user_id) -> str:
    config.read("Configs/Messages.ini", encoding="utf-8")
    return config["Logs"][log].replace('@', f"@{user_id}")
