locatorArray = []

chapter_number_re = '((?:\d){1,3}\s?-?\s?(?:\d){1,4})'
chapter_normalize_re = r"\t|(\s\s)|\n"


# todo переделать в базу данных
class Pattern:
    def __init__(self,
                 url_container,
                 last_chapter,
                 name):
        self.url_container = url_container
        self.last_chapter = last_chapter
        self.name = name


ReadManga = Pattern(
    url_container='readmanga',
    last_chapter='//*[@id="mangaBox"]/div[2]/div[1]/div[1]/div[*]/h4/a',
    name='//div[2]/h1/span[1]',
)

MintManga = Pattern(
    url_container='mintmanga',
    last_chapter='//*[@id="mangaBox"]/div[2]/div[1]/div[1]/div[*]/h4/a',
    name='//div[2]/h1/span[1]',
)

MangaChan = Pattern(
    url_container='manga-chan',
    last_chapter='//*[@id="tc_1"]//tr[3]/td[1]/div/a',
    name='//*[@id="info_wrap"]/div/div/h1/a',
)

ManhwaTop = Pattern(
    url_container='manhwatop',
    last_chapter='//div/div[4]/div/ul/li[1]/a',
    name='//div[1]/div/ol/li[3]/a',
)

MangaReader = Pattern(
    url_container='mangareader',
    last_chapter='//*[@id="main"]/div[3]//div[2]//li[1]/a',
    name='//*[@class="name"]',
)

Niadd = Pattern(
    url_container='niadd',
    last_chapter='//div[4]//a/div/div[2]',
    name='//*[@class="book-headline-name"]',
)

locatorsArray = [ReadManga, MintManga, MangaChan, ManhwaTop, MangaReader, Niadd]


def get_locator(url):
    for locator in locatorsArray:
        if url.__contains__(locator.url_container):
            return locator
