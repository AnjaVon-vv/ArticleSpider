# -*- coding: utf-8 -*-
__author__ = 'Von'

import numpy as np
from elasticsearch import Elasticsearch
client = Elasticsearch(hosts=["192.168.1.106"])

def searchRelate(url):
    # 在相关页面中查找当前url
    response = client.search(
        index="tgbus",
        # index="tgbus",
        body={
            "query": {
                "term": {
                    "relate": url
                }
            }
        }
    )
    return response["hits"]["hits"]
def getUrl(sR):
    u = []
    for s in sR:
        u.append(s["_source"]["url"])
    return u

def writeFile(url, hits):
    # 将规则写入文件
    f = open("input", "a")
    for hit in hits:
        f.write(hit + ' ' + url + '\n')
    return

def clearFile():
    # 清空文件
    f = open("input", "r+")
    f.seek(0)
    f.truncate()
    return

x = 1 # 全局变量，用于计数算了多少个
def updatePR(art, pr):
    # 更新页面PR值
    client.index(
        index="tgbus",
        doc_type="von",
        id=art['_id'],
        body={
            "title":art["_source"]["title"],
            "suggestion":art["_source"]["suggestion"],
            "author":art["_source"]["author"],
            "keywords":art["_source"]["keywords"],
            "abstract":art["_source"]["abstract"],
            "content":art["_source"]["content"],
            "pubTime":art["_source"]["pubTime"],
            "url":art["_source"]["url"],
            "relate":art["_source"]["relate"],
            "PR": pr
        }
    )
    print("修改%s完成" % str(art["_source"]["url"]))
    global x
    x = x+1
    return

def calPR():
    response_all = client.search(
        index="tgbus",
        # index="tgbus",
        body={
            "query": {
                "term": {
                    "PR": 0.3
                }
            }
        }
    )
    for hitA in response_all["hits"]["hits"]:
        if hitA["_source"]["PR"] == 0.3:
            url = hitA["_source"]["url"]
            hits = searchRelate(url)
            if hits:
                hitsUrl = getUrl(hits)
                # 有与当前页面相关的项
                # 开始记录当前相关组的指向规则
                clearFile()
                group = [url] + hitsUrl
                writeFile(url, hitsUrl)
                
                # 对group[1]开始的所有项查找相关并将规则写入文件
                # 直到最后一项为止
                i =1
                while i < len(group):
                    hrs = searchRelate(group[i])
                    if hrs:
                        hrs = getUrl(hrs)
                        writeFile(group[i], hrs)
                        # 将查找到的去重加入group
                        for hr in hrs:
                            if hr not in group:
                                group.append(hr)
                    i = i + 1
                pagerank()
            else:
                # 无与当前页面相关的项、将当前文章PR值设为特定值
                updatePR(hitA, 0.00002333)
    return


def pagerank():
    # 读入指向规则，看作有向图
    f = open('input', 'r')
    edges = [line.strip('\n').split(' ') for line in f]
    # print(edges)

    # 根据边获取节点的集合
    nodes = []
    for edge in edges:
        if edge[0] not in nodes:
            nodes.append(edge[0])
        if edge[1] not in nodes:
            nodes.append(edge[1])
    print(nodes)

    N = len(nodes)

    # 将节点ID映射为数字，便于后面生成矩阵
    i = 0
    node_to_num = {}
    for node in nodes:
        node_to_num[node] = i
        i += 1
    for edge in edges:
        edge[0] = node_to_num[edge[0]]
        edge[1] = node_to_num[edge[1]]
    # print(edges)

    # 生成初步的关系矩阵
    S = np.zeros([N, N])
    for edge in edges:
        S[edge[1], edge[0]] = 1
    # print(S)
    # 计算一个网页对其他网页的PageRank值的贡献
        # 进行列的归一化处理
    for j in range(N):
        sum_of_col = sum(S[:, j])
        for i in range(N):
            if sum_of_col != 0:
                S[i, j] /= sum_of_col
            else:
                S[i, j] = 1 / N
    # print(S)

    d = 0.85 # 阻尼系数
    A = d * S + (1 - d) / N * np.ones([N, N])
    # print(A)

    # 生成初始的PageRank值，记录在pn中，pn和pnNext均用于迭代
    pn = np.ones(N) / N
    pnNext = np.zeros(N)

    e = 1  # 误差初始化
    k = 0  # 记录迭代次数
    # print('loop...')

    while e > 0.00000001:  # 开始迭代
        pnNext = np.dot(A, pn)  # 迭代公式
        e = pnNext - pn
        e = max(map(abs, e))  # 计算误差
        pn = pnNext
        k += 1
        # print('iteration %s:' % str(k), pnNext)

    print('final result:', pn)
    # 将计算所得PR数值写回
        # 改进方法：修改es数据结构对应url、relate和PR放入nested文档减少查询次数
                     # 更新时只写入PR
    i = 0
    for node in nodes:
        res = client.search(
            index="tgbus",
            doc_type="von",
            body={
                "query":{
                    "term":{
                        "url": node
                    }
                }
            }
        )
        updatePR(res["hits"]["hits"][0], pn[i])
        i = i + 1


if __name__ == '__main__':
    calPR()
    calPR()
    calPR()
    calPR()
    calPR()
    calPR()
    calPR()
    calPR()
    print(x) # 计数
