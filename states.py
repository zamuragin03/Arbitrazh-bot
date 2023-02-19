from re import S
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext

class FSMUser(StatesGroup):
    beginning = State()
    choose_action = State()
    choose_debt = State()
    choose_expiary = State()
    choose_estate = State()
    choose_car = State()
    choose_salary = State()
    choose_marital_status = State()
    type_phone = State()
    typing_real_name = State()
    asking_online = State()

class FSMAdmin(StatesGroup):
    choosing_actions = State()