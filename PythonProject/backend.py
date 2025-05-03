from frontend import *
import pandas as pd
#import telebot
import flet as ft
df = pd.read_excel('База_данных.xlsx')
index = 1
balance=0
name_index = df[df["Имя"].isnull()].index.min()
surname_index = df[df["Фамилия"].isnull()].index.min()
name2_index = df[df["Отчество"].isnull()].index.min()
number_index = df[df["Номер"].isnull()].index.min()
password_index = df[df["Пароль"].isnull()].index.min()
balance_index = df[df["Баланс"].isnull()].index.min()
#df.loc[row_index, 'column_name'] =
#def add_name():
#    df_excel.loc[row_index+1, "Имя"] = get_name()
#    return row_index
#add_name()
# Очищаем ячейку в строке 3, столбце 'Цена'
low = "абвгдеёжзийклмнопрстуфхцчшщъыьэюя"
up = 'АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ'
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
            choice = input().lower()
def autorization():
    name = input("Введите ваше имя: ")
    if len(name) > 15 or len(name) < 2:
        while len(name) > 15 or len(name) < 2:
            print("Вас нету в базе данных Госуслуг. Введите ваше настоящее имя")
            name = input("Введите ваше имя: ")
    first_s = name[0]
    if first_s in low:
        pos = low.index(first_s)
        first_s = up[pos]
    offer_s = name[1:]
    low_s = ''
    for i in offer_s:
        if i in up:
            pos = up.index(i)
            i = low[pos]
        low_s += i
    name = first_s + low_s
    surname = input("Введите вашу фамилию: ")
    first_s = surname[0]
    if first_s in low:
        pos = low.index(first_s)
        first_s = up[pos]
    offer_s = surname[1:]
    low_s = ''
    for i in offer_s:
        if i in up:
            pos = up.index(i)
            i = low[pos]
        low_s += i
    surname = first_s + low_s
    name2 = input("Введите ваше отчество: ")
    if len(name2) > 19 or len(name2) < 6:
        while len(name2) > 19 or len(name2) < 6:
            print("Вас нету в базе данных Госуслуг. Введите ваше настоящее имя")
            name = input("Введите ваше имя: ")
    first_s = name2[0]
    if first_s in low:
        pos = low.index(first_s)
        first_s = up[pos]
    offer_s = name2[1:]
    low_s = ''
    for i in offer_s:
        if i in up:
            pos = up.index(i)
            i = low[pos]
        low_s += i
    name2 = first_s + low_s
    number = input("Введите ваш номер: ")
    if len(number) >12 or len(number) < 10:
        print("Вы ввели некорректный номер. пожалуйста, запишите его в такой формате: 79991234567")
        input()
        while len(number) >12 or len(number) <9:
            print("Вы ввели некорректный номер. пожалуйста, запишите его в такой формате: 79991234567")
            input()
    password = input("Введите новый пароль: ")
    df.loc[name_index, 'Имя'] = name
    df.loc[surname_index, 'Фамилия'] = surname
    df.loc[name2_index, 'Отчество'] = name2
    df.loc[number_index, 'Номер'] = number
    df.loc[password_index, 'Пароль'] = password
    df.loc[balance_index, 'Баланс'] = balance

    df.to_excel('База_данных.xlsx', index=False)
    return 0
    index += 1
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
        print("Ошибка: пароль!")#неверный номер телефона или
        return None
def menu():
    print("Вы находитесь в главном меню банка. Выберите следующее действие:")
    print()


