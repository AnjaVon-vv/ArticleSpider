# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


class ArticlespiderPipeline:
    def process_item(self, item, spider):
        return item

import codecs
import json
# 自定义导出为json文件、配置settings
class JsonWithEncodingPipeline(object):
    def __init__(self):
        self.file = codecs.open('article.json', 'w', encoding="utf-8")
    def process_item(self, item, spider):
        lines = json.dumps(dict(item), ensure_ascii=False) + "\n"
        self.file.write(lines)
        return item
    def spider_closed(self, spider):
        self.file.close()

#  # scraoy定义的json exporter导出为json文件
# from scrapy.exporters import JsonItemExporter
# class JsonExporterPipeline(object):
#     def __init__(self):
#         self.file = open('articleExport.json', 'wb')
#         self.exporter = JsonItemExporter(self.file, encoding="utf-8", ensure_ascii=False)
#         self.exporter.start_exporting()
#     def close_spider(self, spider):
#         self.exporter.finish_exporting()
#         self.file.close()
#     def process_item(self, item, spider):
#         self.exporter.export_item(item)
#         return item



import MySQLdb
import MySQLdb.cursors
# # 采用同步机制写入数据库
# class MysqlPipeline(object):
#     def __init__(self):
#         self.conn = MySQLdb.connect('192.168.1.107', 'root', 'AnjaVon9170', 'Spider', charset='utf8', use_unicode=True)
#         self.cursor = self.conn.cursor()
#     def process_item(self, item, spider):
#         insert_sql = """
#                     insert into tgbus
#                     VALUE (%s, %s, %s, %s, %s, %s, %s)
#                 """
#         self.cursor.execute(insert_sql, (item["urlID"], item["title"], item["author"], item["pubTime"], item["abstract"], item["content"], item["url"])) # 同步
#         self.conn.commit()

# 异步化mysql插入与爬取
from twisted.enterprise import adbapi
class MysqlTwistedPipeline(object):
    def __init__(self, dbpool):
        self.dbpool = dbpool
    # 引入settings.py文件的内容
    @classmethod
    def from_settings(cls, settings):
        # settings！！！不然会报错
        # TypeError: __init__() missing 1 required positional argument: 'dbpool'
        dbparms = dict(
            host=settings["MYSQL_HOST"],
            user = settings["MYSQL_USER"],
            passwd = settings["MYSQL_PASSWORD"],
            db = settings["MYSQL_DBNAME"],
            charset = 'utf8',
            cursorclass = MySQLdb.cursors.DictCursor,
            use_unicode = True
        )
        dbpool = adbapi.ConnectionPool("MySQLdb", **dbparms)
        return cls(dbpool)

    def process_item(self, item, spider):
        # 使用twisted实现
        query = self.dbpool.runInteraction(self.do_insert, item)
        # 需要额外的错误处理
        query.addErrback(self.handle_error)
    def handle_error(self, failure):
        # 异步插入异常处理
        print('数据库插入失败了呜呜，原因是：' )
        print(failure)
    def do_insert(self, cursor, item):
        # 执行具体插入
        # 注意content插入可能出错 1241
        insert_sql = """
            insert into tgbus(urlID, title, author, keywords, pubTime, abstract, content, url)
            VALUE (%s, %s, %s, %s, %s, %s, %s, %s)
        """
        cursor.execute(insert_sql, (item["urlID"], item["title"], item["author"], item["keywords"], item["pubTime"], item["abstract"], item["content"], item["url"]))



# 自定义pipeline下载图片并保存图片路径
# from scrapy.pipelines.images import ImagesPipeline
# class articleImagePipeline(ImagesPipeline):
#     def item_completed(self, results, item, info):
#         for ok, value in results:
#             imageFilePath = value["path"]
#         item["imagePath"] = imageFilePath
#         return item
