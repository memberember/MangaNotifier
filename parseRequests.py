from pages.mangaPage import MangaPage


def get_manga(url):

    try:
        page = MangaPage(url)
        page.open()

        return {'manga_name': page.get_name(),
                'last_chapter': page.get_last_chapter()
                }

    except Exception as e:
        print(f'Exception to: {url}')
        print(e)
        return 0


# получить данные по манге (при добавлении)
def get_manga_for_url_list(url_list):
    information = []
    for url in url_list:
        manga = get_manga(url)
        if manga != 0:
            information.append(manga)
    return information


# функция получения последней главы по манге
def get_manga_list_last_chapters(manga_list):
    # создаем пустой массив обновлений
    updates = []

    for current in manga_list:
        from_site = get_manga(current['url'])

        # если манга приходит с нормальным ответом
        if from_site != 0:

            # если последняя глава манги
            if current['last_chapter'] != from_site['last_chapter']:
                updates.append({
                    'manga_name': from_site['manga_name'],
                    'last_chapter': from_site['last_chapter'],
                    'id': current['id'],
                    'url': current['url'],
                    'prev_chapter': current['last_chapter']
                }
                )
    return updates


def get_manga_updates_turbo(current):
    from_site = get_manga(current['url'])

    # если манга приходит с нормальным ответом
    if from_site != 0:

        # если последняя глава манги
        if current['last_chapter'] != from_site['last_chapter']:
            return {
                'manga_name': from_site['manga_name'],
                'last_chapter': from_site['last_chapter'],
                'id': current['id'],
                'url': current['url'],
                'prev_chapter': current['last_chapter']
            }
    return 0
