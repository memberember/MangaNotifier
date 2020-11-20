from messages import Messages
import keyboards as kb


def from_manga_list_dict_to_btn(manga_dict):
    inline_kb = kb.InlineKeyboardMarkup()
    for manga in manga_dict:
        buffer = '[{}] {} {}\n'.format(manga['id'], manga['manga_name'], manga['last_chapter'])
        inline_kb.add(kb.InlineKeyboardButton(buffer, url=manga['url']))
    return inline_kb


def from_short_updated_manga_list_to_str(updates):
    # todo сделать выдачу ошибки
    buffer = ''
    message = [Messages.updates_not_found]
    if len(updates) > 0:
        message[0] = Messages.new_chapters_already
        for update in updates:
            buffer += '{} {}\t->\t{} \t{}\n'.format(update['manga_name'],
                                                    update['prev_chapter'],
                                                    update['last_chapter'],
                                                    update['url'])

            if len(buffer) > 2000:
                message.append(buffer)
                buffer = ""
    if len(buffer) > 0:
        message.append(buffer)
    return message


def text_to_split(text):
    first_step = text.split('\n')
    second_step = []
    third_step = []

    for step in first_step:
        second_step += step.split()

    for step in second_step:
        third_step += step.split(',')

    return third_step


# конвертер глав в кнопки
def from_updates_to_inline_btn(updates):
    inline_kb = kb.InlineKeyboardMarkup()
    if len(updates) > 0:
        for update in updates:
            buffer = '{}\t->\t{} {}'.format(update['prev_chapter'],
                                            update['last_chapter'],
                                            update['manga_name'])
            inline_kb.add(kb.InlineKeyboardButton(buffer, url=update['url']))
        return {'msg': Messages.new_chapters_already,
                'kb': inline_kb}
    return {'msg': Messages.updates_not_found,
            'kb': kb.main_markup}
