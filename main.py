__author__ = 'Von'

from scrapy.cmdline import execute
import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__))) #获取当前文件路径
execute(["scrapy", 'crawl', "tgbus"])



