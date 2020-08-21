import threading
from sqlighter import SQLighter
import time
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram import Bot, Dispatcher, executor, types
import config
import logging
from utils import TestStates
from messages import MESSAGES
import parseRequests as PR
import converter as CV
from selenium import webdriver

# задаем уровень логов
logging.basicConfig(level=logging.INFO)

# инициализируем бота
bot = Bot(token=config.MANGA_API_TOKEN)
# bot = Bot(token=config.TEST_API_TOKEN)
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
    await state.set_state(TestStates.all()[0])


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
    global urls
    argument = message.get_args()
    start_time = time.time()

    # турбо поиск по команде /refresh t
    if argument.lower() == 't' and message.from_user.id == 507981523:
        await message.answer(MESSAGES['fast_search_is_started'])
        urls = get_manga_list_from_db(507981523)
        updates = get_fast_updates(message.from_user.id)
    else:
        await message.answer(MESSAGES['search_is_started'])
        updates = get_updates(message.from_user.id)
    await message.answer(updates)
    await message.answer("Поиск занял %s секунд" % (time.time() - start_time))


# обработчик команды удаления тайтла
@dp.message_handler(commands=['delete'])
async def refresh(message: types.Message):
    state = dp.current_state(user=message.from_user.id)
    await message.answer(MESSAGES['write_manga_id_to_delete'])
    await state.set_state(TestStates.all()[1])


# обработчик добавления ссылки на мангу
@dp.message_handler(state=TestStates.MANGA_ADDITION_STATE)
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
    except:
        await message.answer(MESSAGES['error_try_again'])


# обработчик удаления манги
@dp.message_handler(state=TestStates.MANGA_DELETE_STATE)
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
        manga = PR.get_manga_information(url)

        # проверка спарсилась ли манга
        if manga != 0:
            db.add_manga(
                user_id=user_id,
                url=url,
                last_chapter=manga['last_chapter'],
                name=manga['manga_name'],
                site_type=manga['site_type'],
            )
            return MESSAGES['manga_sucsesfully_added'].format(manga['manga_name'], manga['site_type'])
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
            'site_type': title[5],
            'url': title[2]
        })
    return manga_list


# команда получения url списка манги из БД
# def get_manga_urls_from_db(user_id):
#     manga = db.get_manga(user_id)
#     manga_urls = []
#     for title in manga:
#         manga_urls.append(title[2])
#     return manga_urls


# функция обновления базы данных на новые данные
def update_db(user_id, manga_list):
    for manga in manga_list:
        if manga != None:
            db.update_manga(user_id=user_id,
                            id=manga['id'],
                            last_chapter=manga['last_chapter'])


# функция получения обновлений манги
def get_updates(user_id):
    list_from_db = get_manga_list_from_db(user_id)
    updates = PR.get_manga_chapters(list_from_db)
    update_db(user_id, updates)
    return CV.from_updated_manga_list_to_str(updates)


# турбо обновления
def get_fast_updates(user_id):
    global urls
    global thread_list
    thread_list = []
    for i in range(4):
        thread_b = threading.Thread(target=processing)
        thread_list.append(thread_b)
        thread_b.start()
    while len(thread_list) > 0:
        time.sleep(1)
    update_db(user_id, data)
    return CV.from_updated_manga_list_to_str(data)


# функция турбо поиска обновлений
def processing():
    global thread_list
    driver = webdriver.Chrome()
    while len(urls) > 0:
        with lock:
            thisurl = urls.pop(-1)
        s = PR.get_manga_updates(thisurl, driver)
        with lock:
            data.append(s)
    driver.close()
    with lock:
        thread_list.pop(-1)


# запускаем лонг поллинг
if __name__ == '__main__':
    # dp.loop.create_task(scheduled(10))  # пока что оставим 10 секунд (в качестве теста)
    lock = threading.Lock()
    thread_list = []
    urls = []
    data = []
    executor.start_polling(dp, on_shutdown=shutdown)
    # manga_list = [
    #               {'id': 2, 'manga_name': 'Onepunchman (Ванпанчмен)', 'last_chapter': '27 - 175',
    #                'site_type': 'manga-chan', 'url': 'https://manga-chan.me/manga/17079-onepunchman.html'},
    #               {'id': 15, 'manga_name': 'Милый дом', 'last_chapter': '1 - 114', 'site_type': 'readmanga',
    #                'url': 'https://readmanga.live/sweet_home__kim_carnby_'}]
    #
    # print(PR.get_manga_chapters(manga_list))
    # print(PR.test())
