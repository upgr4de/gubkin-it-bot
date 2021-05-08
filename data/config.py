from environs import Env

# Теперь используем вместо библиотеки python-dotenv библиотеку environs
env = Env()
env.read_env()

BOT_TOKEN = env.str('BOT_TOKEN')  # Забираем значение типа str
ADMINS = env.list('ADMINS')  # Тут у нас будет список из админов
IP = env.str('IP')  # Тоже str, но для айпи адреса хоста
GOOGLE_FORMS_PATH = env.str('GOOGLE_FORMS_PATH')
GOOGLE_CREDENTIALS = GOOGLE_FORMS_PATH + env.str('GOOGLE_CREDENTIALS')
GOOGLE_TOKEN = GOOGLE_FORMS_PATH + env.str('GOOGLE_TOKEN')
SCRIPT_ID = env.str('SCRIPT_ID')
POLLS_PATH = env.str('POLLS_PATH')
INCORRECT_INPUT = env.str('INCORRECT_INPUT')
