from django.core.management.utils import get_random_secret_key


def generate_secret_key(filepath):
    secret_file = open(filepath, "w")
    secret = "SECRET_KEY = " + "\"" + get_random_secret_key() + "\"" + "\n"
    secret_file.write(secret)
    secret_file.close()
