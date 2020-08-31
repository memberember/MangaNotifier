import sqlite3
import time


class SQLighter:

    def __init__(self, database):
        """Подключаемся к БД и сохраняем курсор соединения"""
        self.connection = sqlite3.connect(database)
        self.cursor = self.connection.cursor()

    def add_manga(self, user_id, url,
                  last_chapter='0',
                  name='Без имени',
                  site_type='UK'):
        """Добавляем новую мангу"""
        with self.connection:
            return self.cursor.execute(
                "INSERT INTO `manga_title` (`user_id`,`url`, `last_chapter`,`name`,`site_type`) VALUES(?,?,?,?,?)",
                (user_id, url, last_chapter, name, site_type))

    def get_manga(self, user_id):
        """Проверяем мангу пользователя"""
        with self.connection:
            result = self.cursor.execute("SELECT * FROM `manga_title` WHERE `user_id` = ?", (user_id,)).fetchall()
            return result

    def update_manga(self, user_id, id, last_chapter):
        """Обновляем статус подписки пользователя"""
        with self.connection:
            return self.cursor.execute(
                "UPDATE `manga_title` SET `last_chapter` = ? WHERE (`user_id` = ?) AND (`id` = ?)",
                (last_chapter, user_id, id))

    def delete_manga(self, user_id, id):
        """Удаляем мангу"""
        with self.connection:
            return self.cursor.execute("DELETE FROM `manga_title` WHERE (`user_id` = ?) AND (`id` = ?)", (user_id, id))

    def is_user_have_manga_by_url(self, user_id, url):
        """Проверяем наличие манги у пользователя"""
        with self.connection:
            return bool(len(self.cursor.execute("SELECT * FROM `manga_title` WHERE (`user_id` = ?) AND (`url` = ?)",
                                                (user_id, url)).fetchall()))

    def is_user_have_manga_by_id(self, user_id, id):
        """Проверяем наличие манги у пользователя"""
        with self.connection:
            return bool(len(self.cursor.execute("SELECT * FROM `manga_title` WHERE (`user_id` = ?) AND (`id` = ?)",
                                                (user_id, id)).fetchall()))

    def close(self):
        """Закрываем соединение с БД"""
        self.connection.close()
