#!/usr/bin/env python
# encoding: utf-8
# 单机爬虫
import sys
sys.path.append("../../")
import json
import time
import scrapy
import re
import random
from scrapy import Spider
from scrapy.crawler import CrawlerProcess
from scrapy.http import Request
from scrapy.utils.project import get_project_settings
from newsSpider.items import NewInformationItem_people
from datetime import datetime
from bs4 import BeautifulSoup   # 解析HTML文本


class PeopleNewsSpider(Spider):
    name = "people_news_spider"
    people_news_url = "http://www.people.com.cn/"
    start_urls = 'http://search.people.cn/search-platform/front/search'

    def __init__(self, keywords=None, *args, **kwargs):
        super(PeopleNewsSpider, self).__init__(*args, **kwargs)
        self.keywords = keywords
        self.key = ' '

    def start_requests(self):
        keys = self.keywords.split("、")
        for self.key in keys:
            time_ns = int(round(time.time() * 1000))
            headers={"Accept": "application/json, text/plain, */*",
                    "Content-Type": "application/json",
                    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.64 Safari/537.36 Edg/101.0.1210.53",
                    "Referer": "http://search.people.cn/s/?keyword="+self.key+"&st=0&_="+str(time_ns)
                    }
            data = {"endTime": "0",
                    "hasContent": "True",
                    "hasTitle": "True",
                    "isFuzzy": "True",
                    "key": self.key,
                    "limit": "10",
                    "page": "1",
                    "sortType": "2",
                    "startTime": "0",
                    "type": "0"}
            temp=json.dumps(data)
            yield scrapy.Request(self.start_urls,method='POST',body=temp,headers=headers,callback=self.people_parse, meta={'time_ns': time_ns})

    def people_parse(self, response):
        data_news = json.loads(response.text)
        print("总共页数 :", data_news['data']['pages'])
        print("当前页 :", data_news['data']['current'])
        time_ns = response.meta['time_ns']
        key_value = self.key

        page_flag = 1
        while True:
            if page_flag < data_news['data']['pages']:
                page_flag = page_flag + 1
                # 1000页以后的数据无法获取，1000页以后的数据都是第一页数据的内容
                if page_flag > 1000:
                    break
                headers={"Accept": "application/json, text/plain, */*",
                        "Content-Type": "application/json",
                        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.64 Safari/537.36 Edg/101.0.1210.53",
                        "Referer": "http://search.people.cn/s/?keyword="+key_value+"&st=0&_="+str(time_ns)
                        }
                data = {"endTime": "0",
                        "hasContent": "True",
                        "hasTitle": "True",
                        "isFuzzy": "True",
                        "key": key_value,
                        "limit": "10",
                        "page": page_flag,
                        "sortType": "2",
                        "startTime": "0",
                        "type": "0"}
                temp=json.dumps(data)
                time.sleep(0.1)
                if page_flag % 100 == 0:
                    time.sleep(random.randint(1,10))
                yield scrapy.Request(self.start_urls,method='POST',body=temp,headers=headers,callback=self.people_parse_content, meta={'key_value': key_value})
            else:
                break

    def people_parse_content(self, response):
        key_value = response.meta['key_value']
        data_news = json.loads(response.text)
        records = data_news['data']['records']
        for item in records:
            new_information = NewInformationItem_people()   #每一个item都是一条新闻的信息
            new_information['title'] = re.sub("<em>|</em>|&nbsp|&quo|&amp", "", item['title'])            #&nbsp这些是HTML转义字符
            new_information['url'] = item['url']
            new_information['author'] = item['author']
            new_information['create_time'] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(item["displayTime"]/1000))
            new_information['origin'] = "人民网"
            new_information['point'] = key_value
            new_information['keyword'] = re.sub("<em>|</em>|&nbsp|&quo|&amp", "", item['keyword'])
            dt = datetime.now()
            new_information['crawl_time'] = dt.strftime('%Y-%m-%d %H:%M:%S')
            new_information['article'] = BeautifulSoup(item["content"], "html.parser").text
            new_information['category'] = re.sub("#|&nbsp|&quo|&amp", "", item["belongsName"])
            yield new_information           # 提交到item通道进行持久化


if __name__ == "__main__":
    keywords = '应急'

    process = CrawlerProcess(get_project_settings())
    process.crawl('people_news_spider', keywords=keywords)
    process.start()

    print("peoplenews-search执行完毕")
