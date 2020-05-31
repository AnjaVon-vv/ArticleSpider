# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy

class ArticlespiderItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass



from ArticleSpider.spiders.models.esTypes import tgbusType
from elasticsearch_dsl import connections
es = connections.create_connection(tgbusType._doc_type.using)
# .virtualenvs/aricle/lib/python3.7/site-packages/elasticsearch/connection/http_urllib3.py
# host:'192.168.1.106'
def gen_sugg(index, info_tuple):
    # 根据字符串生成搜索建议数组
    usedWds = set()  # 用于去重，以先到的权重为准
    suggestion = []
    for txt, weight in info_tuple:
        if txt:
            # 调用ES analyze接口分析字符串
            wds = es.indices.analyze(index=index, body={'text':txt, 'analyzer':"ik_max_word"}, params={'filter': ["lowercase"]})
            analyWds = set([r["token"] for r in wds["tokens"] if len(r["token"]) > 1])  # 过滤单字
            newWds = analyWds - usedWds
        else:
            newWds = set()
        if newWds:
            suggestion.append({"input": list(newWds), "weight": weight})
    return suggestion

# from w3lib.html import remove_tags
# remove_tags() 去除html标签
import redis
# redisClient = redis.StrictRedis()
redisClient = redis.StrictRedis(host='192.168.1.106')

class tgbusArticleItem(scrapy.Item):
    title = scrapy.Field()
    author = scrapy.Field()
    keywords = scrapy.Field()
    abstract = scrapy.Field()
    pubTime = scrapy.Field()
    content = scrapy.Field()
    url = scrapy.Field()
    urlID = scrapy.Field()
    relate = scrapy.Field()
    PR = scrapy.Field()
    # 存为es的type
    def save_to_es(self):
        article = tgbusType()
        article.title = self['title']
        article.author = self['author']
        article.keywords = self['keywords']
        article.abstract = self['abstract']
        article.pubTime = self['pubTime']
        article.content = self['content']
        article.meta.id = self['urlID']
        article.url = self['url']
        article.relate = self["relate"]
        article.PR = self["PR"]
        # article.urls.relate = self["relate"]
        # article.urls.io = self['url']

        article.suggestion = gen_sugg(tgbusType._doc_type.index, ((article.title, 7), (article.abstract, 3), (article.keywords, 3)))

        article.save()

        redisClient.incr("tgbusCnt")

        return


# 通过Itemloader加载item
# def add_tgbus(value):
#     return value + " - tgbus"
# from scrapy.loader.processors import MapCompose, TakeFirst
# class tgbusArticleItem(scrapy.Item):
#     title = scrapy.Field(
#         # 通过定义函数，实现对传入的值进行预处理
#         input_processor = MapCompose(add_tgbus), # 将title作为value传入add_tgbus函数
#         output_processor = TakeFirst() # 只取数组的第一个值
#     )

# 为简化操作，可自定义itemLoader
# from scrapy.loader import ItemLoader
# class ArticleItemLoader(ItemLoader):
#     default_output_processor = TakeFirst()