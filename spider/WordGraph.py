# 这段代码用于从百度热搜词云接口获取热门搜索词，并将其存储在数据库中。
import requests
from qdata.cookie import cookies
from qdata.sql import utilSql


def wordGraph():
    i = 0
    # 创建一个 UtilSql 对象
    self = utilSql()

    # 遍历所有关键词
    keywords = utilSql.selectWords(self)

    # 定义一个 headers 变量，用于添加 cookie
    headers = {
        "cookie": cookies[i]
    }

    print(keywords)

    # 遍历所有关键词
    for keys in keywords:
        keys = keys[0].split(',')
        # 取出当前关键词
        for key in keys:
            # 定义一个 URL
            url = 'https://index.baidu.com/api/WordGraph/multi?wordlist={}'.format(key)
            # 使用 requests 模块发送 GET 请求，并获取响应数据
            data = requests.get(url, headers=headers).json()["data"]
            print(data)
            # 取出数据中的起始日期和结束日期
            start_date = data["period"].split('|')[0]
            end_date = data['period'].split('|')[1]
            # 取出数据中的关键词
            try:
                keyword = data['wordlist'][0]["keyword"]
                # 取出数据中的热门搜索词列表
                wordlists = data['wordlist'][0]['wordGraph']
                # 使用 UtilSql 对象创建表格 DemandChart
                utilSql.createTableDemandChart(self)
                for wordlist in wordlists:
                    # 使用 UtilSql 对象将数据插入到 DemandChart 表中
                    utilSql.insertDemandChart(self, keyword, wordlist, start_date, end_date)
            except IndexError:
                print("没有数据")

if __name__ == '__main__':
    wordGraph()