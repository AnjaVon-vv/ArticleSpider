# Python编写简单搜索引擎之爬虫篇（计算站内相关文章PageRank值）

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;爬取[电玩巴士](https://www.tgbus.com)部分文章作为后台数据，根据页面内相关文章计算PR值。爬取与计算均较为简单，不考虑复杂度，因此大量数据下运行时间较长有待改进。

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;具体是学习Mooc网bobby老师的课程，个人总结和教程之后写。<font color=#9055A2><b>(多么鲜艳的Flag)</font>

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;[<font color=#fbd14b> 搜索引擎搭建项目指路 </font>](https://github.com/AnjaVon-vv/VonSearch)

## 技术栈
- Python3
	- virtualenv、virtualenvwrapper（不必要,但建议使用，[<font color=#fbd14b> 安装教程 </font>](https://blog.csdn.net/sinat_41135487/article/details/106225574) ）
- 爬虫框架scrapy：`pip install scrapy`
- 搜索引擎支撑elasticsearch：
	- jdk8+
	- [elasticsearch-rtf](https://github.com/medcl/elasticsearch-rtf) ：大神开发的适用于中文的版本
	- [elasticsearch-head](https://github.com/mobz/elasticsearch-head) ：可视化数据
	- [kibana](https://github.com/elastic/kibana) ：运行不必要，学习ES建议安装
	- python编写接口包elasticsearch_dsl_py：`pip install elasticsearch-dsl`
- pagerank矩阵计算numpy：`pip install numpy`
- redis：`pip install redis`
    - windows下需安装redis-windows
    - 用于记录爬取总数传给搜索引擎（不重要、可直接注释相关代码）

## 运行
- [<font color=#fbd14b> 项目地址 </font>](https://github.com/AnjaVon-vv/ArticleSpider)
- 运行<font color=#fbd14b><b> esType.py </font>在ES中创建数据映射

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;因为在虚拟机写的python物理机运行ES所以改了各种连接配置

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;解决：替换所有的192.168.1.106为localhost
- 运行<font color=#fbd14b><b> main.py </font>开始爬虫（默认设置爬取500页、需半小时左右、可在tgbus.py内修改）
- 运行<font color=#fbd14b><b> pagerank.py </font>开始计算pr值

    - 存在重复扫描问题、待解决……
    - 程序运行较慢，主要是在写入和查询es的地方，还有在筛选相关内容的算法上。

P.S.如果网站有浏览量、点赞数、收藏数之类的数据可以作为添加网页权重值的依据改进为其他算法（比如HITS、TrustRank）
<br>
<table><tr><td bgcolor=#fffff3><font color=#6a60a9><b> 欢迎指正与讨论！</b></font></td></tr></table>