import sys
sys.path.append("../../")
import redis
import json
import re
from scrapy import Spider
from lxml import etree
from scrapy.crawler import CrawlerProcess
from scrapy.selector import Selector
from scrapy.http import Request
from scrapy.utils.project import get_project_settings
from scrapy_redis.spiders import RedisSpider
from newsSpider.items import NewInformationItem_xinhua
from datetime import datetime


""""如果一个关键词相关的新闻总数超过10000，则只能查询前10000条数据。目前最多只能查询以时间为顺序的前10000条数据"""
class Xinhua_News_Info_Spider(RedisSpider):
    name = "xinhua_news_info_spider"
    redis_key = "xinhua_news_search_spider:start_urls"

    def __init__(self, *args, **kwargs):
        super(Xinhua_News_Info_Spider, self).__init__(*args, **kwargs)

    """ 解析响应 """
    def parse(self, response):
        text = "".join([response.text.strip().rsplit("}", 1)[0], "}"])
        data = json.loads(text)
        for item in data['content']['results']:
            new_information = NewInformationItem_xinhua()   #每一个item都是一条新闻的信息           
            new_information['title'] = re.sub("<font color=red>|</font>|&nbsp|&quo|&amp", "", item['title'])            #&nbsp这些是HTML转义字符
            new_information['url'] = item['url']
            new_information['author'] = item['sitename']
            new_information['create_time'] = item['pubtime']
            new_information['origin'] = "新华网"
            dt = datetime.now()
            new_information['crawl_time'] = dt.strftime('%Y-%m-%d %H:%M:%S')
            if item['keyword'] is None:
                new_information['keyword'] = " "
            else:
                new_information['keyword'] = re.sub("<font color=red>|</font>", "", item['keyword'])
            yield Request(new_information['url'], callback=self.parse_content, dont_filter=True, meta={'new_item': new_information})

    def parse_content(self, response):
        new_item = response.meta['new_item']
        selector = Selector(response)
        """每个网页的内容有不同的id或class"""
        """每个网页的结构不相同，无法将所有的网页爬取到"""
        article = selector.xpath('//p//text()').extract()
        new_item['article'] = '\n'.join(article) if article else ''
        if article is None or str(article).strip() == "":         #str(article).strip():是把article的头和尾的空格，以及位于头尾的\n \t之类给删掉。
            print(response.url)
        else:
            yield new_item


if __name__ == "__main__":
    conn = redis.Redis(host="xx.xx.xx.xx", port=6379, password="root")
    print("url数量:" + str(conn.llen('xinhua_news_search_spider:start_urls')))

    process = CrawlerProcess(get_project_settings())
    process.crawl('xinhua_news_info_spider')
    process.start()
