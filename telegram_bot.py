from aiogram import Bot, Dispatcher, types, executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.dispatcher.filters import Text
import time
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

from config import TOKEN, MSG
from database import Database
from Buttons import OptionsButton, KeybordButtons, MenuButton, DeleteButtons, ChoiseOnAdding, ChoiseOnCreating_in, menu

async def on_start_up(_):
    'Bot succesfully started'
    Database()._start()

class CreateColl(StatesGroup):
    name_coll = State()
    img_descr = State()
    photo = State()

class AddingColl(StatesGroup):
    name_coll = State()
    img_descr = State()
    photo = State()

class GetImage(StatesGroup):
    name_coll = State()
    descr = State()

class DeleteColl(StatesGroup):
    choise = State()
    name_coll = State()



class MyBot():
    def __init__(self, api) -> None:
        self.bot = Bot(api)
        self.storage = MemoryStorage()
        self.dp = Dispatcher(self.bot, storage=self.storage)
        self.database = Database()

    def start(self):
        print('Bot succesfully started')
        @self.dp.message_handler(commands=['start', 'help'])
        async def _start(message: types.Message):
            await message.answer(f'Привет {message.from_user.first_name}. {MSG}',reply_markup=MenuButton)

        @self.dp.message_handler() 
        async def echo(message : types.Message):
            if message.text == 'Главное меню' or message.text == 'Список команд':
                await message.answer(f'{message.from_user.first_name}, Выбирай :', reply_markup=OptionsButton)
            else:
                await message.answer('не розумiю')

        @self.dp.callback_query_handler()
        async def all_data(callback : types.CallbackQuery):

            if callback.data == 'create':
                await callback.message.answer('Напиши название для своей коллекции',reply_markup = KeybordButtons)
                await CreateColl.name_coll.set()
                self._create()

            if callback.data == 'add':
                result = self.database.show_collection(callback.from_user.id)
                if result == []:
                    await callback.message.answer('Коллекции еще не созданы, создать новую ?', reply_markup = ChoiseOnCreating_in)
                else:
                    await callback.message.answer('Напиши название для коллекции, в которую ты хочешь добавить фотографию',reply_markup = KeybordButtons)
                    await AddingColl.name_coll.set()
                    self._adding()

            if callback.data == 'show_img':
                res = self.database.show_collection(id = callback.from_user.id)
                if res == []:
                    await callback.message.answer("Коллекции еще не созданы", reply_markup = KeybordButtons)
                else:
                    collections = self.database.show_collection(id = callback.from_user.id)
                    await callback.message.answer('Из какой коллекции хочешь посмотреть фотографию ?',reply_markup = self._gen_but(self.database.show_collection(callback.from_user.id)))
                    for elem in range(len(collections)):
                        await callback.message.answer(f'{elem + 1}) {collections[elem]}')
                    await GetImage.name_coll.set()
                    self._get_image()

            if callback.data == 'delete':
                res = self.database.show_collection(id = callback.from_user.id)
                if res == []:
                    await callback.message.answer("Коллекции еще не созданы", reply_markup = KeybordButtons)
                else:
                    await callback.message.answer('Удалить все коллекции или какую-либо одну ?',reply_markup = DeleteButtons)
                    await DeleteColl.choise.set()
                    self._delete()

            if callback.data == 'show_coll':
                result = self.database.show_collection(callback.from_user.id)
                if result == []:
                    await callback.message.answer('Коллекции еще не созданы')
                else:
                    await callback.message.answer('Твои коллекции :')
                    for elem in result:
                        await callback.message.answer(elem)
            
            if callback.data == 'menu':
                await callback.message.answer(f'{callback.from_user.first_name}, Выбирай:', reply_markup=OptionsButton)


    def _create(self):
        @self.dp.message_handler(state="*", commands='Главное меню')
        @self.dp.message_handler(Text(equals = 'Главное меню', ignore_case = True), state = "*")
        async def cancel(message : types.Message, state = FSMContext):
            curent_state = await state.get_state()
            if curent_state is None:
                return
            await state.finish()
            await message.reply('Возвращаемся в меню',reply_markup = MenuButton)
        
        @self.dp.message_handler(state="*", commands='Добавить')
        @self.dp.message_handler(Text(equals = 'Добавить', ignore_case = True), state = "*")
        async def cancel(message : types.Message, state = FSMContext):
            await message.reply('Напиши описание к фотографии',reply_markup = MenuButton)
            await AddingColl.img_descr.set()
            self._adding()

        @self.dp.message_handler(state="*", commands='Не добавлять')
        @self.dp.message_handler(Text(equals = 'Не добавлять', ignore_case = True), state = "*")
        async def cancel(message : types.Message, state = FSMContext):
            await message.reply('Отменяю создание коллекции',reply_markup = MenuButton)
            await state.finish()
            return

        @self.dp.message_handler(state = CreateColl.name_coll)
        async def name_coll(message : types.Message, state : FSMContext):
            async with state.proxy() as data:
                data['name_coll'] = message.text
            is_allowed = self.database._check_collections(id = message['from']['id'],
                                                          name_coll = data['name_coll'])
            if is_allowed == False:
                await message.answer('Такая коллекция уже существует, добавить в нее фотографии ?',reply_markup=ChoiseOnAdding)
            else:
                await message.reply('Напиши описание для своей фотографии',
                                    reply_markup=KeybordButtons)
                await CreateColl.next()
            
        @self.dp.message_handler(state = CreateColl.img_descr)
        async def img_descr(message : types.Message, state : FSMContext):
            async with state.proxy() as data:
                data['img_descr'] = message.text
            await message.reply('Пришли фотографию, которую хочешь сохранить в коллекцию',
                                 reply_markup=KeybordButtons)
            await CreateColl.next()

        @self.dp.message_handler(content_types=['photo'], state = CreateColl.photo)
        async def load_photo(message : types.Message, state : FSMContext):
            async with state.proxy() as data:
                data['photo'] = message.photo[0].file_id
            result = self.database.create_collection(id = message['from']['id'],
                                                name_coll = data['name_coll'], 
                                                descr = data['img_descr'],
                                                img = data['photo'])
            if result :
                await message.reply(f'Отлично, коллекция {data["name_coll"]} сохранена',
                                    reply_markup=KeybordButtons)
                await state.finish()
                return
            else:
                await message.reply(f'что-то пошло не так...',
                                        reply_markup=KeybordButtons)
                await state.finish()
                return

    def _adding(self):
        @self.dp.callback_query_handler(state="*")
        async def _choise(callback : types.CallbackQuery, state = FSMContext):
            if callback.data == 'create':
                await callback.message.answer('Напиши название для коллекции')
                await CreateColl.name_coll.set()
                self._create()
            if callback.data == 'menu':
                await state.finish()

        @self.dp.message_handler(state="*", commands='Главное меню')
        @self.dp.message_handler(Text(equals = 'Главное меню', ignore_case = True), state = "*")
        async def cancel(message : types.Message, state = FSMContext):
            curent_state = await state.get_state()
            if curent_state is None:
                return
            await state.finish()
            await message.reply('Возвращаемся в меню',reply_markup = MenuButton)

        @self.dp.message_handler(state = AddingColl.name_coll)
        async def name_coll(message : types.Message, state : FSMContext):
            async with state.proxy() as data:
                data['name_coll'] = message.text
            res = self.database._check_collections(id = message['from']['id'],
                                                name_coll = data['name_coll'])
            if res == False:
                await message.reply('Напиши описание для своей фотографии',
                                    reply_markup=KeybordButtons)
                await AddingColl.next()
            else:
                await message.reply('Такой коллекции не существует, создать новую ?',
                                    reply_markup=ChoiseOnCreating_in)


        @self.dp.message_handler(state = AddingColl.img_descr)
        async def img_descr(message : types.Message, state : FSMContext):
            async with state.proxy() as data:
                data['img_descr'] = message.text
            await message.reply(f'Пришли фотографию, которую хочешь добавить в коллекцию {data["name_coll"]}',
                                    reply_markup=KeybordButtons)
            await AddingColl.next()

        @self.dp.message_handler(content_types=['photo'], state = AddingColl.photo)
        async def load_photo(message : types.Message, state : FSMContext):
            async with state.proxy() as data:
                data['photo'] = message.photo[0].file_id
            res = self.database.add_image(id = message.from_user.id,
                                          name_coll = data['name_coll'], 
                                          descr = data['img_descr'],
                                          img = data['photo'])
            if res:
                await message.reply(f'Фотография успешно добавлена',
                                        reply_markup=KeybordButtons)
            else:
                await message.reply(f'Что-то пошло не так',
                                        reply_markup=KeybordButtons)
            await state.finish()
            return

    def _get_image(self):
        @self.dp.message_handler(state="*", commands='Главное меню')
        @self.dp.message_handler(Text(equals = 'Главное меню', ignore_case = True), state = "*")
        async def cancel(message : types.Message, state = FSMContext):
            curent_state = await state.get_state()
            if curent_state is None:
                return
            await state.finish()
            await message.reply('Возвращаемся в меню',reply_markup = MenuButton)

        @self.dp.message_handler(state = GetImage.name_coll)
        async def name_coll(message : types.Message, state : FSMContext):
            collections = self.database.show_collection(id= message.from_user.id)
            async with state.proxy() as data:
                data['name_coll'] = collections[int(message.text) - 1]
            if self.database._check_collections(id = message.from_user.id, name_coll = data['name_coll']):
                await message.answer('Такой коллекции не существует',
                                    reply_markup=KeybordButtons)
                await state.finish()
                return
            else:
                await message.answer('Выбери описание к желаемой фотографии',
                                    reply_markup=KeybordButtons)
            descripitons = self.database._get_descriptions(id = message.from_user.id, name_coll = data['name_coll'])
            for elem in range(len(descripitons)):
                await message.answer(f'{elem + 1}) {descripitons[elem]}', reply_markup = self._gen_but(descripitons))
            await GetImage.next()

        @self.dp.message_handler(state = GetImage.descr)
        async def image(message : types.Message, state : FSMContext):
            async with state.proxy() as data:
                descripitons = self.database._get_descriptions(id = message.from_user.id, name_coll = data['name_coll'])
                data['descr'] = descripitons[int(message.text) - 1]
            descriptions = self.database._get_descriptions(id = message.from_user.id, name_coll = data['name_coll'])
            if data['descr'] in descriptions:
                await message.answer('Ищу фотографию, нужно немного подождать')
                time.sleep(1)
                result = self.database.get_image(id = message.from_user.id, descr = data['descr'])
                await message.answer('Смотри какая красота',
                                        reply_markup=KeybordButtons)
                time.sleep(0.5)
                create_time = result["time"]
                if create_time == None:
                    await message.answer_photo(result['image'], f'{data["name_coll"]}, {data["descr"]}')
                else:
                    await message.answer_photo(result['image'], f'{data["name_coll"]}, {data["descr"]} \nБыла добавлена {str(create_time).split(" ")[0]} в {str(create_time).split(" ")[1]}')
                await state.finish()
                return
            else:
                await message.answer('Фотографии с таким описанием нет в твоей коллекции')
                await state.finish()
                return

    def _delete(self):
        @self.dp.message_handler(state="*", commands='Главное меню')
        @self.dp.message_handler(Text(equals = 'Главное меню', ignore_case = True), state = "*")
        async def cancel(message : types.Message, state = FSMContext):
            curent_state = await state.get_state()
            if curent_state is None:
                return
            await state.finish()
            await message.reply('Возвращаемся в меню',reply_markup = MenuButton)
        
        @self.dp.message_handler(state = DeleteColl.choise)
        async def name_coll(message : types.Message, state : FSMContext):
            async with state.proxy() as data:
                data['choise'] = message.text
            if message.text == 'Отмена':
                await message.answer('Отменяю удаление', reply_markup = KeybordButtons)
                await state.finish()
                return
            if message.text == 'Все коллекции':
                res = self.database.delete_all_coll(id = message.from_user.id, list_coll = self.database.show_collection(message.from_user.id))
                if res:
                    await message.answer('Все коллекции удалены.', reply_markup = KeybordButtons)
                    await state.finish()
                    return
                else:
                    await message.answer('Не получилось удалить :(', reply_markup = KeybordButtons)
            if message.text == 'Одну коллекцию':
                await message.answer('Выбери коллекцию, которую хочешь удалить', reply_markup = self._gen_but(self.database.show_collection(message.from_user.id)))
            collections = self.database.show_collection(id= message.from_user.id)
            for elem in range(len(collections)):
                await message.answer(f'{elem + 1}) {collections[elem]}')
            await DeleteColl.next()


        @self.dp.message_handler(state = DeleteColl.name_coll)
        async def image(message : types.Message, state : FSMContext):
            collections = self.database.show_collection(id= message.from_user.id)
            async with state.proxy() as data:
                data['name_coll'] = collections[int(message.text) - 1]
            res = self.database.delete_one_coll(name_coll = data['name_coll'], id = message.from_user.id)
            if res:
                await message.answer(f'Коллекция {data["name_coll"]} удалена успешно', reply_markup = KeybordButtons)
            else:
                await message.answer('Что-то пошло не так...', reply_markup= KeybordButtons)
            await state.finish()
            return

    def _gen_but(self, descripions : list):
        buttons = ReplyKeyboardMarkup(resize_keyboard = True)
        if len(descripions) == 1:
            butt = KeyboardButton(text= 1)
            buttons.add(butt)
        else:
            for elem in range(len(descripions)):
                butt = KeyboardButton(text= elem + 1)
                buttons.add(butt)
        buttons.add(menu)    
        return buttons
    

def main():
    obj = MyBot(TOKEN)
    obj.start()
    executor.start_polling(dispatcher=obj.dp,
                           on_startup=on_start_up,
                           skip_updates=True)

if __name__ == '__main__':
    main()