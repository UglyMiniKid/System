from frontend import *
import pandas as pd
import telebot
from telebot import types

token = "7569945224:AAF9JMJcw4E2iFfwSKbyL-TB4KGhzw7Pp44"
bot = telebot.TeleBot(token)
remove_markup = types.ReplyKeyboardRemove()
df = pd.read_excel("База_данных.xlsx")
balance = 0
name_index = df[df["Имя"].isnull()].index.min()
surname_index = df[df["Фамилия"].isnull()].index.min()
name2_index = df[df["Отчество"].isnull()].index.min()
number_index = df[df["Номер"].isnull()].index.min()
password_index = df[df["Пароль"].isnull()].index.min()
balance_index = df[df["Баланс"].isnull()].index.min()
low = "абвгдеёжзийклмнопрстуфхцчшщъыьэюя"
up = "АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ"


@bot.message_handler(commands=["start"])
def start(message):
    bot.send_message(message.chat.id,
                     f"Здравствуйте, {message.chat.username}! Вы попали в банковскую систему имени Дмитрия Вардугина!")

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(types.KeyboardButton("Авторизация"), types.KeyboardButton("Вход"))

    bot.send_message(message.chat.id, "Выберите действие:", reply_markup=markup)


@bot.message_handler(content_types=["text"])
def main_handler(message):
    if message.text == "Авторизация":
        bot.send_message(message.chat.id, "Введите ваше имя:")
        bot.register_next_step_handler(message, process_name)

    elif message.text == "Вход":
        bot.send_message(message.chat.id, "Введите ваш пароль:")
        bot.register_next_step_handler(message, enter)

def enter(message):
    password = message.text
    user = df[df["Пароль"] == password]

    if not user.empty:
        bot.send_message(message.chat.id, f"Пользователь найден! Добро пожаловать, {user.iloc[0]['Имя']}!")

    else:
        bot.send_message(message.chat.id, "Ошибка: неверный пароль!")
        bot.send_message(message.chat.id, "Попробуйте еще раз или выберите 'Авторизация'")


def process_name(message):
    name = message.text

    if len(name) < 2 or len(name) > 15:
        bot.send_message(message.chat.id, "Некорректное имя! Введите снова:")
        bot.register_next_step_handler(message, process_name)
        return

    first_letter = name[0].upper()
    rest = name[1:].lower()
    final_name = first_letter + rest

    bot.send_message(message.chat.id, f"Принятое имя: {final_name}")
    df.loc[name_index, "Имя"] = final_name

    bot.send_message(message.chat.id, "Теперь введите вашу фамилию:")
    bot.register_next_step_handler(message, process_surname)


def process_surname(message):
    surname = message.text

    first_letter = surname[0].upper()
    rest = surname[1:].lower()
    final_surname = first_letter + rest

    bot.send_message(message.chat.id, f"Принятая фамилия: {final_surname}")
    df.loc[surname_index, "Фамилия"] = surname

    bot.send_message(message.chat.id, "Теперь введите ваше отчество:")
    bot.register_next_step_handler(message, process_name2)


def process_name2(message):
    name2 = message.text

    first_letter = name2[0].upper()
    rest = name2[1:].lower()
    final_name2 = first_letter + rest

    bot.send_message(message.chat.id, f"Принятое отчество: {final_name2}")
    df.loc[name2_index, "Отчество"] = name2

    bot.send_message(message.chat.id, "Теперь введите ваш номер:")
    bot.register_next_step_handler(message, process_number)


def process_number(message):
    number = message.text

    first_letter = number[0].upper()
    rest = number[1:].lower()
    final_number = first_letter + rest

    bot.send_message(message.chat.id, f"Ваш номер: {final_number}")
    df.loc[surname_index, "Номер"] = number

    bot.send_message(message.chat.id, "Теперь введите ваш новый пароль:")
    bot.register_next_step_handler(message, process_password)


def process_password(message):
    password = message.text
    df.loc[password_index, "Пароль"] = password
    df.loc[balance_index, "Баланс"] = balance

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(types.KeyboardButton("Сохранить"))

    bot.send_message(message.chat.id, "Нажмите кнопку для сохранения:", reply_markup=markup)
    bot.register_next_step_handler(message, save_user)


def save_user(message):
    df.to_excel("База_данных.xlsx", index=False)
    bot.send_message(message.chat.id, "Данные сохранены!", reply_markup=remove_markup)

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add("Главное меню", "Выход")

    bot.send_message(message.chat.id, "Выберите следующее действие: ", reply_markup=markup)
    bot.register_next_step_handler(message, main_menu)


def main_menu(message):
    if message.text == "Выход":
        print("Da")


bot.infinity_polling()