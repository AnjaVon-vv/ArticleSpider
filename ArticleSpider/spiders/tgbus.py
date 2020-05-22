# -*- coding: utf-8 -*-
__author__ = "Von"

import scrapy
from scrapy.http import Request
# from urllib import parse

from ArticleSpider.items import  tgbusArticleItem
from ArticleSpider.utils.common import get_md5

pn = 2
class TgbusSpider(scrapy.Spider):
    name = 'tgbus'
    # allowed_domains = ['https://www.tgbus.com']
    start_urls = ['https://www.tgbus.com/list/all/']

    def parse(self, response):
        # 获取文章具体url并交给解析函数
        post_urls = response.css(".information-item__link::attr(href)").extract()
        for post_url in post_urls:
            # image_url = post_url.css("::attr(src)").extract_first("")
            # yield Request(url=parse.urljoin(response.url, post_url), meta={"image_url":image_url}, callback=self.parseDetail)
            yield Request(url=post_url, callback=self.parseDetail)

        # 获取下一页url进行下载后交给parse
        global pn
        spn = str(pn)
        next_url = 'https://www.tgbus.com/list/all/' + spn
        if pn >= 5:
            self.crawler.engine.close_spider(self, "无有效信息，关闭spider")
        else:
            pn = pn + 1
            yield Request(url=next_url, callback=self.parse)

    def parseDetail(self, response):
        # fpImage ＝ response.meta.get("url", "")

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
        # 实例化Item
        tgArticleItem = tgbusArticleItem()
        tgArticleItem["title"] = title
        tgArticleItem["author"] = author
        tgArticleItem["time"] = time
        tgArticleItem["abstract"] = abstract
        tgArticleItem["content"] = content
        tgArticleItem["url"] = response.url
        tgArticleItem["urlID"] = get_md5(response.url)
        yield tgArticleItem #settings

        pass