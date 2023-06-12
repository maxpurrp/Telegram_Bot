from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, KeyboardButton, ReplyKeyboardMarkup




OptionsButton = InlineKeyboardMarkup()

ChoiseOnCreating_in = InlineKeyboardMarkup()

KeybordButtons = ReplyKeyboardMarkup(resize_keyboard = True)

MenuButton = ReplyKeyboardMarkup(resize_keyboard = True)

DeleteButtons = ReplyKeyboardMarkup(resize_keyboard = True)

ChoiseOnCreating_kb = ReplyKeyboardMarkup(resize_keyboard = True)

ChoiseOnAdding = ReplyKeyboardMarkup(resize_keyboard = True)


create_but = InlineKeyboardButton(text='Создать коллекцию', callback_data='create')
add_img = InlineKeyboardButton(text='Добавить фото в коллекцию', callback_data='add')
show_img = InlineKeyboardButton(text='Посмотреть фото из коллекции', callback_data='show_img')
show_coll = InlineKeyboardButton(text='Посмотреть существующие коллкции', callback_data='show_coll')

create_new = InlineKeyboardButton(text = 'Создать новую', callback_data = 'create')
back_menu = InlineKeyboardButton(text = 'Список команд', callback_data = 'menu')

delete = InlineKeyboardButton(text='Удалить коллекции', callback_data='delete')
menu = KeyboardButton(text='Главное меню')
list_command = KeyboardButton(text='Список команд')


one_collection = KeyboardButton(text='Все коллекции')
one_img = KeyboardButton(text='Одну коллекцию')
back = KeyboardButton(text = 'Отмена')

create_new_coll = KeyboardButton('Создать новую')


ButtonAdd = KeyboardButton(text = 'Добавить')
ButtonNo = KeyboardButton(text = 'Не добавлять')



OptionsButton.add(create_but)
OptionsButton.add(add_img)
OptionsButton.add(show_img)
OptionsButton.add(show_coll)
OptionsButton.add(delete)

ChoiseOnCreating_in.add(create_new)
ChoiseOnCreating_in.add(back_menu)

KeybordButtons.add(menu)

MenuButton.add(list_command)

DeleteButtons.add(one_collection, one_img, back)

ChoiseOnCreating_kb.add(create_new_coll, menu)

ChoiseOnAdding.add(ButtonAdd, ButtonNo, back)

