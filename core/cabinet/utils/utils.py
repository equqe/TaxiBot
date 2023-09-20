import random
import string


def get_telegram_data_upload_path(instance, filename):
    return "telegram_data/{}".format(filename)


def get_random_string() -> str:
    return "".join([random.choice(string.ascii_letters) for i in range(12)])
