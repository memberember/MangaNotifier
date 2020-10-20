import re
import pages.locators as P


def from_manga_list_dict_to_manga_str(manga_dict):
    manga_list_string = ''
    for manga in manga_dict:
        manga_list_string += '[{}] {} {}\n'.format(manga['id']
                                                   , manga['manga_name']
                                                   , manga['last_chapter'])
    return manga_list_string


def from_short_updated_manga_list_to_str(updates):
    buffer = ''
    message = ['Нет обновлений']
    if len(updates) > 0:
        message[0] = 'Вышли новые главы:\n'
        for update in updates:
            buffer += '{} {}\t->\t{} \t{}\n'.format(update['manga_name'],
                                                    update['prev_chapter'],
                                                    update['last_chapter'],
                                                    update['url'])

            if len(buffer) > 2000:
                print(buffer)
                message.append(buffer)
                buffer = ""
    if len(buffer) > 0:
        message.append(buffer)
    return message


def text_to_splitted(text):
    first_step = text.split('\n')
    second_step = []
    third_step = []

    for step in first_step:
        second_step += step.split()

    for step in second_step:
        third_step += step.split(',')

    return third_step


def text_to_date_and_chapter_url_dict(text, url):
    chapter_date = re.search(P.chapter_date_re, text)[0]
    return {
        'url': url,
        'date': chapter_date
    }
