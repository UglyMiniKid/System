import pandas as pd
import telebot
from telebot import types

token = "7569945224:AAF9JMJcw4E2iFfwSKbyL-TB4KGhzw7Pp44"
bot = telebot.TeleBot(token)
remove_markup = types.ReplyKeyboardRemove()
df = pd.read_excel("База_данных.xlsx")
dfp = pd.read_excel("база_переводов.xlsx")
balance = 0
index = 0
low = "абвгдеёжзийклмнопрстуфхцчшщъыьэюя"
up = "АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ"
transfer_data = []
@bot.message_handler(commands=["start"])
def start(message):
    bot.send_message(message.chat.id, f"Здравствуйте, {message.chat.first_name}! Вы попали в банковскую систему "
                                      "имени Ученика Уникума!")
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(types.KeyboardButton("Авторизация"), types.KeyboardButton("Вход"))
    bot.send_message(message.chat.id, "Выберите действие:", reply_markup=markup)
    bot.register_next_step_handler(message, main_handler)
@bot.message_handler(content_types=["text"])
def main_handler(message):
    if message.text == "Авторизация":
        for i in range(df[df["Имя"].nonnull()].index.min(), df[df["Имя"].nonnull()].index.max()):
            if i == message.chat.id:
                bot.send_message(message.chat.id, "Вы уже регистрировались в нашем банке, "
                                                  "пожалуйста, войдите в Ваш аккаунт")
        bot.send_message(message.chat.id, "Введите ваше имя:", reply_markup=remove_markup)
        bot.register_next_step_handler(message, process_name)
    elif message.text == "Вход":
        bot.send_message(message.chat.id, "Введите ваш номер:", reply_markup=remove_markup)
        bot.register_next_step_handler(message, check_number)

def num_main_port(message):
    if message.text == "Авторизация":
        bot.send_message(message.chat.id, "Введите ваше имя:", reply_markup=remove_markup)
        bot.register_next_step_handler(message, process_name)
    else:
        try:
            number = str(message.text).strip()
            if not number.isdigit() or len(number) != 11:
                raise ValueError
            bot.send_message(message.chat.id, "Введите ваш номер:")
            bot.register_next_step_handler(message, check_number)
        except:
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            markup.add(types.KeyboardButton("Авторизация"), types.KeyboardButton("Вход"))
            bot.send_message(message.chat.id, "Некорректный номер! Используйте формат 79991234567", reply_markup=markup)
            bot.send_message(message.chat.id, "Попробуйте еще раз или выберите 'Авторизация'")
            bot.register_next_step_handler(message, num_main_port)

def check_number(message):
    try:
        number = str(message.text).strip()
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
        user = df[(df["Номер"] == number) & (df["Пароль"] == password) & (df["ID"] == message.chat.id)]
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
        bot.send_message(message.chat.id, "Попробуйте ввести номер снова или нажмите 'Авторизация'")
        bot.register_next_step_handler(message, num_main_port)
        return

def process_name(message):
    name_index = df[df["Имя"].isnull()].index.min()
    name = message.text
    if len(name) < 2 or len(name) > 15:
        bot.send_message(message.chat.id, "Некорректное имя! Введите снова:")
        bot.register_next_step_handler(message, process_name)
        return
    if not name.isalpha():
        bot.send_message(message.chat.id,"Имя должно содержать только буквы (без цифр, пробелов и других символов)! Введите снова:")
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
    if not surname.isalpha():
        bot.send_message(message.chat.id,"Фамилия должна содержать только буквы (без цифр, пробелов и других символов)! Введите снова:")
        bot.register_next_step_handler(message, process_surname)
        return
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
        bot.send_message(message.chat.id, "Некорректное отчество! Введите снова:")
        bot.register_next_step_handler(message, process_name2)
        return
    if not name2.isalpha():
        bot.send_message(message.chat.id,"Отчество должно содержать только буквы (без цифр, пробелов и других символов)! Введите снова:")
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
    if len(number) != 11:
        bot.send_message(message.chat.id, "Некорректный номер! Введите снова в формате 79991234567:")
        bot.register_next_step_handler(message, process_number)
        return
    print(f"Номер нового пользователя {message.chat.id}: {number}")
    bot.send_message(message.chat.id, f"Ваш номер: {number}")
    df.loc[number_index, "Номер"] = number
    bot.send_message(message.chat.id, "Теперь введите ваш новый пароль:")
    bot.register_next_step_handler(message, process_password)
def process_password(message):
    password_index = df[df["Пароль"].isnull()].index.min()
    balance_index = df[df["Баланс"].isnull()].index.min()
    ID_index = df[df["ID"].isnull()].index.min()
    password = message.text
    ID = message.chat.id
    print(f"Пароль нового пользователя {message.chat.id}: {password}")
    df.loc[password_index, "Пароль"] = password
    df.loc[balance_index, "Баланс"] = balance
    df.loc[ID_index, "ID"] = ID
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
    user_data = df[df["ID"] == message.chat.id]
    if user_data.empty:
        bot.send_message(message.chat.id, "Ошибка: ваш профиль не найден")
        return
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
    user_data = df[df["ID"] == message.chat.id]
    if user_data.empty:
        bot.send_message(message.chat.id, "Ошибка: ваш профиль не найден")
        return
    if message.text == "Кошелек":
        current_balance = user_data.iloc[0]["Баланс"]
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        markup.add("Заработок", "Перевод", "История", "Назад")
        bot.send_message(message.chat.id,f"Ваш текущий баланс: {current_balance} руб.",reply_markup=markup)
        user_name = user_data.iloc[0]["Имя"]
        print(f"Пользователь {user_name} просмотрел баланс")
        bot.register_next_step_handler(message, money_operation)
    elif message.text == "Назад":
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        markup.add("Главное меню", "Выход")
        bot.send_message(message.chat.id, "Возвращаю вас в главное меню...", reply_markup=markup)
        bot.register_next_step_handler(message, main_menu)
def money_operation(message):
    user_data = df[df["ID"] == message.chat.id]
    if user_data.empty:
        bot.send_message(message.chat.id, "Ошибка: ваш профиль не найден")
        return
    if message.text == "Заработок":
        start_balance = user_data.iloc[0]["Баланс"]
        new_balance = start_balance + 1000
        df.loc[df["ID"] == message.chat.id, "Баланс"] = new_balance
        df.to_excel("База_данных.xlsx", index=False)
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        markup.add("Заработок", "Перевод", "История", "Назад")
        bot.send_message(message.chat.id,f"+1000 руб! Новый баланс: {new_balance} руб.",reply_markup=markup)
        bot.register_next_step_handler(message, money_operation)
    elif message.text == "Перевод":
        bot.send_message(message.chat.id, "Введите имя пользователя, которому вы хотите перевести деньги")
        bot.register_next_step_handler(message, start_perevod)
    elif message.text == "Назад":
        user_name = user_data.iloc[0]["Имя"]
        final_balance = user_data.iloc[0]["Баланс"]
        print(f"Баланс пользователя {user_name}: {final_balance}")
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        markup.add("Главное меню", "Выход")
        bot.send_message(message.chat.id, "Возвращаю вас в главное меню...", reply_markup=markup)
        bot.register_next_step_handler(message, main_menu)
def start_perevod(message):
    user_data = df[df["ID"] == message.chat.id]
    if user_data.empty:
        bot.send_message(message.chat.id, "Ошибка: ваш профиль не найден")
        return
    recipient_name = message.text.strip()
    user2_data = df[df["Имя"] == recipient_name]
    if user2_data.empty:
        bot.send_message(message.chat.id, "Ошибка: профиль получателя не найден")
        return
    if user2_data.iloc[0]["ID"] == message.chat.id:
        bot.send_message(message.chat.id, "Ошибка: нельзя переводить самому себе")
        return
    global transfer_data
    transfer_data = {
        'Получатель': user2_data.iloc[0]["ID"],
        'Отправитель': message.chat.id
    }
    bot.send_message(message.chat.id, f"Введите сумму для перевода (ваш баланс {user_data.iloc[0]['Баланс']} руб.):")
    bot.register_next_step_handler(message, end_perevod)
def end_perevod(message):
    try:
        amount = float(message.text)
        if amount <= 0:
            raise ValueError("Сумма должна быть положительной")
        recipient_id = transfer_data['Получатель']
        sender_id = transfer_data['Отправитель']
        user_data = df[df["ID"] == sender_id]
        user2_data = df[df["ID"] == recipient_id]
        user_balance = user_data.iloc[0]["Баланс"]
        user2_balance = user2_data.iloc[0]["Баланс"]
        if amount > user_balance:
            bot.send_message(sender_id, "Ошибка: недостаточно средств на балансе")
            return
        user_new_balance = user_balance - amount
        user2_new_balance = user2_balance + amount
        df.loc[df["ID"] == sender_id, "Баланс"] = user_new_balance
        df.loc[df["ID"] == recipient_id, "Баланс"] = user2_new_balance
        global dfp
        new_transfer = pd.DataFrame({
            "Отправитель": [user_data.iloc[0]["Имя"]],
            "Получатель": [user2_data.iloc[0]["Имя"]],
            "Сумма": [amount]
        })
        dfp = pd.concat([dfp, new_transfer], ignore_index=True)
        dfp.to_excel("База_переводов.xlsx", index=False)
        df.to_excel("База_данных.xlsx", index=False)
        bot.send_message(sender_id, f"Перевод выполнен! Ваш баланс: {user_new_balance} руб.")
        bot.send_message(recipient_id, f"Пользователь {user_data.iloc[0]['Имя']} перевел вам {amount} руб. "
                                       f"Ваш новый баланс: {user2_new_balance} руб.")
        print(
            f"Пользователь {user_data.iloc[0]['Имя']} перевел {amount} рублей пользователю {user2_data.iloc[0]['Имя']}")
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        markup.add("Заработок", "Перевод", "История", "Назад")
        bot.send_message(sender_id, "Возвращаю в меню кошелька...", reply_markup=markup)
        bot.register_next_step_handler(message, money_operation)
    except ValueError:
        bot.send_message(message.chat.id, "Ошибка: введите корректную сумму (число)")
        bot.register_next_step_handler(message, end_perevod)
def money_operation(message):
    user_data = df[df["ID"] == message.chat.id]
    if user_data.empty:
        bot.send_message(message.chat.id, "Ошибка: ваш профиль не найден")
        return
    user_name = user_data.iloc[0]["Имя"]
    current_balance = user_data.iloc[0]["Баланс"]
    print(f"Баланс пользователя {user_name}: {current_balance}")
    if message.text == "Заработок":
        new_balance = current_balance + 1000
        df.loc[df["ID"] == message.chat.id, "Баланс"] = new_balance
        df.to_excel("База_данных.xlsx", index=False)
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        markup.add("Заработок", "Перевод", "История", "Назад")
        bot.send_message(message.chat.id, f"+1000 руб! Новый баланс: {new_balance} руб.", reply_markup=markup)
        bot.register_next_step_handler(message, money_operation)
    elif message.text == "Перевод":
        bot.send_message(message.chat.id, f"Ваш текущий баланс: {current_balance} руб.")
        bot.send_message(message.chat.id, "Введите имя пользователя, которому вы хотите перевести деньги")
        bot.register_next_step_handler(message, start_perevod)
    elif message.text == "История":
        show_history(message)
    elif message.text == "Назад":
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        markup.add("Главное меню", "Выход")
        bot.send_message(message.chat.id, "Возвращаю вас в главное меню...", reply_markup=markup)
        bot.register_next_step_handler(message, main_menu)
def show_history(message):
    user_data = df[df["ID"] == message.chat.id]
    if user_data.empty:
        bot.send_message(message.chat.id, "Ошибка: ваш профиль не найден")
        return
    user_name = user_data.iloc[0]["Имя"]
    user_history = dfp[(dfp["Отправитель"] == user_name) | (dfp["Получатель"] == user_name)]
    if user_history.empty:
        bot.send_message(message.chat.id, "У вас пока нет истории переводов")
    else:
        history_text = "Ваша история переводов: "
        for _, transfer in user_history.iterrows():
            if transfer["Отправитель"] == user_name:
                history_text += f"Отправлено {transfer['Сумма']} руб. пользователю {transfer['Получатель']}"
            else:
                history_text += f"Получено {transfer['Сумма']} руб. от пользователя {transfer['Отправитель']}"
        bot.send_message(message.chat.id, history_text)
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add("Заработок", "Перевод", "История", "Назад")
    bot.send_message(message.chat.id, "Выберите действие:", reply_markup=markup)
    bot.register_next_step_handler(message, money_operation)
bot.infinity_polling()