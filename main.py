__author__ = 'Von'

import os
import sys

# 执行爬取程序
from scrapy.cmdline import execute

sys.path.append(os.path.dirname(os.path.abspath(__file__))) #获取当前文件路径
execute(["scrapy", 'crawl', "tgbus"])



