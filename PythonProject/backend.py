from frontend import *
import pandas as pd
#import telebot
import flet as ft
df = pd.read_excel('База_данных.xlsx')
index = 1
balance=0
#df.loc[row_index, 'column_name'] =
#def add_name():
#    df_excel.loc[row_index+1, "Имя"] = get_name()
#    return row_index
#add_name()
# Очищаем ячейку в строке 3, столбце 'Цена'
def hello():
    print("Здравствуйте! Вы попали в банковскую систему имени Дмитрия Вардугина!")
    print("Выберите следующее действие: Авторизация; Вход")
    choice = input().lower()
    while True:
        if choice == "авторизация":
            autorization()
            break
        elif choice == "вход":
            enter()
            break
        else:
            print("Некорректное действие. Пожалуйста, выберите действие из описанных ранее:")
def autorization():
    name = input("Введите ваше имя: ")
    surname = input("Введите вашу фамилию: ")
    name2 = input("Введите ваше отчество: ")
    number = input("Введите ваш номер: ")
    if len(number) >12 or len(number) < 10:
        print("Вы ввели некорректный номер. пожалуйста, запишите его в такой формате: 79991234567")
        input()
        while len(number) >12 or len(number) <9:
            print("Вы ввели некорректный номер. пожалуйста, запишите его в такой формате: 79991234567")
            input()
    password = input("Введите новый пароль: ")
    name.upper()
    surname.upper()
    name2.upper()
    df.loc[index, 'Баланс'] = balance
    df.loc[index, 'Имя'] = name
    df.loc[index, 'Фамилия'] = surname
    df.loc[index, 'Отчество'] = name2
    df.loc[index, 'Номер'] = number
    df.loc[index, 'Пароль'] = password
    df.to_excel('База_данных.xlsx', index=False)
    return 0
def on_click():  # Функция, вызываемая при нажатии
    global balance
    balance += 100  # Добавляем текст на экран
    return 0
def add_balance(page: ft.Page):
    page.title = "Кликер деняк)"
    button1 = ft.ElevatedButton("+100", on_click=on_click)
    page.add(button1)
    #df.loc[index, 'Баланс'] = balance
def enter():
    print("Введите ваш пароль:")
    pas = input()
    user = df[(df["Пароль"] == pas)]
    if not user.empty:
        print(f"Пользователь найден! Добро пожаловать, {user.iloc[0]['Имя']}!")
        return user.index[0]
    else:
        print("Ошибка: неверный номер телефона или пароль!")
        return None


