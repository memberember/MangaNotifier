import threading
from sqlighter import SQLighter
import time
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram import Bot, Dispatcher, executor, types
import config
import logging
from utils import BotStates
from messages import MESSAGES
import converter as CV
import parseRequests as PR

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
    await message.reply(MESSAGES['start'])


# обработчик команды помощи
@dp.message_handler(commands=['help'])
async def process_help_command(message: types.Message):
    await message.reply(MESSAGES['help'])


# обработчик команды добавления манги
@dp.message_handler(commands=['add'])
async def process_add_url(message: types.Message):
    state = dp.current_state(user=message.from_user.id)
    await message.answer(MESSAGES['write_url'])
    await state.set_state(BotStates.all()[0])


# обработчик команды вывода списка моих тайтлов
@dp.message_handler(commands=['getsubscribed'])
async def get_subcribed(message: types.Message):
    try:
        manga_list = get_manga_list_from_db(message.from_user.id)
        await message.answer(CV.from_manga_list_dict_to_manga_str(manga_dict=manga_list))
    except:
        await message.answer(MESSAGES['empty_manga_list'])


# обработчик команды обновления
@dp.message_handler(state='*', commands=['refresh'])
async def refresh(message: types.Message):
    global global_manga_list
    argument = message.get_args()
    start_time = time.time()

    # турбо поиск по команде /refresh t
    if argument.lower() == 't' and message.from_user.id == ADMIN_USER_ID:
        await message.answer(MESSAGES['fast_search_is_started'])
        updates = get_fast_updates(message.from_user.id)
    else:
        await message.answer(MESSAGES['search_is_started'])
        updates = get_updates(message.from_user.id)
    for update in updates:
        await message.answer(update)
    await message.answer("\nПоиск занял %s секунд" % (time.time() - start_time))


# обработчик команды удаления тайтла
@dp.message_handler(commands=['delete'])
async def refresh(message: types.Message):
    state = dp.current_state(user=message.from_user.id)
    await message.answer(MESSAGES['write_manga_id_to_delete'])
    await state.set_state(BotStates.all()[1])


# обработчик добавления ссылки на мангу
@dp.message_handler(state=BotStates.MANGA_ADDITION_STATE)
async def manga_addition_handler(message: types.Message):
    state = dp.current_state(user=message.from_user.id)

    try:

        # если пользователь не отменил ввод, то начинаем поиск
        if message.text != '/cancel':
            url_list = CV.text_to_splitted(message.text)
            for url in url_list:
                answer = add_manga(message.from_user.id, url)
                await message.answer(answer)
        else:
            # посылаем сообщение об отмене
            await message.answer(MESSAGES['canceled'])
            # сброс состояния
        await state.reset_state()

        # сообщение об ошибке
    finally:
        pass
        # await message.answer(MESSAGES['error_try_again'])


# обработчик удаления манги
@dp.message_handler(state=BotStates.MANGA_DELETE_STATE)
async def manga_delete_handler(message: types.Message):
    state = dp.current_state(user=message.from_user.id)

    try:

        # проверка на отмену команды
        if message.text != '/cancel':
            id_list = CV.text_to_splitted(message.text)
            for id in id_list:
                answer = delete_manga_from_bd(message.from_user.id, id)
                await message.answer(answer)
        else:
            await message.answer(MESSAGES['canceled'])
        await state.reset_state()
    except:
        await message.answer(MESSAGES['error_try_again'])


@dp.message_handler()
async def echo_message(msg: types.Message):
    await bot.send_message(msg.from_user.id, msg.text)


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
        print(manga)
        # проверка спарсилась ли манга
        if manga != 0:
            db.add_manga(
                user_id=user_id,
                url=url,
                last_chapter=manga['last_chapter'],
                name=manga['manga_name'],
            )
            return MESSAGES['manga_sucsesfully_added'].format(manga['manga_name'])
        return MESSAGES['data_error'].format(url)
    return MESSAGES['you_already_have_this_manga'].format(url)


# функция удаления манги с БД
def delete_manga_from_bd(user_id, id):
    if db.is_user_have_manga_by_id(user_id, id):
        db.delete_manga(user_id=user_id, id=id)
        return MESSAGES['sucsessfully_deleted'].format(id)
    else:
        return MESSAGES['dont_have_such_manga'].format(id)


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
    return CV.from_short_updated_manga_list_to_str(updates)


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
    return CV.from_short_updated_manga_list_to_str(data)


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
    # dp.loop.create_task(scheduled(10))  # пока что оставим 10 секунд (в качестве теста)
    lock = threading.Lock()
    thread_list = []
    global_manga_list = []
    data = []
    executor.start_polling(dp, on_shutdown=shutdown)
