from decouple import config


DEBUG = config("DEBUG", cast=bool, default=False)
BASE_URL = config("BASE_URL")
API_URL = BASE_URL + "api/"
TOKEN = config("TOKEN")
