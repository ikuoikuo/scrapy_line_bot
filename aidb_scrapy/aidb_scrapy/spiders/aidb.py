import scrapy
from aidb_scrapy.items import Post

class AidbSpider(scrapy.Spider):
    name = "aidb"
    allowed_domains = ["ai-data-base.com"]
    start_urls = ["https://ai-data-base.com/"]

    def parse(self, response):
        """
        レスポンスに対するパース処理
        """
        # response.css で scrapy デフォルトの css セレクタを利用できる
        for post in response.css('#post_list1 .post_item'):
            # items に定義した Post のオブジェクトを生成して次の処理へ渡す
            yield Post(
                url=post.css('div.post_info h3.title a::attr(href)').extract_first().strip(),
                title=post.css('div.post_info h3.title a::text').extract_first().strip(),
                date=post.css('li.post_date time::text').extract_first().strip(),
            )
