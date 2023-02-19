from aiogram.types import ParseMode, InputFile
from aiogram import Bot, types, executor, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.utils.markdown import *
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
import keyboards
import configparser
from WorkingWithDB import DB
from states import FSMUser, FSMAdmin
import GoogleSheets

config = configparser.ConfigParser()
config.read("config.ini")
BOT_TOKEN = config['Telegram']['bot_token']

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot, storage=MemoryStorage())


@dp.message_handler(commands=['start'], state='*')
async def start(message: types.Message):
    DB.delete_creating_info(external_id=message.from_user.id)
    text = """
Мы – Правовой Центр ABC. Наша работа направлена на защиту прав граждан и их законное освобождение от задолженностей через процедуру банкротства.
Списываем долги
✔️ Бесплатно консультируем по банкротству, разбираем ваш конкретный случай 
✔️ Гарантируем максимальный результат при вашем минимальном участии – мы всё делаем сами
✔️ Работаем быстро и качественно по всей России
✔️ Эксперты со стажем более 5 лет

Наш канал: @bankrotstvo77
Написать в Telegram: @denbro888
Наш сайт: https://abc-groupe.ru
Позвонить: +7(988) 503 71 66
    """
    DB.add_new_user(external_id=message.from_user.id,
                    username=message.from_user.username,
                    firstname=message.from_user.first_name,
                    lastname=message.from_user.last_name)
    await bot.send_photo(message.from_user.id,
                         photo=InputFile('images/main.jpg'),
                         caption=text,
                         reply_markup=keyboards.main_kb)

    if DB.has_heal_name(message.from_user.id):
        await bot.send_message(message.from_user.id,
                               text='Для продолжения, напишите свое имя',
                               reply_markup=keyboards.ReplyKeyboardRemove())
        await FSMUser.typing_real_name.set()


@dp.message_handler(state=FSMUser.typing_real_name)
async def typing_real_name(message: types.Message):
    real_name = message.text
    DB.add_real_name(external_id=message.from_user.id, real_name=real_name)
    await bot.send_message(
        message.from_user.id,
        text='Спасибо\nНажмите /help чтобы посмотреть информацию',
        reply_markup=keyboards.ReplyKeyboardRemove())
    await FSMUser.beginning.set()


@dp.message_handler(commands=['help'], state='*')
async def help(message: types.Message):
    DB.delete_creating_info(external_id=message.from_user.id)
    text = """Приветствую! Я официальный бот Центра Правовой Помощи Должникам 💸

Вот что я могу для вас сделать:

💲Создать заявку на консультацию
ℹ️ Рассказать о нас поподробнее
⚡Задать вопрос online⚡"""
    await bot.send_message(message.from_user.id,
                           text=text,
                           reply_markup=keyboards.help_kb)
    await FSMUser.choose_action.set()


@dp.message_handler(lambda c: c.text == '⚡Задать вопрос online⚡',
                    state=FSMUser.choose_action)
async def ask_online(message: types.Message):
    await bot.send_message(message.from_user.id,
                           text='Введите текст сообщения',
                           reply_markup=keyboards.ReplyKeyboardRemove())
    await FSMUser.asking_online.set()


@dp.message_handler(state=FSMUser.asking_online)
async def typing_message_online(message: types.Message):
    msg = str(message.text)
    admins = DB.get_all_admins()
    contacts = InlineKeyboardMarkup()
    b = InlineKeyboardButton(text='Показать контакты',
                             callback_data=f'get_info_{message.from_user.id}')
    contacts.add(b)
    for admin in admins:
        await bot.send_message(
            admin,
            text=text(
                msg,
                '\n',
                f'от пользователя @{message.from_user.username}',
            ),
            reply_markup=contacts)


@dp.callback_query_handler(lambda c: 'get_info_' in c.data, state='*')
async def get_info(call: types.CallbackQuery):
    external_id = ''.join(filter(str.isdigit, call.data))
    data = DB.get_contacts_by_id(external_id=external_id)
    await bot.send_message(call.message.chat.id, text=data)


@dp.message_handler(lambda c: c.text == 'ℹ️Рассказать о нас подробнее',
                    state=FSMUser.choose_action)
async def more_info(message: types.Message):
    DB.delete_creating_info(external_id=message.from_user.id)
    text = '''Мы – Правовой Центр ABC. Наша работа направлена на защиту прав граждан и их законное освобождение от задолженностей через процедуру банкротства.

Списываем долги
✔️ Бесплатно консультируем по банкротству, разбираем ваш конкретный случай 
✔️ Гарантируем максимальный результат при вашем минимальном участии – мы всё делаем сами
✔️ Работаем быстро и качественно по всей России
✔️ Эксперты со стажем более 5 лет

Наш канал: @bankrotstvo77
Написать в Telegram: @denbro888
Наш сайт: https://abc-groupe.ru
Позвонить: +7 (988) 503 71 66'''
    await bot.send_message(message.from_user.id,
                           text=text,
                           reply_markup=keyboards.main_kb)


@dp.message_handler(lambda c: '💲Создать заявку на консультацию' in c.text,
                    state=FSMUser.choose_action)
async def get_price(message: types.Message):
    DB.delete_creating_info(external_id=message.from_user.id)
    DB.create_info(message.from_user.id)
    await bot.send_message(message.from_user.id,
                           text='Какая у вас сумма долга?',
                           reply_markup=keyboards.debt_kb)
    await FSMUser.choose_debt.set()


@dp.message_handler(lambda c: c.text in keyboards.prices,
                    state=FSMUser.choose_debt)
async def has_debt(message: types.Message):
    credit = message.text
    DB.add_credit(credit=credit, external_id=message.from_user.id)
    await bot.send_message(message.from_user.id,
                           text='Есть ли просрочки?',
                           reply_markup=keyboards.yes_no_kb)
    await FSMUser.choose_expiary.set()


@dp.message_handler(lambda c: c.text in keyboards.yes_no,
                    state=FSMUser.choose_expiary)
async def has_debt(message: types.Message):
    context = message.text
    DB.add_expiary_payment(context=context, external_id=message.from_user.id)
    await bot.send_message(message.from_user.id,
                           text='Есть ли у вас недвижимость?',
                           reply_markup=keyboards.yes_no_kb)
    await FSMUser.choose_estate.set()


@dp.message_handler(lambda c: c.text in keyboards.yes_no,
                    state=FSMUser.choose_estate)
async def has_estate(message: types.Message):
    context = message.text
    DB.add_estate(context=context, external_id=message.from_user.id)
    await bot.send_message(message.from_user.id,
                           text='Есть ли у вас автомобиль?',
                           reply_markup=keyboards.yes_no_kb)
    await FSMUser.choose_car.set()


@dp.message_handler(lambda c: c.text in keyboards.yes_no,
                    state=FSMUser.choose_car)
async def has_car(message: types.Message):
    context = message.text
    DB.add_car(context=context, external_id=message.from_user.id)
    await bot.send_message(message.from_user.id,
                           text='Какой у вас доход?',
                           reply_markup=keyboards.salary_kb)
    await FSMUser.choose_salary.set()


@dp.message_handler(lambda c: c.text in keyboards.salary,
                    state=FSMUser.choose_salary)
async def check_salary(message: types.Message):
    context = message.text
    DB.add_salary(context=context, external_id=message.from_user.id)
    await bot.send_message(message.from_user.id,
                           text='Укажите ваше семейное положение',
                           reply_markup=keyboards.marital_status_kb)
    await FSMUser.choose_marital_status.set()


@dp.message_handler(lambda c: c.text in keyboards.marital,
                    state=FSMUser.choose_marital_status)
async def check_marital_status(message: types.Message):
    context = message.text
    order_id = DB.get_last_index(message.from_user.id)
    DB.add_marital_status(context=context, external_id=message.from_user.id)
    flag = DB.has_phone(message.from_user.id)
    if flag:
        await bot.send_message(message.from_user.id,
                               text='Укажите номер телефона',
                               reply_markup=keyboards.ReplyKeyboardRemove())
        await FSMUser.type_phone.set()
    else:
        DB.finish_info(external_id=message.from_user.id)
        await bot.send_message(
            message.from_user.id,
            text=text(
                'Спасибо за уделенное время! Наш специалист свяжется с вами в ближайшее время.'
            ),
            reply_markup=keyboards.help_kb)
        GoogleSheets.update()
        await FSMUser.beginning.set()
        admins = DB.get_all_admins()
        m = DB.get_info_by_id(order_id)
        for admin in admins:
            await bot.send_message(
                admin,
                text=text(f'Новый пользователь создал заказ\n{m}', ),
                reply_markup=keyboards.ReplyKeyboardRemove())


@dp.message_handler(state=FSMUser.type_phone)
async def type_phone(message: types.Message):
    phone = message.text
    order_id = DB.get_last_index(message.from_user.id)
    if (str(phone)).isalpha():
        await bot.send_message(message.from_user.id,
                               text='Неверный номер. Повторите попытку',
                               reply_markup=keyboards.ReplyKeyboardRemove())
        await FSMUser.type_phone.set()
        return

    DB.add_phone(phone, message.from_user.id)
    DB.finish_info(external_id=message.from_user.id)
    await bot.send_message(
        message.from_user.id,
        text=text(
            'Спасибо за уделенное время! Наш специалист свяжется с вами в ближайшее время.'
        ),
        reply_markup=keyboards.help_kb)
    GoogleSheets.update()
    await FSMUser.beginning.set()
    admins = DB.get_all_admins()
    m = DB.get_info_by_id(order_id)
    for admin in admins:
        await bot.send_message(admin,
                               text=text(
                                   f'Новый пользователь создал заказ\n{m}', ),
                               reply_markup=keyboards.ReplyKeyboardRemove())


@dp.message_handler(commands=['run_admin_menu'], state='*')
async def run_admin_menu(message: types.Message):
    if DB.check_admin(message.from_user.id):
        await bot.send_message(message.from_user.id,
                               text='Выберите действие\n',
                               reply_markup=keyboards.admin_panel_kb)
        await FSMAdmin.choosing_actions.set()


@dp.message_handler(lambda c: c.text == 'Посмотреть список заказов',
                    state=FSMAdmin.choosing_actions)
async def get_all_orders(message: types.Message):
    data = DB.get_all_infos()
    await bot.send_message(message.from_user.id,
                           text=data,
                           reply_markup=keyboards.ReplyKeyboardRemove())


@dp.callback_query_handler(lambda c: c.data == 'main', state='*')
async def main(call: types.CallbackQuery):
    DB.delete_creating_info(external_id=call.from_user.id)
    text = """Приветствую! Я официальный бот Центра Правовой Помощи Должникам 💸

Вот что я могу для вас сделать:

💲Создать заявку на консультацию
ℹ️ Рассказать о нас поподробнее
⚡Задать вопрос online⚡
"""
    await bot.send_message(call.from_user.id,
                           text=text,
                           reply_markup=keyboards.help_kb)
    await FSMUser.choose_action.set()


if __name__ == '__main__':
    print('started')
    DB.delete_creating_info
    executor.start_polling(dp, skip_updates=False)
