# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
# -*- coding: utf-8 -*-
"""定义了item Pipeline(项目管道)的实现 -->清洗存储数据"""
from pymongo.errors import DuplicateKeyError
from newsSpider.items import NewInformationItem_xinhua, NewInformationItem_people,NewInformationItem
from newsSpider.settings import MYSQL_HOST, MYSQL_DBNAME, MYSQL_USER, MYSQL_PASSWD, MYSQL_PORT
import pymysql      #python3.x中用于连接mysql的库
import copy

class MysqlPipeline(object):
    def __init__(self):
        self.connect = pymysql.connect(
            host=MYSQL_HOST,
            db=MYSQL_DBNAME,
            user=MYSQL_USER,
            passwd=MYSQL_PASSWD,
            charset='utf8',
            use_unicode=True)
        self.cursor = self.connect.cursor()  #cursor用来执行命令

    def process_item(self, item, spider):
        """ 判断item的类型（item是否是定义的数据结构类型），并作相应的处理，再入数据库 """
        asynItem = copy.deepcopy(item)    #需要导入import copy
        if isinstance(asynItem, NewInformationItem_xinhua):
            self.insert_NewInformationItem(asynItem)
        elif isinstance(asynItem, NewInformationItem_people):
            self.insert_NewInformationItem_people(asynItem)
        elif isinstance(asynItem, NewInformationItem):
            self.insert_NewInformationItem(asynItem)
        return asynItem

    def insert_NewInformationItem(self, item):
        try:
            sql_str = "insert into news_information_xinhua(author,url,title,keyword,point, origin,article,create_time,crawl_time) value ('%s','%s','%s','%s','%s','%s','%s','%s','%s')" % (
                item['author'], item['url'], item['title'], item['keyword'],item['point'], item['origin'],
                item['article'], item['create_time'], item['crawl_time'])
            self.cursor.execute(sql_str)
            self.connect.commit()       #提交事务
            print("插入数据成功")
        except Exception as error:
            print("插入数据错误")
            print(error)
            print(item)
        return item

    def insert_NewInformationItem_people(self, item):
        try:
            sql_str = "insert into news_information_people(author,url,title,keyword,point,origin,article,create_time,crawl_time) value ('%s','%s','%s','%s','%s','%s','%s','%s','%s')" % (
                item['author'], item['url'], item['title'], item['keyword'],item['point'], item['origin'],
                item['article'], item['create_time'], item['crawl_time'])
            self.cursor.execute(sql_str)
            self.connect.commit()       #提交事务
            print("插入数据成功")
        except Exception as error:
            print("插入数据错误")
            print(error)
            print(item)
        return item
    # @staticmethod
    # def insert_item(collection, item):
    #     try:
    #         collection.insert(dict(item))
    #     except DuplicateKeyError:
    #         """
    #         说明有重复数据
    #         """
    #         pass
