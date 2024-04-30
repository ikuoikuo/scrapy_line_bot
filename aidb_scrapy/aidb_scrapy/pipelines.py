# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import os
import sqlite3
import requests

class AidbScrapyPipeline(object):
    try:
        _db = sqlite3.connect(os.path.join('/app/aidb_scrapy', 'aidb.db'))
    except:
        _db = None

    @classmethod
    def get_database(cls):
        if cls._db is None:  # データベース接続が未定義の場合にのみ接続
            db_path = os.path.join('/app/aidb_scrapy', 'aidb.db')
            cls._db = sqlite3.connect(db_path)
            cls._initialize_db()

        return cls._db

    @classmethod
    def _initialize_db(cls):
        """データベースの初期化とテーブルの作成を行う"""
        cursor = cls._db.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS post(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                url TEXT UNIQUE NOT NULL,
                title TEXT NOT NULL,
                date TEXT NOT NULL
            );
        ''')
        cls._db.commit()

    def process_item(self, item, spider):
        """
        Pipeline にデータが渡される時に実行される
        item に spider から渡された item がセットされる
        """
        self.save_post(item)
        return item

    def call_send_message(self,message_text):
        """
        DBに追加する場合はLINEに内容を追加する。
        """
        url = 'http://localhost:9999/send_message'
        params = {'message': message_text}
        try:
            response = requests.get(url, params=params)
            print(f'Status Code: {response.status_code}')
            print(f'Response Body: {response.text}')
        except requests.exceptions.RequestException as e:
            print(f'An error occurred: {e}')

    def save_post(self, item):
        """
        item を DB に保存する
        """
        if self.post_exists(item['url']):
            # 既に同じURLのデータが存在する場合はスキップ
            return
        db = self.get_database()
        db.execute(
            'INSERT INTO post (title, url, date) VALUES (?, ?, ?)', (
                item['title'],
                item['url'],
                item['date']
            )
        )
        db.commit()
        message_text = (
            f"おはよう。筋トレ行く前にこれ読めって。\n"
            f"理解できないと厳しいって。\n"
            
            "-------------------------------\n"
            f"日付：{item['date']}\n"
            f"タイトル：\n{item['title']}\n"
            f"URL：{item['url']}\n"
            "-------------------------------"
        )
        self.call_send_message(message_text)

    def post_exists(self, url):
        db = self.get_database()
        cursor = db.execute(
            'SELECT * FROM post WHERE url=?',
            (url,)
        )
        return cursor.fetchone() is not None
    