# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html
"""定义item的数据结构（爬取结果的数据结构）"""
"""Field:字段"""
from scrapy import Item, Field

class NewInformationItem(Item):
    """ 新华网及其它新闻信息 """
    id = Field()
    author = Field()  # 作者
    url = Field()  # url
    title = Field()  # 标题
    keyword = Field()   # 关键字
    point = Field()   # search 指针
    article = Field()  # 内容
    create_time = Field()  # 发布时间
    crawl_time = Field()  # 抓取时间戳
    origin = Field()  # 来源的网站
    is_delete = Field()  # 是否删除

class NewInformationItem_xinhua(Item):
    """ 新华网新闻信息 """
    id = Field()
    author = Field()  # 作者
    url = Field()  # url
    title = Field()  # 标题
    keyword = Field()   # 关键字
    point = Field()   # search 指针
    article = Field()  # 内容
    create_time = Field()  # 发布时间
    crawl_time = Field()  # 抓取时间戳
    origin = Field()  # 来源的网站
    is_delete = Field()  # 是否删除

class NewInformationItem_people(Item):
    """ 人民网新闻信息 """
    id = Field()
    author = Field()  # 作者
    url = Field()  # url
    title = Field()  # 标题
    keyword = Field()   # 关键字
    point = Field()   # search 指针
    article = Field()  # 内容
    create_time = Field()  # 发布时间
    crawl_time = Field()  # 抓取时间戳
    origin = Field()  # 来源的网站
    is_delete = Field()  # 是否删除

