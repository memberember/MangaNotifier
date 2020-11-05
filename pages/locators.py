locatorArray = []

chapter_number_re = '((?:\d){1,3}\s?-?\s?(?:\d){1,4})'
chapter_normalize_re = r"\t|(\s\s)|\n"


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

locatorsArray = [ReadManga, MintManga, MangaChan, ManhwaTop]


def get_locator(url):
    for locator in locatorsArray:
        if url.__contains__(locator.url_container):
            return locator
