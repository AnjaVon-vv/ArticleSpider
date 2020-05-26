# -*- coding: utf-8 -*-
__author__ = 'Von'

from urllib import parse

import scrapy
from scrapy.http import Request


class XueshuSpider(scrapy.Spider):
    name = 'xueShu'
    allowed_domains = ['xueshu.baidu.com']
    start_urls = ['https://xueshu.baidu.com/s?wd=information+security']

    def parse(self, response):
        #获取文章具体url并交给解析函数
        post_urls = response.css(".t.c_font a::attr(href)").extract()
        for post_url in post_urls:
            yield Request(url=parse.urljoin(response.url, post_url), callback=self.parse_detail)

        #获取下一页url进行下载后交给parse
        next_url = response.css("a.n::attr(href)").extract_first("")
        if next_url:
            yield Request(url=parse.urljoin(response.url, next_url), callback=self.parse)


    def parse_detail(self, response):
        #提取文章具体字段
        #标题、第一作者、关键词、摘要、发表年份、文章链接
        #被引量、阅读量、收藏量
        title = response.css(".main-info h3 a::text").extract_first().strip()
        firstAuthor = response.css(".author_text span a::text").extract_first("Unknown")
        keywords = response.css(".kw_main span a::text").extract() #不一定存在、不定长数组
        abstract = response.css(".abstract::text").extract_first()
        year = response.css(".year_wr .kw_main::text").extract_first("Unknown").strip()
        refNum = int(response.css(".ref-wr-num a::text").extract_first("0").strip())
        readNum = int(response.css(".label-r p:nth-child(2)::text").extract_first("0"))
        starNum = int(response.css(".like-amount-num::text").extract_first("0"))
        articleLink = response.css(".dl_item::attr(href)").extract() #不定长数组

        pass
