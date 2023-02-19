from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove

main_kb = InlineKeyboardMarkup()
b = InlineKeyboardButton(
    text='Нужна консультация',
    url=
    'https://t.me/denbro888'
)
b_1 = InlineKeyboardButton(text='Главное меню', callback_data='main')
assess = InlineKeyboardButton(
    text='Наш телеграм канал',
    url=
    'https://t.me/bankrotstvo77'
)
main_kb.add(b).add(b_1).add(assess)

help_kb = ReplyKeyboardMarkup(one_time_keyboard=False, resize_keyboard=True)
options = [
    '💲Создать заявку на консультацию',
    'ℹ️Рассказать о нас подробнее','⚡Задать вопрос online⚡'
]
for option in options:
    btn = KeyboardButton(text=option)
    help_kb.add(btn)

debt_kb = ReplyKeyboardMarkup(one_time_keyboard=False, resize_keyboard=True)
prices = [
    'До 300.000 руб', '300.000 руб – 1.000.000 руб',
    '1.000.000 руб – 3.000.000 руб', 'Свыше 3.000.000 руб'
]
for option in prices:
    btn = KeyboardButton(text=option)
    debt_kb.add(btn)

yes_no_kb = ReplyKeyboardMarkup(one_time_keyboard=False, resize_keyboard=True)
yes_no = ['Да', 'Нет']
for word in yes_no:
    btn = KeyboardButton(text=word)
    yes_no_kb.add(btn)

salary_kb = ReplyKeyboardMarkup(one_time_keyboard=False, resize_keyboard=True)
salary = ['Официальаный', 'Неофициальный', 'Доходов нет']
for pos in salary:
    btn = KeyboardButton(text=pos)
    salary_kb.add(btn)

marital_status_kb = ReplyKeyboardMarkup(one_time_keyboard=False,
                                        resize_keyboard=True)
marital = ['В браке', 'Не в браке']
for pos in marital:
    btn = KeyboardButton(text=pos)
    marital_status_kb.add(btn)

admin_panel_kb = ReplyKeyboardMarkup(one_time_keyboard=False,
                                     resize_keyboard=True)
admin = [
    'Посмотреть список заказов',
]
for pos in admin:
    btn = KeyboardButton(text=pos)
    admin_panel_kb.add(btn)
