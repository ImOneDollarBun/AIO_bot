from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup

from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder

from sqbases.database_sq import CatalogName

dbCatalogName = CatalogName("sqbases/database.db")


def base_catalog():
    return (ReplyKeyboardBuilder().
            add(KeyboardButton(text="Список товаров")).
            add(KeyboardButton(text="На главную"))).as_markup(resize_keyboard=True)


def kb_builder_upload(buttons, column):
    builder = ReplyKeyboardBuilder()

    for btn in buttons:
        builder.add(KeyboardButton(text=btn))
    builder.adjust(column)
    return builder.as_markup(resize_keyboard=True)


def cart_kb_builder(callback, text_btn):
    builder = InlineKeyboardBuilder()
    builder.button(text=f"{text_btn}", callback_data=f"{callback}")
    return builder.as_markup()


def cart_kb(txt, callback):
    return InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text=txt, callback_data=f"{callback}")]])


main = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text="Каталог")],
                                     [KeyboardButton(text="Корзина")],
                                     [KeyboardButton(text="Контакты"), KeyboardButton(text="Мой Профиль")]],
                           resize_keyboard=True,
                           input_field_placeholder='Выберите пункт меню...')

admin_kb = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text="Каталог"), KeyboardButton(text="Панелька админа")],
                                         [KeyboardButton(text="Корзина"), KeyboardButton(text="Закинуть товаров")],
                                         [KeyboardButton(text="Контакты"), KeyboardButton(text="Мой Профиль")]],
                               resize_keyboard=True)

administrator = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text="Изменить качество картинок"), KeyboardButton(text="Каталоги")],
    [KeyboardButton(text="На главную")]], resize_keyboard=True)

catalog = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="Арты бывшего фурри",
                                                                      callback_data="furry")],
                                                [InlineKeyboardButton(text="Толстовки дотера",
                                                                      callback_data="dota")],
                                                ])

get_number = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text="Отправить номер", request_contact=True)]],
                                 resize_keyboard=True)

cancel = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="Изменить", callback_data="Cancel")]])

cancel_any = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="Отменить", callback_data="stop_any")]])

change_sth = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="Добавить еще", callback_data='add_item')]])

cancel_registr = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text="Отменить регистрацию")]])

at_home = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text="На главную")]])

catalogs_settings = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text="Добавить категорию"),
                                                   KeyboardButton(text="Удалить категорию"),
                                                   KeyboardButton(text="Список категорий")],
                                                  [KeyboardButton(text="На главную")]], resize_keyboard=True)

delete_item = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="Удалить",
                                                                          callback_data="delete_item")]])
