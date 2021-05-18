import pyrebase

# функция исправляет баг который возвращает строку в неправильном формате
def noquote(s):
    return s


class FireBaser:

    def __init__(self, firebase_config):
        """Подключаемся к БД и сохраняем курсор соединения"""
        self.firebase = pyrebase.initialize_app(firebase_config)
        self.db = self.firebase.database()
        pyrebase.pyrebase.quote = noquote

    def add_manga(self, user_id, url,
                  last_chapter='0',
                  name='Без имени'):
        """Создаем запись и пушим ее в БД"""
        data = {
            'user_id': user_id,
            'url': url,
            'last_chapter': last_chapter,
            'name': name
        }
        self.db.child('Manga').push(data)

    def get_manga(self, user_id):
        """Подключаемся к БД и находим мангу юзера"""
        manga_list = self.db.child("Manga").order_by_child('user_id').equal_to(user_id).get()
        buf = []
        for manga in manga_list.each():
            manga_with_id = manga.val()
            manga_with_id['id'] = manga.key()
            buf.append(manga_with_id)
        sorted_list = sorted(buf, key=lambda k: k['name'])
        return sorted_list

    # todo оптимизировать под обновление списком
    def update_manga(self, user_id, id, last_chapter):
        """Обновляем мангу пользователя"""
        self.db.child('Manga').child(id).update({
            'last_chapter': last_chapter
        })

    def delete_manga(self, user_id, id):
        """Удаляем мангу"""
        self.db.child("Manga").child(id).remove()

    # todo научиться вытаскивать мангу по двум параметрам сразу в запросе
    def is_user_have_manga_by_url(self, user_id, url):
        """Проверяем наличие манги у пользователя"""
        manga = self.db.child("Manga").order_by_child('url').equal_to(url).get()
        for m in manga.each():
            if m.val()['user_id'] == user_id:
                return True
        return False

    def get_manga_by_id(self, user_id, id):
        """Проверяем наличие манги у пользователя"""
        manga = self.db.child("Manga").child(id).get()
        return manga.val()
