
"""Регулярки"""
chapter_number_re = '((?:\d){1,3}\s-\s(?:\d){1,4})'
chapter_date_re = '((?:\d){1,4}[-.](?:\d){2}[-.](?:\d){2})'

"""XPATH"""
readmanga_last_chapter_xpath = '//*[@id="mangaBox"]/div[2]/div[1]/div[1]/div[*]/h4/a'
readmanga_last_manga_url_xpath = '/html/body/div[4]/div[2]/div[*]/table/tbody/tr[1]/td[1]/a'
readmanga_name_xpath = '//*[@id="mangaBox"]/div[2]/h1/span'
readmanga_chapter_xpath = '//*[@id="mangaBox"]/div[2]/div[*]/table/tbody/tr[*]'
readmanga_date_xpath = '//*[@id="mangaBox"]/div[2]/div[*]/table/tbody/tr[*]/td[2]'

mangachan_last_chapter_xpath = '//*[@id="tc_1"]/tbody/tr[3]/td[1]/div/a'
mangachan_last_manga_url_xpath = '//tbody/tr[*]/td[1]/div/a'
mangachan_name_xpath = '//*[@id="info_wrap"]/div/div/h1/a'
mangachan_chapter_xpath = '//*[@id="tc_1"]/tbody/tr[*]/td[1]/div/a/../../..'
mangachan_date_xpath = '//*[@id="tc_1"]/tbody/tr[*]/td[2]/div'

Readmanga = {
    'chapter_cutter_re': chapter_number_re,
    'last_chapter_xpath': readmanga_last_chapter_xpath,
    'last_manga_url_xpath': readmanga_last_manga_url_xpath,
    'name_xpath': readmanga_name_xpath,
    'chapter_xpath': readmanga_chapter_xpath,
    'date_xpath': readmanga_date_xpath

}

Mangachan = {
    'chapter_cutter_re': chapter_number_re,
    'last_chapter_xpath': mangachan_last_chapter_xpath,
    'last_manga_url_xpath': mangachan_last_manga_url_xpath,
    'name_xpath': mangachan_name_xpath,
    'chapter_xpath': mangachan_chapter_xpath,
    'date_xpath': mangachan_date_xpath
}
