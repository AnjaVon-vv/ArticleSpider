# -*- coding: utf-8 -*-
__author__ = "Von"

# from urllib import parse
import datetime

import scrapy
from scrapy.http import Request

from ArticleSpider.items import tgbusArticleItem
from ArticleSpider.utils.common import get_md5

pn = 2
class TgbusSpider(scrapy.Spider):
    name = 'tgbus'
    # allowed_domains = ['https://www.tgbus.com', 'https://tech.tgbus.com']
    start_urls = ['https://www.tgbus.com/list/all/']
    # start_urls = ['https://www.tgbus.com/news/124939']  #游戏Test
    # start_urls = ['https://tech.tgbus.com/news/124955']  #科技Test

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
        if pn >= 501: # 爬500页
            print("爬取%s页！！！" % str(pn-1))
            self.crawler.engine.close_spider(self, "已是最后一页，关闭spider")
        else:
            pn = pn + 1
            yield Request(url=next_url, callback=self.parse)

    def parseDetail(self, response):
        # fpImage ＝ response.meta.get("url", "")

        # 标题
        title = response.css("h1 span::text")
        if title:
            title = title.extract_first()
            keywords = "游戏"
        else:
            title = response.css("div.title::text").extract_first()
            keywords = "科技"
        # 作者、发布日期和时间
        info = response.css(".article-main__sourceInfo h5")
        if info:
            info = info
        else:
            info = response.css(".info-box")
        author = info.css(":nth-child(4)::text").extract_first("Unknown")
        date_time = info.css("i::text").extract_first("Unknown").replace("  ", " ")
        # 摘要
        abstract = response.css(".description div::text")
        if abstract:
            abstract = abstract.extract_first("Noting in abstract!")
        else:
            abstract = response.css(".summary::text").extract_first("Noting in abstract!")
        # 正文数组
        content = response.css(".article-main-contentraw p::text").extract() #不定长数组
        content = ''.join(content) # 将爬取到的数组连接为字符串（避免插入数据库出错）
        # 相关新闻urlID
        relate = response.css(".tb-recommend-hot__lists li a::attr(href)")
        if relate:
            relate = relate.extract()
        else:
            relate = response.css(".special-card a::attr(href)").extract()
        relate = relate[:5]
        # 初始PR值，避免空值出现
        PR = 0.3



        # 实例化Item
        tgArticleItem = tgbusArticleItem()
        tgArticleItem["urlID"] = get_md5(response.url)
        tgArticleItem["title"] = title
        tgArticleItem["author"] = author
        tgArticleItem["keywords"] = keywords
        try:
            date_time = datetime.datetime.strptime(date_time, '%Y-%m-%d %H:%M') # 转为datetime类型
        except Exception as e:
            date_time = datetime.datetime.now()  # 出错改为当前时间
        tgArticleItem["pubTime"] = date_time
        tgArticleItem["abstract"] = abstract
        tgArticleItem["content"] = content
        tgArticleItem["url"] = response.url
        tgArticleItem["relate"] = relate
        tgArticleItem["PR"] = PR

        # 通过Itemloader加载item
        # 结合提取和实例化item，简化代码
        # from scrapy.loader import ItemLoader
        # # 调用自定义的itemLoader
        # from ArticleSpider.items import ArticleItemLoader
        # itemLoader = ArticleItemLoader(item=tgbusArticleItem(), response=response)
        # itemLoader.add_css("", "")
        # itemLoader.add_value("", )
        # # 默认item方法会将所有项变为list
        # tgArticleItem = itemLoader.load_item()


        yield tgArticleItem #settings

        pass
