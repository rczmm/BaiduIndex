# 这段代码的主要功能是使用 requests 库发送 HTTP GET 请求，从百度搜索 API 中获取关键词的性别和年龄信息，并将其存储在数据库中。
import requests
from qdata.sql import utilSql
from qdata.cookie import cookies


def socialApi():
    i = 0
    # 创建一个 UtilSql 对象
    self = utilSql()
    # 查询数据库中的关键词列表
    keywords = utilSql.selectWords(self)
    # 创建一个包含 cookie 的请求头
    headers = {
        'cookie': cookies[i]
    }

    # 创建表
    self.createTablePersonchartgender()
    self.createTablePersonchartage()

    # 遍历关键词列表，发送请求并存储数据
    for keyword in keywords:
        # 构造请求 URL
        url = 'https://index.baidu.com/api/SocialApi/baseAttributes?wordlist[]={}'.format(keyword[0])
        #发送 GET 请求，获取响应数据
        responses = requests.get(url, headers=headers).json()
        print(responses)

        # 遍历响应数据中的结果
        for response in responses['data']['result']:
            # 获取关键词和性别/年龄信息
            key = response['word']
            if key == '全网分布':
                key += keyword[0]
            genders = response['gender']
            ages = response['age']
            # 遍历性别列表，将数据插入到 person_chart_gender 表中
            for gender in genders:
                utilSql.insertePersonchartgender(self, key, gender)
            # 遍历年龄列表，将数据插入到 person_chart_age 表中
            for age in ages:
                utilSql.insertePersonchartage(self, key, age)
