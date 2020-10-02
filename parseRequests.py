from selenium import webdriver
import re
import patterns as P
import converter as CV


# todo оптимизировать под множество манги
# функция получения информации по манге
def get_manga_information(target_url):
    try:
        pattern = get_url_pattern(target_url)
        name_xpath = pattern['name_xpath']
        cutter_re = pattern['chapter_cutter_re']
        last_chapter_xpath = pattern['last_chapter_xpath']
        url_xpath = pattern['last_manga_url_xpath']
        site_type = target_url.split('/')[2].split('.')[0]
    except:
        pass
    try:

        driver = webdriver.Chrome()
        driver.get(target_url)
        manga_name = driver.find_element_by_xpath(name_xpath).text
        last_chapter = re.search(cutter_re,
                                 driver.find_element_by_xpath(
                                     last_chapter_xpath)
                                 .text)[0]
        chapter_url = driver.find_element_by_xpath(url_xpath).get_attribute('href')
        driver.quit()
        return {'manga_name': manga_name,
                'last_chapter': last_chapter,
                'chapter_url': chapter_url,
                'site_type': site_type}
    except:
        driver.quit()
        return 0


# функция возвращения паттерна парсинга
def get_url_pattern(target_url):
    try:
        if target_url.__contains__('readmanga') or target_url.__contains__('mintmanga'):
            return P.Readmanga
        elif target_url.__contains__('manga-chan'):
            return P.Mangachan
        else:
            return 0
    except:
        return 0


# функция получения набора данных для парсинга сайта
def get_manga_define_dataset(site_type):
    if site_type == 'manga-chan':
        return P.Mangachan
    elif site_type == 'readmanga' or site_type == 'mintmanga':
        return P.Readmanga


# todo может получится ускорить поиск глав без выкачивания полного списка или при помощи IE
# функция получения последних глав по манге
def get_manga_chapters(manga_list):
    # инициализируем опции хрома (отключаем подгрузку изображений)
    option = webdriver.ChromeOptions()
    chrome_prefs = {}
    option.experimental_options["prefs"] = chrome_prefs
    chrome_prefs["profile.default_content_settings"] = {"images": 2}
    chrome_prefs["profile.managed_default_content_settings"] = {"images": 2}
    driver = webdriver.Chrome(chrome_options=option)

    # создаем пустой массив обновлений
    updates = []

    # цикл для прогонки большого количества манги
    for manga in manga_list:

        # обработчик ошибок
        try:

            # получаем шаблоны по которым будем парсить данные
            cutter_re = P.chapter_number_re
            this_manga_pattern = get_manga_define_dataset(manga['site_type'])
            chapter_xpath = this_manga_pattern['chapter_xpath']
            last_chapter_xpath = this_manga_pattern['last_chapter_xpath']
            name_xpath = this_manga_pattern['name_xpath']

            # открываем ссылку и создаем пустой массив с новыми главами
            driver.get(manga['url'])
            new_chapters = []

            # процесс парсинга
            chapters = driver.find_elements_by_xpath(chapter_xpath)
            manga_name = driver.find_element_by_xpath(name_xpath).text
            last_chapter = re.search(cutter_re,
                                     driver.find_element_by_xpath(
                                         last_chapter_xpath)
                                     .text)[0]

            # процесс проверки глав на новизну
            for chapter in chapters:

                # TODO баг в манге Герой? Я давно перестал им быть на главе 1-117 когда за день вышло больше 30 глав
                # todo исправить кастыль в виде try except
                try:
                    chapter_num = re.search(cutter_re,
                                            chapter.text)[1]
                    chapter_url = chapter.find_element_by_tag_name('a').get_attribute('href')
                    new_chapter = CV.text_to_date_and_chapter_url_dict(chapter.text, chapter_url)

                    # если дошли до главы которую мы читали последней выходим из цикла и добавляем записи в обновления
                    if (chapter_num == manga['last_chapter']):
                        updates.append({
                            'manga_name': manga_name,
                            'last_chapter': last_chapter,
                            'new_chapters': new_chapters,
                            'id': manga['id']
                        }
                        )
                        break

                    # иначе, если главу не читали, то добавляем ее как новую главу
                    new_chapters.append(new_chapter)

                except:

                    # TODO исправить костыль для бага с мангой 30+
                    updates.append({
                        'manga_name': manga_name,
                        'last_chapter': last_chapter,
                        'new_chapters': new_chapters,
                        'id': manga['id']
                    }
                    )
                    break
        except:
            pass

    # закрытие браузера
    driver.quit()
    return updates


# функция получения последних глав по манге
def get_manga_list_last_chapters(manga_list):
    # инициализируем опции хрома (отключаем подгрузку изображений)
    option = webdriver.ChromeOptions()
    chrome_prefs = {}
    option.experimental_options["prefs"] = chrome_prefs
    chrome_prefs["profile.default_content_settings"] = {"images": 2}
    chrome_prefs["profile.managed_default_content_settings"] = {"images": 2}
    driver = webdriver.Chrome(chrome_options=option)

    # создаем пустой массив обновлений
    updates = []

    # цикл для прогонки большого количества манги
    for manga in manga_list:

        # обработчик ошибок
        try:

            # получаем шаблоны по которым будем парсить данные
            cutter_re = P.chapter_number_re
            this_manga_pattern = get_manga_define_dataset(manga['site_type'])
            last_chapter_xpath = this_manga_pattern['last_chapter_xpath']
            name_xpath = this_manga_pattern['name_xpath']

            driver.get(manga['url'])
            manga_name = driver.find_element_by_xpath(name_xpath).text
            last_chapter = re.search(cutter_re,
                                     driver.find_element_by_xpath(
                                         last_chapter_xpath)
                                     .text)[0]

            if (manga['last_chapter'] != last_chapter):
                updates.append({
                    'manga_name': manga_name,
                    'last_chapter': last_chapter,
                    'id': manga['id'],
                    'url': manga['url'],
                    'prev_chapter': manga['last_chapter']
                }
                )

        except:
            pass

    # закрытие браузера
    driver.quit()
    return updates


# todo поставить try catch и проверить
# функция получения последних глав по манге (турбо режим)
def get_manga_updates_turbo(manga, driver):
    cutter_re = P.chapter_number_re
    this_manga_pattern = get_manga_define_dataset(manga['site_type'])
    chapter_xpath = this_manga_pattern['chapter_xpath']
    last_chapter_xpath = this_manga_pattern['last_chapter_xpath']
    name_xpath = this_manga_pattern['name_xpath']
    driver.get(manga['url'])
    new_chapters = []
    chapters = driver.find_elements_by_xpath(chapter_xpath)
    manga_name = driver.find_element_by_xpath(name_xpath).text
    last_chapter = re.search(cutter_re,
                             driver.find_element_by_xpath(
                                 last_chapter_xpath)
                             .text)[0]
    update = {
        'manga_name': manga_name,
        'last_chapter': last_chapter,
        'new_chapters': new_chapters,
        'id': manga['id']
    }

    for chapter in chapters:
        chapter_num = re.search(cutter_re,
                                chapter.text)[0]

        chapter_url = chapter.find_element_by_tag_name('a').get_attribute('href')
        new_chapter = CV.text_to_date_and_chapter_url_dict(chapter.text, chapter_url)
        if chapter_num == manga['last_chapter']:
            update = {
                'manga_name': manga_name,
                'last_chapter': last_chapter,
                'new_chapters': new_chapters,
                'id': manga['id']
            }
            break
        new_chapters.append(new_chapter)
    return update


def test():
    try:
        url = 'https://manga-chan.me/manga/17079-onepunchman.html'
        xpath = '//*[@id="tc_1"]/tbody/tr[*]/td[1]/div/a/../../..'
        driver = webdriver.Chrome()
        driver.get(url)
        chapters = driver.find_elements_by_xpath(xpath)

        chapter_url = chapters[0].find_element_by_tag_name('a').get_attribute('href')
        new_chapter = CV.text_to_date_and_chapter_url_dict(chapters[0].text, chapter_url)
        print(new_chapter)
        driver.quit()
    except:
        driver.quit()
