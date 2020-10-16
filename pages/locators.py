locatorArray = []

chapter_number_re = '((?:\d){1,3}\s-\s(?:\d){1,4})'
chapter_date_re = '((?:\d){1,4}[-.](?:\d){2}[-.](?:\d){2})'


class Pattern:
    def __init__(self,
                 url_container,
                 last_chapter,
                 last_manga_url,
                 name,
                 chapters):
        self.url_container = url_container
        self.last_chapter = last_chapter
        self.last_manga_url = last_manga_url
        self.name = name
        self.chapters = chapters


ReadManga = Pattern(
    url_container='readmanga',
    last_chapter='//*[@id="mangaBox"]/div[2]/div[1]/div[1]/div[*]/h4/a',
    last_manga_url='//div[*]/table/tbody/tr[1]/td[1]/a',
    name='//div[2]/h1/span[1]',
    chapters='//*[@id="mangaBox"]/div[2]/div[*]/table/tbody/tr[*]',
)

MintManga = Pattern(
    url_container='mintmanga',
    last_chapter='//*[@id="mangaBox"]/div[2]/div[1]/div[1]/div[*]/h4/a',
    last_manga_url='//div[*]/table/tbody/tr[1]/td[1]/a',
    name='//div[2]/h1/span[1]',
    chapters='//*[@id="mangaBox"]/div[2]/div[*]/table/tbody/tr[*]',
)

MangaChan = Pattern(
    url_container='manga-chan',
    last_chapter='//*[@id="tc_1"]//tr[3]/td[1]/div/a',
    last_manga_url='//tbody/tr[*]/td[1]/div/a',
    name='//*[@id="info_wrap"]/div/div/h1/a',
    chapters='//table[*]//tr[*]/td[1]/div/a/text()',
)

locatorsArray = [ReadManga, MintManga, MangaChan]


def get_locator(url):
    for locator in locatorsArray:
        if url.__contains__(locator.url_container):
            return locator
