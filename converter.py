import re
import patterns as P


def from_manga_list_dict_to_manga_str(manga_dict):
    manga_list_string = ''
    for manga in manga_dict:
        manga_list_string += '[{}] {} {} {}\n'.format(manga['id']
                                                      , manga['manga_name']
                                                      , manga['last_chapter']
                                                      , manga['site_type'])
    return manga_list_string


def from_updated_manga_list_to_str(updates):
    message = 'Нет обновлений\n'
    for update in updates:
        if update != None:
            if len(update['new_chapters']) > 0:
                if message == 'Нет обновлений\n':
                    message = 'Вышли новые главы:'
                message += '{}\n'.format(update['manga_name'])
                for chapter in update['new_chapters']:
                    message += '{} {}\n'.format(chapter['url'], chapter['date'])
                message += '\n'
    return message


def from_short_updated_manga_list_to_str(updates):
    message = 'Нет обновлений\n'
    if len(updates)>0:
        message = 'Вышли новые главы:\n'
        for update in updates:
            print(update['manga_name'])
            message += '{} {}\t->\t{} \t{}\n'.format(update['manga_name'],
                                                     update['prev_chapter'],
                                                     update['last_chapter'],
                                                     update['url'])
            message += '\n'
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
