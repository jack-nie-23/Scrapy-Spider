#!/usr/bin/env python
# encoding: utf-8
import sys
sys.path.append("../../")
import redis
import json
from scrapy import Spider
from scrapy.crawler import CrawlerProcess
from scrapy.http import Request
from scrapy.utils.project import get_project_settings



class XinhuaNewsSearchSpider(Spider):
    name = "xinhua_news_search_spider"
    conn = redis.Redis(host="xx.xx.xx.xx", port=6379, password="root")

    xinhua_news_url = "http://www.xinhuanet.com/"

    def __init__(self, keywords=None, *args, **kwargs):
        super(XinhuaNewsSearchSpider, self).__init__(*args, **kwargs)
        self.keywords = keywords

    def start_requests(self):
        keys = self.keywords.split("、")

        for key in keys:
            xinhua_search_url = "http://so.news.cn/getNews?keyword=%s&curPage=1&sortField=0&searchFields=0&lang=cn" % key
            yield Request(xinhua_search_url, callback=self.xinhua_parse)

    def xinhua_parse(self, response):
        data = json.loads(response.text)
        attr = response.url.split("curPage=1")
        pageCount = int(data['content']['pageCount'])       #获得当前的总页数
        print("总页数：", pageCount)
        for page in range(1, pageCount + 1):                #将所有页码对应的页面的url提取出来并保存
            url = attr[0] + "curPage=" + str(page) + "&sortField=0&searchFields=0&lang=cn"
            self.conn.lpush("xinhua_news_search_spider:start_urls", url)

if __name__ == "__main__":
    keys = '应急'

    process = CrawlerProcess(get_project_settings())
    process.crawl('xinhua_news_search_spider', keywords=keys)
    process.start()

    print("xinhua-search执行完毕")
