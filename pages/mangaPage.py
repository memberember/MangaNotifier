from .locators import *
import re
import requests
from lxml import html


class MangaPage:
    def __init__(self, url):
        self.url = url
        self.locator = get_locator(url)
        self.pageTree = ''

    # открыть страницу
    def open(self):
        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.9; rv:45.0) Gecko/20100101 Firefox/45.0'
        }

        r = requests.get(self.url, headers)
        self.pageTree = html.fromstring(r.text)

    # получить последнюю главу
    def get_last_chapter(self):
        last_chapter = self.pageTree.xpath(self.locator.last_chapter)[0].text
        return re.search(chapter_number_re, last_chapter)[0]

    # полчить название
    def get_name(self):
        return self.pageTree.xpath(self.locator.name)[0].text
