from frontend import *
import pandas as pd
import telebot
import flet as ft
df = pd.read_excel('База_данных.xlsx')
index = 1

#df.loc[row_index, 'column_name'] =
#def add_name():
#    df_excel.loc[row_index+1, "Имя"] = get_name()
#    return row_index
#add_name()
# Очищаем ячейку в строке 3, столбце 'Цена'
def hello():
    print("Здравствуйте! Вы попали в банковскую систему имени Дмитрия Вардугина!")
def get_name():
    name = input("Введите ваше имя: ")
    df.loc[index, 'Имя'] = name
    return 0
def get_surname():
    surname = input("Введите вашу фамилию: ")
    df.loc[index, 'Фамилия'] = surname
    return 0
def name2():
    name2 = input("Введите ваше отчество: ")
    df.loc[index, 'Отчество'] = name2
    return 0
def get_number():
    number = input("Введите ваш номер: ")
    df.loc[index, 'Номер'] = number
    if len(number) >12 or len(number) < 10:
        print("Вы ввели некорректный номер. пожалуйста, запишите его в такой формате: 79991234567")
        input()
        while len(number) >12 or len(number) <10:
            print("Вы ввели некорректный номер. пожалуйста, запишите его в такой формате: 79991234567")
            input()
    return 0
def get_password():
    password = input("Введите новый пароль: ")
    df.loc[index, 'Пароль'] = password
    return 0
def save_user():
    df.info()
    df.to_excel('База_данных.xlsx', index=False)
def start_balance():
    balance=0
    df.loc[index, 'Баланс'] = balance
    return 0
