<img width="453" alt="image" src="https://github.com/ikuoikuo/scrapy_line_bot/assets/92318768/a4bfcf46-e393-49f8-81df-6bcbec87b52b">


## Usage
1. プロジェクトのダウンロード

```bash
git clone https://github.com/ikuoikuo/scrapy_line_bot.git
```

2. コンテナの立ち上げ
```bash
cd scrapy_line_bot
docker compose up -d
```

3. コンテナの中に入る
```bash
docker compose exec app /bin/bash
```

4. .envとusers.csvの準備

app直下にLINEのアクセストークン等を記した.envを配置
```
CHANNEL_ACCESS_TOKEN = hoge
CHANNEL_SECRET = hogehoge
```

aidb_scrapy直下に送信対象ユーザーを記したusers.csvを配置
```
hoge
hogehoge
```

5. APIサーバーの起動
```bash
cd /app/libs
python line_bot.py
```

6. scrapy-do でのスクレイピングスケジュール設定

scrapy-doの起動
```bash
scrapy-do -n scrapy-do
```

プロジェクトのプッシュ
```bash
cd aidb_scrapy
scrapy-do-cl push-project
```

（実行テスト）
```bash
scrapy-do-cl schedule-job --project aidb_scrapy  \
    --spider aidb --when now
```
（定期実行）
```bash
scrapy-do-cl schedule-job --project aidb_scrapy --spider aidb --when 'every day at 06:30'
```
