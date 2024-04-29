# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import datetime
import os
import sqlite3


class AidbScrapyPipeline(object):
    _db = None

    @classmethod
    def get_database(cls):
        cls._db = sqlite3.connect(
            os.path.join(os.getcwd(), 'aidb.db'))

        # テーブル作成
        cursor = cls._db.cursor()
        cursor.execute(
            'CREATE TABLE IF NOT EXISTS post(\
                id INTEGER PRIMARY KEY AUTOINCREMENT, \
                url TEXT UNIQUE NOT NULL, \
                title TEXT NOT NULL, \
                date DATE NOT NULL \
            );')

        return cls._db

    def process_item(self, item, spider):
        """
        Pipeline にデータが渡される時に実行される
        item に spider から渡された item がセットされる
        """
        self.save_post(item)
        return item

    def save_post(self, item):
        """
        item を DB に保存する
        """
        if self.find_post(item['url']):
            # 既に同じURLのデータが存在する場合はスキップ
            return

        db = self.get_database()
        db.execute(
            'INSERT INTO post (title, url, date) VALUES (?, ?, ?)', (
                item['title'],
                item['url'],
                datetime.datetime.strptime(item['date'], '%B %d, %Y')
            )
        )
        db.commit()

    def find_post(self, url):
        db = self.get_database()
        cursor = db.execute(
            'SELECT * FROM post WHERE url=?',
            (url,)
        )
        return cursor.fetchone()
