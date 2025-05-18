from frontend import *
import pandas as pd
import telebot
from telebot import types

token = "7569945224:AAF9JMJcw4E2iFfwSKbyL-TB4KGhzw7Pp44"
bot = telebot.TeleBot(token)
remove_markup = types.ReplyKeyboardRemove()
df = pd.read_excel("База_данных.xlsx")
balance = 0
index = 0
low = "абвгдеёжзийклмнопрстуфхцчшщъыьэюя"
up = "АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ"




@bot.message_handler(commands=["start"])
def start(message):
    bot.send_message(message.chat.id, f"Здравствуйте, {message.chat.first_name}! Вы попали в банковскую систему имени Дмитрия Вардугина!")
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(types.KeyboardButton("Авторизация"), types.KeyboardButton("Вход"))
    bot.send_message(message.chat.id, "Выберите действие:", reply_markup=markup)
    bot.register_next_step_handler(message, main_handler)


@bot.message_handler(content_types=["text"])
def main_handler(message):
    if message.text == "Авторизация":
        bot.send_message(message.chat.id, "Введите ваше имя:", reply_markup=remove_markup)
        bot.register_next_step_handler(message, process_name)
    elif message.text == "Вход":
        bot.send_message(message.chat.id, "Введите ваш номер:", reply_markup=remove_markup)
        bot.register_next_step_handler(message, check_number)


def check_number(message):
    try:
        number = str(message.text).strip()  # Приводим к строке и убираем пробелы
        if not number.isdigit() or len(number) != 11:
            raise ValueError

        bot.send_message(message.chat.id, "Введите ваш пароль:")
        bot.register_next_step_handler(message, check_password, {'number': number})
    except:
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        markup.add(types.KeyboardButton("Авторизация"), types.KeyboardButton("Вход"))
        bot.send_message(message.chat.id, "Некорректный номер! Используйте формат 79991234567", reply_markup=markup)
        bot.send_message(message.chat.id, "Попробуйте еще раз или выберите 'Авторизация'")


def check_password(message, number_data):
    try:
        password = str(message.text).strip()
        number = str(number_data['number']).strip()

        df['Номер'] = df['Номер'].astype(str).str.strip()
        df['Пароль'] = df['Пароль'].astype(str).str.strip()

        user = df[(df["Номер"] == number) & (df["Пароль"] == password)]

        if not user.empty:
            print(f"Вошел пользователь {user.iloc[0]['Имя']}")
            bot.send_message(message.chat.id, f"Пользователь найден! Добро пожаловать, {user.iloc[0]['Имя']}!")
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            markup.add("Главное меню", "Выход")
            bot.send_message(message.chat.id, "Выберите следующее действие: ", reply_markup=markup)
            bot.register_next_step_handler(message, main_menu)
        else:
            raise ValueError
    except:
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        markup.add(types.KeyboardButton("Авторизация"), types.KeyboardButton("Вход"))
        bot.send_message(message.chat.id, "Ошибка: неверный номер или пароль!", reply_markup=markup)
        bot.send_message(message.chat.id, "Попробуйте еще раз или выберите 'Авторизация'")


def process_name(message):
    name_index = df[df["Имя"].isnull()].index.min()
    name = message.text
    if len(name) < 2 or len(name) > 15:
        bot.send_message(message.chat.id, "Некорректное имя! Введите снова:")
        bot.register_next_step_handler(message, process_name)
        return

    first_letter = name[0].upper()
    rest = name[1:].lower()
    final_name = first_letter + rest
    print(f"Имя нового пользователя {message.chat.id}: {final_name}")
    bot.send_message(message.chat.id, f"Принятое имя: {final_name}")
    df.loc[name_index, "Имя"] = final_name

    bot.send_message(message.chat.id, "Теперь введите вашу фамилию:")
    bot.register_next_step_handler(message, process_surname)


def process_surname(message):
    surname_index = df[df["Фамилия"].isnull()].index.min()
    surname = message.text
    first_letter = surname[0].upper()
    rest = surname[1:].lower()
    final_surname = first_letter + rest
    print(f"Фамилия нового пользователя {message.chat.id}: {final_surname}")
    bot.send_message(message.chat.id, f"Принятая фамилия: {final_surname}")
    df.loc[surname_index, "Фамилия"] = surname

    bot.send_message(message.chat.id, "Теперь введите ваше отчество:")
    bot.register_next_step_handler(message, process_name2)


def process_name2(message):
    name2_index = df[df["Отчество"].isnull()].index.min()
    name2 = message.text
    if len(name2) < 6 or len(name2) > 19:
        bot.send_message(message.chat.id, "Некорректное Отчество! Введите снова:")
        bot.register_next_step_handler(message, process_name2)
        return
    first_letter = name2[0].upper()
    rest = name2[1:].lower()
    final_name2 = first_letter + rest
    print(f"Отчество нового пользователя {message.chat.id}: {final_name2}")
    bot.send_message(message.chat.id, f"Принятое отчество: {final_name2}")
    df.loc[name2_index, "Отчество"] = name2

    bot.send_message(message.chat.id, "Теперь введите ваш номер:")
    bot.register_next_step_handler(message, process_number)


def process_number(message):
    number_index = df[df["Номер"].isnull()].index.min()
    number = message.text
    if len(number) < 11 or len(number) > 12:
        bot.send_message(message.chat.id, "Некорректный номер! Введите снова в формате 79991234567:")
        return
    print(f"Номер нового пользователя {message.chat.id}: {number}")
    bot.send_message(message.chat.id, f"Ваш номер: {number}")
    df.loc[number_index, "Номер"] = number

    bot.send_message(message.chat.id, "Теперь введите ваш новый пароль:")
    bot.register_next_step_handler(message, process_password)


def process_password(message):
    password_index = df[df["Пароль"].isnull()].index.min()
    balance_index = df[df["Баланс"].isnull()].index.min()
    password = message.text
    print(f"Пароль нового пользователя {message.chat.id}: {password}")
    df.loc[password_index, "Пароль"] = password
    df.loc[balance_index, "Баланс"] = balance
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add("Сохранить ✅", "Отмена ❎")

    bot.send_message(message.chat.id, "Нажмите кнопку для сохранения:", reply_markup=markup)
    bot.register_next_step_handler(message, save_user)


def save_user(message):
    if message.text == "Сохранить ✅":
        df.to_excel("База_данных.xlsx", index=False)
        print(f"Новый пользователь сохранен")
        bot.send_message(message.chat.id, "Данные сохранены!", reply_markup=remove_markup)

        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        markup.add("Главное меню", "Выход")

        bot.send_message(message.chat.id, "Выберите следующее действие: ", reply_markup=markup)
        bot.register_next_step_handler(message, main_menu)
    elif message.text == "Отмена ❎":
        print("Пользователь отменил создание профиля")
        bot.send_message(message.chat.id, "Создание нового пользователя отменено. Нажмите /start для повторного входа в систему")
        bot.register_next_step_handler(message, start)

def main_menu(message):
    if message.text == "Главное меню":
        bot.send_message(message.chat.id, "Вы попали в главное меню банка!", reply_markup=remove_markup)
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        markup.add("Кошелек", "Назад")
        bot.send_message(message.chat.id, "Выберите следующее действие:", reply_markup=markup)
        bot.register_next_step_handler(message, menu_functions)
    elif message.text == "Выход":
        bot.send_message(message.chat.id, "Вы вышли из профиля. Напишите /start для повторного входа", reply_markup=remove_markup)
        bot.register_next_step_handler(message, start)


def menu_functions(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add("Главное меню", "Выход")
    if message.text == "Кошелек":
        bot.send_message(message.chat.id, f"Ваш баланс: {balance}",reply_markup=markup)
        bot.register_next_step_handler(message, main_menu)
    elif message.text == "Назад":
        bot.send_message(message.chat.id, "Возвращаю вас в главное меню...", reply_markup=markup)
        bot.register_next_step_handler(message, start)




bot.infinity_polling()