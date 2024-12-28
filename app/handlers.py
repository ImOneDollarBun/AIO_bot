import os

from aiogram.types import Message, CallbackQuery, FSInputFile
from aiogram.filters import CommandStart, Command
from aiogram import F, Router, Bot
from aiogram.fsm.context import FSMContext
from aiogram.enums import ParseMode

from aiogram.types import ReplyKeyboardRemove

import app.keyboards as kb
from app.statesgr import Registration, Uploaditems, Categories, SystemConfig, DeleteItems, Cart

from sqbases.database_sq import Database, DataBaseItems, SYS, CatalogName, CartUsage

db = Database('sqbases/database.db')
dbT = DataBaseItems('sqbases/database.db')
dbSYS = SYS('sqbases/database.db')
dbCatalogName = CatalogName("sqbases/database.db")
dbCart = CartUsage("sqbases/database.db")

router = Router()
quality = dbSYS.get_quality()
column_kb = 3


@router.message(CommandStart())
async def cmd_start(message: Message):
    if message.from_user.id == int(os.getenv('admin_id')):
        await message.answer("Админ на месте"
                             "\n/register"
                             "\n/start", reply_markup=kb.admin_kb)
    else:
        await message.answer("<b>Здравствуйте</b>\n\n"
                             "Вы можете начать с просмотра каталога товаров\n\nили /register",
                             reply_markup=kb.main, parse_mode=ParseMode.HTML)


# Registration user into BaseData
@router.message(Command("register"))
async def registration(message: Message, state: FSMContext):
    await message.answer("Введите имя", reply_markup=kb.cancel_any)
    await state.set_state(Registration.name)

    # user exists then add to db
    if not db.user_if(message.from_user.id):
        db.user_detect(message.from_user.id)


@router.message(Registration.name)
async def registration_name(message: Message, state: FSMContext):
    await state.update_data(name=message.text)
    await state.set_state(Registration.age)
    await message.answer("Введите возраст")


@router.message(Registration.age)
async def registration_num(message: Message, state: FSMContext):
    await state.update_data(age=message.text)
    await state.set_state(Registration.phone_num)
    await message.answer("Введите номер телефона")


@router.message(Registration.phone_num)
async def registration_phonenum(message: Message, state: FSMContext):
    await state.update_data(phone_num=message.text)
    data = await state.get_data()

    # add user to Database
    db.user_add(message.from_user.id, data['name'], data['phone_num'], data['age'])

    await message.answer(
        f"Итого"
        f"\n"
        f"\n"
        f"Ваше имя при регистрации: <b>{data['name']}</b>"
        f"\nВозраст: <b>{data['age']}</b>"
        f"\nНомер телефона: <b>{data['phone_num']}</b>", parse_mode=ParseMode.HTML, reply_markup=kb.cancel)
    await state.clear()


@router.callback_query(F.data == "Cancel")
async def cancel(callback: CallbackQuery, state: FSMContext):
    await callback.answer('')
    await state.set_state(Registration.name)
    await callback.message.answer("Введите имя", reply_markup=kb.cancel_any)


# Buttons
@router.message(F.text == "На главную")
async def at_home(message: Message, state: FSMContext):
    await state.clear()
    if message.from_user.id == int(os.getenv('admin_id')):
        await message.answer('Главная: ', reply_markup=kb.admin_kb)
    else:
        await message.answer('Главная: ', reply_markup=kb.main)
    await message.delete()


@router.callback_query(F.data == "stop_any")
async def registration_cancel(callback: CallbackQuery, state: FSMContext):
    await callback.answer('')
    await state.clear()
    if callback.from_user.id == int(os.getenv('admin_id')):
        await callback.message.answer('Главная: ', reply_markup=kb.admin_kb)
    else:
        await callback.message.answer('Главная: ', reply_markup=kb.main)
    await callback.message.delete()


@router.message(F.text == "Панелька админа")
async def admin_panel(message: Message):
    if message.from_user.id == int(os.getenv('admin_id')):
        await message.answer("Без проблем", reply_markup=kb.administrator)


@router.message(F.text == "Каталог")
async def catalog(message: Message):
    await message.answer("Выберите категорию товаров",
                         reply_markup=kb.base_catalog())


@router.message(F.text == "Мой Профиль")
async def catalog(message: Message):
    user_id = message.from_user.id
    await message.answer(f"Ваше имя: <b>{db.get_name(user_id)}</b>"
                         f"\nВозраст: <b>{db.get_age(user_id)}</b>"
                         f"\nНомер телефона: <b>{db.get_phone(user_id)}</b>", reply_markup=kb.cancel)


@router.message(F.text == "Контакты")
async def contacts(message: Message):
    await message.answer("<b>Контакты</b>\n\n@userpaym - <b>Легенда сего бота и мой отец</b>\n\nА больше никого нет :(")


# upload items
@router.message(F.text == "Закинуть товаров")
async def upload_name(message: Message, state: FSMContext):
    if message.from_user.id == int(os.getenv('admin_id')):
        await state.set_state(Uploaditems.name)
        await message.answer("Процесс добавление товара", reply_markup=ReplyKeyboardRemove())
        await message.answer("Отправьте название товара", reply_markup=kb.cancel_any)


@router.message(Uploaditems.name)
async def upload_description(message: Message, state: FSMContext):
    await state.update_data(name=message.text)
    await message.answer("Отправьте описание товара")
    await state.set_state(Uploaditems.description)


@router.message(Uploaditems.description)
async def upload_price(message: Message, state: FSMContext):
    await state.update_data(description=message.text)
    await message.answer("Отправьте цену товара")
    await state.set_state(Uploaditems.price)


@router.message(Uploaditems.price)
async def upload_photo(message: Message, state: FSMContext):
    await state.update_data(price=message.text)
    await message.answer("Выберите категорию товара",
                         reply_markup=kb.kb_builder_upload(dbCatalogName.get_names(), column_kb))
    await state.set_state(Uploaditems.catalog)


@router.message(Uploaditems.catalog)
async def choose_catalog(message: Message, state: FSMContext):
    await state.update_data(catalog=message.text)
    await message.answer(".", reply_markup=ReplyKeyboardRemove())
    await message.answer("Отправьте фото товара")
    await state.set_state(Uploaditems.photo)


@router.message(Uploaditems.photo)
async def upload_db(message: Message, state: FSMContext, bot: Bot):
    # quality = dbSYS.get_quality()
    await state.update_data(photo_id=message.photo[quality].file_id)
    await state.update_data(
        photo_path=rf"C:\Users\Andrew\PycharmProjects\AIO_bot\photos\{message.photo[quality].file_id}.jpg")
    await bot.download(message.photo[quality],
                       rf"C:\Users\Andrew\PycharmProjects\AIO_bot\photos\{message.photo[quality].file_id}.jpg")
    data = await state.get_data()

    # add item to dbT
    dbT.set_item(data['photo_id'],
                 data['name'],
                 data['description'],
                 data['price'],
                 message.from_user.id,
                 data['catalog'],
                 data['photo_path'])

    # add categories to dbCatalogName
    if not dbCatalogName.name_exists(data['catalog']):
        dbCatalogName.set_names(data['catalog'])

    # show it to me
    await message.answer_photo(FSInputFile(rf"C:\Users\Andrew\PycharmProjects\AIO_bot\photos\{data['photo_id']}.jpg"),
                               f"<b>Наименование товара:</b> {data['name']}"
                               f"\n\n<b>Описание товара:</b> {data['description']}"
                               f"\n<b>Цена:</b> {data['price']}"
                               f"\n\nitem_id: <code>{dbT.get_item_id(data['photo_id'])}</code>"
                               f"\nКатегория: <code>{data['catalog']}</code>",
                               reply_markup=kb.change_sth, parse_mode=ParseMode.HTML
                               )
    if message.from_user.id == int(os.getenv('admin_id')):
        await message.answer('Товар добавлен', reply_markup=kb.admin_kb)

    await state.clear()


# change sth
@router.callback_query(F.data == "delete_item")
async def delete_item(callback: CallbackQuery, state: FSMContext):
    await callback.answer("")
    await callback.message.answer("Отправьте ID товара, который хотите удалить")
    await state.set_state(DeleteItems.name_del)


@router.message(DeleteItems.name_del)
async def delete(message: Message, state: FSMContext):
    await state.update_data(item_id=int(message.text))
    data = await state.get_data()
    dbT.delete_item(data['item_id'])
    await state.clear()
    await message.answer("Товар удален")


@router.callback_query(F.data == "add_item")
async def change_price(callback: CallbackQuery, state: FSMContext):
    await callback.answer('')
    await state.set_state(Uploaditems.name)
    await callback.message.answer("Процесс добавление товара", reply_markup=ReplyKeyboardRemove())
    await callback.message.answer("Отправьте название товара", reply_markup=kb.cancel_any)


# show items
@router.message(F.text == "Список товаров")
async def items(message: Message, state: FSMContext):
    if message.from_user.id == int(os.getenv('admin_id')):
        for i in dbT.get_items_id():
            await message.answer_photo(FSInputFile(dbT.get_photo_path(i)),
                                       f"<b>Наименование товара:</b> {dbT.get_item(i)[1]}"
                                       f"\n\n<b>Описание товара:</b> {dbT.get_item(i)[2]}"
                                       f"\n<b>Цена:</b> {dbT.get_item(i)[3]} рублей"
                                       f"\n\nID: <code>{dbT.get_item(i)[4]}</code>"
                                       f"\nPHOTO_ID: <code>{dbT.get_item(i)[0]}</code>",
                                       parse_mode=ParseMode.HTML, reply_markup=kb.delete_item)
    else:
        for id_item in dbT.get_items_id():
            await message.answer_photo(FSInputFile(dbT.get_photo_path(id_item)),
                                       f"<b>Наименование товара:</b> {dbT.get_item(id_item)[1]}"
                                       f"\n\n<b>Описание товара:</b> {dbT.get_item(id_item)[2]}"
                                       f"\n<b>Цена:</b> {dbT.get_item(id_item)[3]} рублей",
                                       parse_mode=ParseMode.HTML,
                                       reply_markup=kb.cart_kb_builder(text_btn="В корзину",
                                                                       callback=id_item))
    await state.set_state(Cart.add_cart_item)


# scanning for choose
@router.message(Cart.add_cart_item)
@router.callback_query()
async def answer(callback: CallbackQuery, state: FSMContext):
    await callback.answer('')

    if not callback.data in dbCart.get_items(callback.from_user.id)[0]:
        # Получаем текущее значение из состояния

        current_count = await state.get_data()
        current_count = current_count.get("count", 0)  # Если 'count' отсутствует, устанавливаем 0

        # Добавляем новое значение к текущему
        new_count = str(current_count) + callback.data

        # Обновляем состояние
        await state.update_data(count=new_count)

        # Обновляем данные в базе данных
        dbCart.update_items(new_count, callback.from_user.id)

    else:
        await callback.message.answer("Товар уже находится в вашей корзине!")


# trash
@router.message(F.text == "Корзина")
async def cart(message: Message, state: FSMContext):

    # удаляем нолик перед числом с id товаров
    if dbCart.get_items(message.from_user.id)[0][0] == "0":
        current = dbCart.get_items(message.from_user.id)[0][1:]
        dbCart.update_items(current, message.from_user.id)

    def iterate(value: str):
        finish = []
        # finish = [26, 27, 28, 29]
        for el in dbT.get_items_id():
            if str(el) in value:

                if value.find(str(el)) == 0:
                    tmp_value = value[:len(str(el))]
                    finish.append(tmp_value)
                else:
                    tmp_value = value[value.find(str(el)):value.find(str(el))+len(str(el))]
                    finish.append(tmp_value)
                print(value.find(str(el)))
        print(finish)
        return finish

    if not len(dbCart.get_items(message.from_user.id)[0]) == 0:
        for i in iterate(dbCart.get_items(message.from_user.id)[0]):
            await message.answer_photo(FSInputFile(dbT.get_photo_path(i)),
                                       f"<b>Наименование товара:</b> {dbT.get_item(i)[1]}"
                                       f"\n\n<b>Описание товара:</b> {dbT.get_item(i)[2]}"
                                       f"\n<b>Цена:</b> {dbT.get_item(i)[3]} рублей",
                                       parse_mode=ParseMode.HTML) # надо кнопку покупки делать

    else:
        await message.answer("Корзина пуста")


# system configuration
@router.message(F.text == "Изменить качество картинок")
async def change_quality(message: Message, state: FSMContext):
    if message.from_user.id == int(os.getenv('admin_id')):
        await message.answer("Отправьте значение от 0 до 3."
                             "\nЧем ближе к 0 тем хуже качество."
                             "\nИзменения буду применены только к новым изображениям"
                             f"\n\nСейчас значение: <b>{dbSYS.get_quality()}</b>")
        await state.set_state(SystemConfig.change_quality)


@router.message(SystemConfig.change_quality)
async def change_quality(message: Message, state: FSMContext):
    await state.update_data(count=int(message.text))
    data = await state.get_data()
    dbSYS.change_quality(data['count'])
    await state.clear()
    await message.answer("Качество фото обновлено")


@router.message(F.text == "Каталоги")
async def catalogs(message: Message):
    if message.from_user.id == int(os.getenv('admin_id')):
        await message.answer("Чего хочешь?", reply_markup=kb.catalogs_settings)


@router.message(F.text == "Добавить категорию")
async def add_cat(message: Message, state: FSMContext):
    if message.from_user.id == int(os.getenv('admin_id')):
        await message.answer("Отправьте название категории в чат")
        await state.set_state(Categories.name_add)


@router.message(Categories.name_add)
async def catch_name(message: Message, state: FSMContext):
    await state.update_data(name=message.text)
    data = await state.get_data()
    dbCatalogName.set_names(data['name'])
    await message.answer("Добавил категорию")
    await state.clear()


@router.message(F.text == "Удалить категорию")
async def add_cat(message: Message, state: FSMContext):
    if message.from_user.id == int(os.getenv('admin_id')):
        await message.answer("Отправьте название категории в чат")
        await state.set_state(Categories.name_del)


@router.message(Categories.name_del)
async def catch_name(message: Message, state: FSMContext):
    await state.update_data(name=message.text)
    data = await state.get_data()
    dbCatalogName.delete_names(dbCatalogName.get_id_by_name(data['name'])[0])
    await message.answer("Удалил категорию")
    await state.clear()


@router.message(F.text == "Список категорий")
async def list_cat(message: Message):
    if message.from_user.id == int(os.getenv('admin_id')):
        for i in dbCatalogName.get_names():
            await message.answer(f"<code>{i}</code>", parse_mode=ParseMode.HTML)
        if len(dbCatalogName.get_names()) == 0:
            await message.answer("Их нет")
