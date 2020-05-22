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
    abstract = scrapy.Field()
    time = scrapy.Field()
    content = scrapy.Field()
    url = scrapy.Field()
    urlID = scrapy.Field()