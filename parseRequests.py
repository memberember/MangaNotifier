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
        return 0
    try:

        driver = webdriver.Chrome()
        driver.get(target_url)
        manga_name = driver.find_element_by_xpath(name_xpath).text
        last_chapter = re.search(cutter_re,
                                 driver.find_element_by_xpath(
                                     last_chapter_xpath)
                                 .text)[0]
        chapter_url = driver.find_element_by_xpath(url_xpath).get_attribute('href')
        driver.close()
        return {'manga_name': manga_name,
                'last_chapter': last_chapter,
                'chapter_url': chapter_url,
                'site_type': site_type}
    except:
        driver.close()
        return 0


# функция возвращения паттерна парсинга
# todo добавить mintmanga
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


# todo оптимизировать
# функция получения набора данных для парсинга сайта
def get_manga_define_dataset(site_type):
    if site_type == 'manga-chan':
        return P.chapter_number_re, P.mangachan_chapter_xpath, P.mangachan_last_chapter_xpath, P.mangachan_name_xpath
    elif site_type == 'readmanga' or site_type == 'mintmanga':
        return P.chapter_number_re, P.readmanga_chapter_xpath, P.readmanga_last_chapter_xpath, P.readmanga_name_xpath


# функция получения последних глав по манге
def get_manga_chapters(manga_list):
    option = webdriver.ChromeOptions()
    chrome_prefs = {}
    option.experimental_options["prefs"] = chrome_prefs
    chrome_prefs["profile.default_content_settings"] = {"images": 2}
    chrome_prefs["profile.managed_default_content_settings"] = {"images": 2}
    driver = webdriver.Chrome(chrome_options=option)

    updates = []
    for manga in manga_list:
        try:
            cutter_re, chapter_xpath, last_chapter_xpath, name_xpath = get_manga_define_dataset(manga['site_type'])
            driver.get(manga['url'])
            new_chapters = []
            chapters = driver.find_elements_by_xpath(chapter_xpath)
            manga_name = driver.find_element_by_xpath(name_xpath).text
            last_chapter = re.search(cutter_re,
                                     driver.find_element_by_xpath(
                                         last_chapter_xpath)
                                     .text)[0]
            for chapter in chapters:

                chapter_num = re.search(cutter_re,
                                        chapter.text)[0]

                chapter_url = chapter.find_element_by_tag_name('a').get_attribute('href')
                new_chapter = CV.text_to_date_and_chapter_url_dict(chapter.text, chapter_url)

                if (chapter_num == manga['last_chapter']):
                    updates.append({
                        'manga_name': manga_name,
                        'last_chapter': last_chapter,
                        'new_chapters': new_chapters,
                        'id': manga['id']
                    }
                    )
                    break
                new_chapters.append(new_chapter)
        except:
            pass
    driver.close()
    return updates


# функция получения последних глав по манге (турбо режим)
def get_manga_updates(manga, driver):
    cutter_re, chapter_xpath, last_chapter_xpath, name_xpath = get_manga_define_dataset(manga['site_type'])
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
        driver.close()
    except:
        driver.close()
