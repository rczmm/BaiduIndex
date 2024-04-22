# 这段代码用于从百度搜索关键词，并将搜索结果存储到数据库中。
import requests

from qdata.sql import utilSql
from qdata.cookie import cookies
import json


def seachApi(start_date, end_date):
    i = 0
    # 创建一个 UtilSql 对象
    self = utilSql()
    # 创建 regionchart 表
    utilSql.cretaeTableRegionchart(self)
    # 选择要搜索的关键词
    headers = {
        "cookie": cookies[i]
    }
    keywords = utilSql.selectWords(self)
    # 遍历每个关键词
    for keyword in keywords:
        # 拼接搜索 URL
        url = 'https://index.baidu.com/api/SearchApi/region?region=0&word={}&startDate={}&endDate={}&days'.format(
            keyword[0], start_date, end_date)
        # 使用 requests 模块发送 GET 请求，并解析 JSON 数据
        r = requests.get(url, headers=headers).json()
        while r['data'] == '':
            i += 1
            headers = {
                "cookie": cookies[i]
            }
            r = requests.get(url, headers=headers).json()
        datas = r['data']['region']
        # 遍历搜索结果
        for data in datas:
            # 提取关键词、开始日期、结束日期、省份、城市等信息
            key = data['key']
            period = data['period'].split('|')
            start_date = period[0]
            end_date = period[1]
            prov = data['prov']
            city = data['city']
            # 解决单双引号问题
            prov = json.dumps(prov)
            city = json.dumps(city)
            # 使用 UtilSql 对象将搜索结果插入 regionchart 表
            utilSql.insertRegionchart(self, key, start_date, end_date, prov, city)


if __name__ == '__main__':
    seachApi('2019-01-01', '2024-04-20')
