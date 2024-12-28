from aiogram.fsm.state import State, StatesGroup


class Registration(StatesGroup):
    name = State()
    age = State()
    phone_num = State()


class Uploaditems(StatesGroup):
    name = State()
    description = State()
    price = State()
    photo = State()
    catalog = State()


class DeleteItems(StatesGroup):
    name_del = State()


class Categories(StatesGroup):
    name_add = State()
    name_del = State()


class SystemConfig(StatesGroup):
    change_quality = State()


class Cart(StatesGroup):
    add_cart_item = State()
    tmp_stage = State()
