import threading
from sqlighter import SQLighter
import time
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram import Bot, Dispatcher, executor, types
import config
import logging
from utils import BotStates
from messages import Messages
import converter as CV
import parseRequests as PR
import keyboards as kb

# задаем уровень логов
logging.basicConfig(level=logging.INFO)

# инициализируем бота
bot = Bot(token=config.MANGA_API_TOKEN)
ADMIN_USER_ID = config.ADMIN_USER_ID

dp = Dispatcher(bot, storage=MemoryStorage())

# todo попробовать сделать бд на сервере
# инициализируем соединение с БД
db = SQLighter('dborig.db')


# обработчик команды старта
@dp.message_handler(commands=['start'])
async def process_start_command(message: types.Message):
    await message.answer(Messages.welcome)
    await message.answer(Messages.send_btns, reply_markup=kb.main_markup)


# обработчик команды помощи
@dp.message_handler(commands=['help'])
async def process_help_command(message: types.Message):
    await message.reply(Messages.commands, reply_markup=kb.main_markup)


# обработчик команды добавления манги
@dp.message_handler(commands=['add'])
async def process_add_url(message: types.Message):
    state = dp.current_state(user=message.from_user.id)
    await message.answer(Messages.write_url, reply_markup=kb.undo_addition_markup)
    await state.set_state(BotStates.all()[0])


# обработчик команды вывода списка моих тайтлов
@dp.message_handler(commands=['getsubscribed'])
async def process_get_subcribed(message: types.Message):
    try:
        manga_list = get_manga_list_from_db(message.from_user.id)

        # преобразование списка в кнопки
        answers = CV.from_manga_list_dict_to_btn(manga_list)

        # список из ответов
        for answer in answers:
            await message.answer(answer['msg'], reply_markup=answer['kb'])
    except:
        await message.answer(Messages.empty_manga_list)


# обработчик команды обновления
@dp.message_handler(state='*', commands=['refresh'])
async def process_refresh(message: types.Message):
    global global_manga_list
    argument = message.get_args()
    start_time = time.time()

    # турбо поиск по команде /refresh t
    if argument.__str__().lower() == 't' or message.from_user.id == ADMIN_USER_ID:
        await message.answer(Messages.fast_search_is_started)
        updates = get_fast_updates(message.from_user.id)
    else:
        await message.answer(Messages.search_is_started)
        updates = get_updates(message.from_user.id)
    msg = CV.from_updates_to_inline_btn(updates)
    await message.answer(msg['msg'], reply_markup=msg['kb'])
    await message.answer(Messages.search_time_is % (time.time() - start_time))


# обработчик команды удаления тайтла
@dp.message_handler(commands=['delete'])
async def proc_delete(message: types.Message):
    state = dp.current_state(user=message.from_user.id)
    await message.answer(Messages.write_manga_id_to_delete, reply_markup=kb.undo_delition_markup)
    await state.set_state(BotStates.all()[1])


# обработчик добавления ссылки на мангу
@dp.message_handler(state=BotStates.MANGA_ADDITION_STATE)
async def manga_addition_handler(message: types.Message):
    state = dp.current_state(user=message.from_user.id)

    try:

        # если пользователь не отменил ввод, то начинаем поиск
        if message.text != '/cancel' and message.text != Messages.undo_accept:
            url_list = CV.text_to_split(message.text)
            for url in url_list:
                answer = add_manga(message.from_user.id, url)
                await message.answer(answer, reply_markup=kb.main_markup)
        else:
            # посылаем сообщение об отмене
            await message.answer(Messages.canceled, reply_markup=kb.main_markup)
            # сброс состояния
        await state.reset_state()

        # сообщение об ошибке
    except:
        await message.answer(Messages.error_try_again)


# обработчик удаления манги
@dp.message_handler(state=BotStates.MANGA_DELETE_STATE)
async def manga_delete_handler(message: types.Message):
    state = dp.current_state(user=message.from_user.id)

    try:

        # проверка на отмену команды
        if message.text != '/cancel' and message.text != Messages.undo_delete:
            id_list = CV.text_to_split(message.text)
            for id in id_list:
                answer = delete_manga_from_bd(message.from_user.id, id)
                await message.answer(answer, reply_markup=kb.main_markup)
        else:
            await message.answer(Messages.canceled, reply_markup=kb.main_markup)

        await state.reset_state()
    except:
        await message.answer(Messages.error_try_again)


# обработчик сообщений с кнопок
@dp.message_handler()
async def echo_message(message: types.Message):
    if message.text == Messages.add:
        await process_add_url(message)
    elif message.text == Messages.delete:
        await proc_delete(message)
    elif message.text == Messages.get_subscribed_list:
        await process_get_subcribed(message)
    elif message.text == Messages.refresh:
        await process_refresh(message)
    elif message.text == Messages.commands:
        await message.answer(Messages.my_commands)
    else:
        await bot.send_message(message.from_user.id, message.text, reply_markup=kb.main_markup)


async def shutdown(dispatcher: Dispatcher):
    await dispatcher.storage.close()
    await dispatcher.storage.wait_closed()


# функция добавления манги
def add_manga(user_id, url):
    is_user_have_manga_by_url = db.is_user_have_manga_by_url(user_id, url)

    # проверка наличия этой манги у пользователя
    if not is_user_have_manga_by_url:

        # получение информации о манге
        manga = PR.get_manga(url)
        # проверка спарсилась ли манга
        if manga != 0:
            db.add_manga(
                user_id=user_id,
                url=url,
                last_chapter=manga['last_chapter'],
                name=manga['manga_name'],
            )
            return Messages.manga_sucsesfully_added.format(manga['manga_name'])
        return Messages.data_error.format(url)
    return Messages.you_already_have_this_manga.format(url)


# функция удаления манги с БД
def delete_manga_from_bd(user_id, id):
    manga = db.get_manga_by_id(user_id, id)
    if bool(len(manga)):
        db.delete_manga(user_id=user_id, id=id)
        return Messages.sucsessfully_deleted.format(manga[-1])
    else:
        return Messages.dont_have_such_manga.format(id)


# команда получения списка манги из БД
def get_manga_list_from_db(user_id):
    manga = db.get_manga(user_id)
    manga_list = []
    for title in manga:
        manga_list.append({
            'id': title[0],
            'manga_name': title[4],
            'last_chapter': title[3],
            'url': title[2]
        })
    return manga_list


# функция обновления базы данных на новые данные
def update_db(user_id, manga_list):
    for manga in manga_list:
        if manga != None:
            db.update_manga(user_id=user_id,
                            id=manga['id'],
                            last_chapter=manga['last_chapter'])


# короткие обновления
def get_updates(user_id):
    list_from_db = get_manga_list_from_db(user_id)

    updates = PR.get_manga_list_last_chapters(list_from_db)
    update_db(user_id, updates)
    return updates


# турбо обновления
def get_fast_updates(user_id):
    # объявление глобальных переменных
    global global_manga_list
    global thread_list
    global data

    # очистка глобальных переменных
    global_manga_list = get_manga_list_from_db(user_id)
    thread_list = []
    data = []

    # распределение потоков
    for i in range(10):
        thread_b = threading.Thread(target=processing)
        thread_list.append(thread_b)
        thread_b.start()
    while len(thread_list) > 0:
        time.sleep(1)
    update_db(user_id, data)
    return data


# функция турбо поиска обновлений
def processing():
    global thread_list
    global data
    while len(global_manga_list) > 0:
        with lock:
            manga = global_manga_list.pop(-1)
        s = PR.get_manga_updates_turbo(manga)

        # проверка на пустоту ответа
        if s != 0:
            with lock:
                data.append({
                    'manga_name': s["manga_name"],
                    'last_chapter': s["last_chapter"],
                    'id': manga['id'],
                    'url': manga['url'],
                    'prev_chapter': manga['last_chapter']
                })
    with lock:
        thread_list.pop(-1)


# запускаем лонг поллинг
if __name__ == '__main__':
    lock = threading.Lock()
    thread_list = []
    global_manga_list = []
    data = []
    executor.start_polling(dp, on_shutdown=shutdown)
