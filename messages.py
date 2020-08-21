from utils import TestStates

help_message = 'Мои команды такие:\n' \
               '➕/add - добавляет новую мангу по ссылке в твой список\n' \
               '❌/delete - удаляет мангу по айди из твоего списка\n' \
               '🍀/getsubcribed - выводит список твоей манги\n' \
               '🔮/refresh - говорит тебе что обновилось в твоем списке\n' \
               '📖/help - выводит мои команды'

start_message = 'Привет!👋 Я бот который поможет тебе следить за большим количеством манги и ' \
                'сэкономить свое время. Я могу работать с readmanga и manga-chan!\n' + help_message
write_url_message = 'Введите ссылку на тайтл или /cancel чтобы отменить'
empty_manga_list_message = 'У вас еще нет списка манги'
error_try_again_message = 'Ошибка, попробуйте снова'
data_error_message = 'Ошибка, проверьте правильность данных для {}'
write_manga_id_to_delete_message = 'Введите id манги которую хотите удалить или /cancel чтобы отменить'
sucsessfully_deleted_message = 'Манга с id = {} успешно удалена'
canceled_message = 'Отменено'
manga_sucsesfully_added_message = 'Манга {}[{}] успешно добавлена!'
dont_have_such_manga_message = 'У вас нет манги с id = {}'
search_is_started_message = 'Я началь искать...'
fast_search_is_started_message = 'Включаю турбо поиск'
you_already_have_this_manga = 'У вас уже есть эта манга - {}'
MESSAGES = {
    'start': start_message,
    'help': help_message,
    'write_url': write_url_message,
    'empty_manga_list': empty_manga_list_message,
    'error_try_again': error_try_again_message,
    'write_manga_id_to_delete': write_manga_id_to_delete_message,
    'sucsessfully_deleted': sucsessfully_deleted_message,
    'canceled': canceled_message,
    'manga_sucsesfully_added': manga_sucsesfully_added_message,
    'dont_have_such_manga': dont_have_such_manga_message,
    'search_is_started': search_is_started_message,
    'fast_search_is_started': fast_search_is_started_message,
    'data_error': data_error_message,
    'you_already_have_this_manga': you_already_have_this_manga
}
