# -*- coding: utf-8 -*-
__author__ = "Von"

import scrapy
from scrapy.http import Request
from urllib import parse


pn = 2
class TgbusSpider(scrapy.Spider):
    name = 'tgbus'
    allowed_domains = ['https://www.tgbus.com']
    start_urls = ['https://tech.tgbus.com/news/124761']

    def parse(self, response):

        # fpImage ＝
        # 标题
        title = response.css("h1 span::text")
        if title:
            title = title.extract_first()
        else:
            title = response.css("div.title::text").extract_first()
        # 作者、发布时间
        info = response.css(".article-main__sourceInfo h5")
        if info:
            info = info
        else:
            info = response.css(".info-box")
        author = info.css(":nth-child(4)::text").extract_first("Unknown")
        time = info.css("i::text").extract_first("Unknown")
        # 摘要
        abstract = response.css(".description div::text")
        if abstract:
            abstract = abstract.extract_first()
        else:
            abstract = response.css(".summary::text").extract_first()
        # 正文数组
        content = response.css(".article-main-contentraw p::text").extract() #不定长数组
        # 收藏数 int
        starNum = int(response.css(".article-collection__collectionNumber::text").extract_first("Unknown"))



        pass
