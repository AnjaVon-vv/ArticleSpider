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

class tgbusArticleItem(scrapy.Item):
    title = scrapy.Field()
    author = scrapy.Field()
    keywords = scrapy.Field()
    abstract = scrapy.Field()
    pubTime = scrapy.Field()
    content = scrapy.Field()
    url = scrapy.Field()
    urlID = scrapy.Field()

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