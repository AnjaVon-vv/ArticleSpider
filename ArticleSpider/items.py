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

class ArticleItem(scrapy.Item):
    title = scrapy.Field()
    firstAuthor = scrapy.Field()
    keywords = scrapy.Field()
    abstract = scrapy.Field()
    year = scrapy.Field()
    refNum = scrapy.Field()
    readNum = scrapy.Field()
    starNum = scrapy.Field()
    articleLink = scrapy.Field()