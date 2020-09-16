import parseRequests as PR

def bugWihMoreMangas():
    manga_list = [{
        'id': '12',
        'manga_name': 'Герой? Я давно перестал им быть',
        'last_chapter': '1 - 103',
        'site_type': 'readmanga',
        'url': 'http://readmanga.me/hero__i_quit_a_long_time_ago'
    }]
    print(PR.get_manga_chapters(manga_list))
    # todo перестроить логику поиска новых глав
    """ Можно сделать так, чтобы выводилась информация о том какая глава читалась последней
    и какая глава сейчас последняя, затем кидать ссылку на последнюю +1"""