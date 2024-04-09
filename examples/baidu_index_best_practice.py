"""
百度指数数据获取最佳实践
此脚本完成
1. 清洗关键词
2. 发更少请求获取更多的数据
3. 请求容错
4. 容错后并保留当前已经请求过的数据，并print已请求过的keywords
"""
from queue import Queue
from typing import Dict, List
import traceback
import time

import pandas as pd
from qdata.baidu_index import get_search_index
from qdata.baidu_index.common import check_keywords_exists, split_keywords

# cookies = """BIDUPSID=38F5338FA8E28C949649AB1687617AF7; PSTM=1676143631; BAIDU_WISE_UID=wapp_1678162318556_633; BAIDUID=93FCA382B4563B8F51CDE204952C057E:FG=1; ab_jid=e4abc08fa33c106ce7d4fadfbd4328ae909f; ab_jid_BFESS=e4abc08fa33c106ce7d4fadfbd4328ae909f; __bid_n=1883243f92ac366ef74207; FPTOKEN=KOR8WhDJ0TErgEq6xG2cKv2uL9wlq9W66GBmnyW8IDa/OuNHGxqs9VxwwedUjebk0KkAn9gcODQHIizgJ/2BvylnOuutRpE0S8EcgCqiHpcZIXKcOQgt5bO5juTWiKSWFORjFY1XN16ER9bGMLBAqkPpoVbw5fmMTSQ7ds0V3YX34LHGBlBT04TXFeZsDn9hREroPm/gThtHF/9zUkAGyEUwS9V7hPlZMXQiE3fZPVXleRr70qltOvKsHa7EFSY03HLGM9+cwihQ78O1gFLY6LzX3ORS6bphwLV1UqqdCxdH3ZQjzqdcM2BgU8fhsfEGXbs5xsiWVzxtapMgwc0GXn6kG78Z2MCGVp4/hDVX1ZKJyZ2rX2s7M9jG9ZlZzi6yBEF/nH/5FaN3oCbJUaE7cw==|knhHzc2YDa1Iw2lVKeGHpyBpViTBszQfCMI9WhJmYl8=|10|0b84ea4b2244066ea71dc722b8d5c779; BAIDUID_BFESS=93FCA382B4563B8F51CDE204952C057E:FG=1; ZFY=zGGThvmmp2flsA9Kq0EYnK6n1hv5esOyd106m96fxH0:C; BDUSS=VRGMTRNUENlOXdCaXlGYjh1UDZqNVRmby0wejRsVWo2Yk1saHNsWURnckRVZUZsRVFBQUFBJCQAAAAAAAAAAAEAAAABVhBfxM66zrHKxKsAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAMPEuWXDxLllU; SIGNIN_UC=70a2711cf1d3d9b1a82d2f87d633bd8a04592714977I00FMrnYsdNpNn9JsaMZLoVrojWp7FXDDay3hhywkIh9%2F%2FCajJBXn3mib9ZvZ6XYFUa87WeuwpZQJqzVY7TEdzB4TqZarpHHxi3UbMeImE%2F7G4n%2FqcDw8jYqJPFDustedFDdXTCyaztJl6%2BPwDzUU761KQzBzc4N%2FyEJUGHYNErNxvxizJgCdm4lTqGJgQatTj9L69P9K6qSBdwDTR1sMUAsao0kTl7kyHwM2bnMX%2FB8Vc%2F9XPBaZsfehrcRqetZbeSucxn7EhD%2BZMM%2BHyrUhYPnqBecj1OlNd10qimdezH8pJe1s%2FGCetCL%2FZ91nX4E71660647481804412301593990903166; bdindexid=g0gm63dlptu7dthdjvo98rk014; ab_bid=065ac0f63a02df52a30340b2384e193d8cc9; ab_sr=1.0.1_ZTM2ZTA1Y2Q4ZTNmYzk1YzE0NDVlZDIwNWQ5NDZmODcwZWY4OWEwOTU5NTI5ODlhM2I2OTFlYjYwZTJkYzZkOWQzZjg5NWRhNTZlM2ZiNDE0ODhjMWYwMTBkNjliYzMxYWZlMzAxZTA1ZDM3OTkyZjZlYjhjZjUzMTRjNWU5NmI1MWFiOTAxZmYyNjA2ZmRhNDc5ZmM3Mjk5YTYzYzA3Yg==; H_PS_PSSID=40169_39662_40207_40211_40217_40222_40275_40283_40294_40289_40285_40317_40320_40079; BA_HECTOR=2585210l2g8400802505010khgutoe1iu2eka1t; BDORZ=B490B5EBF6F3CD402E515D22BCDA1598; BDRCVFR[feWj1Vr5u3D]=I67x6TjHwwYf0; PSINO=1; delPer=0; RT="z=1&dm=baidu.com&si=f4e23756-779a-4a04-8982-66686828deb1&ss=lt80pdfk&sl=4&tt=7i7&bcn=https%3A%2F%2Ffclog.baidu.com%2Flog%2Fweirwood%3Ftype%3Dperf"; BDUSS_BFESS=VRGMTRNUENlOXdCaXlGYjh1UDZqNVRmby0wejRsVWo2Yk1saHNsWURnckRVZUZsRVFBQUFBJCQAAAAAAAAAAAEAAAABVhBfxM66zrHKxKsAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAMPEuWXDxLllU"""


cookies = """BAIDUID=93FCA382B4563B8F51CDE204952C057E:FG=1; __bid_n=1883243f92ac366ef74207; FPTOKEN=KOR8WhDJ0TErgEq6xG2cKv2uL9wlq9W66GBmnyW8IDa/OuNHGxqs9VxwwedUjebk0KkAn9gcODQHIizgJ/2BvylnOuutRpE0S8EcgCqiHpcZIXKcOQgt5bO5juTWiKSWFORjFY1XN16ER9bGMLBAqkPpoVbw5fmMTSQ7ds0V3YX34LHGBlBT04TXFeZsDn9hREroPm/gThtHF/9zUkAGyEUwS9V7hPlZMXQiE3fZPVXleRr70qltOvKsHa7EFSY03HLGM9+cwihQ78O1gFLY6LzX3ORS6bphwLV1UqqdCxdH3ZQjzqdcM2BgU8fhsfEGXbs5xsiWVzxtapMgwc0GXn6kG78Z2MCGVp4/hDVX1ZKJyZ2rX2s7M9jG9ZlZzi6yBEF/nH/5FaN3oCbJUaE7cw==|knhHzc2YDa1Iw2lVKeGHpyBpViTBszQfCMI9WhJmYl8=|10|0b84ea4b2244066ea71dc722b8d5c779; BAIDUID_BFESS=93FCA382B4563B8F51CDE204952C057E:FG=1; ZFY=zGGThvmmp2flsA9Kq0EYnK6n1hv5esOyd106m96fxH0:C; Hm_lvt_d101ea4d2a5c67dab98251f0b5de24dc=1710744536,1711175736,1711206454,1711207329; BDUSS=E5RYjlubU91cTRzVUNwazF6VDh-dzlaeVVza2JwWHU5UkNQakcyZ1V5TEpnU1ptSUFBQUFBJCQAAAAAAQAAAAEAAABvNquEAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAMn0~mXJ9P5ld; bdindexid=7cu3d8m81f5sq27p9kc59a8ue4; SIGNIN_UC=70a2711cf1d3d9b1a82d2f87d633bd8a04612682199qdYi1ly7ew7uJWAGmdMQncrGt398bp8hivOz49P8Ag1eG%2BYRn2shVxyG7tHjdhonIovU%2BgEIF0OFnF6POdaQw3C3Z%2BmAo0%2Fjz39%2BHKl%2BKaO9eZjTTIcnOXRqt3v5LFcv9bzMqZb0CaTdIWdxhPy%2BQSf%2BU06%2BCVGH2aG0SY17QzS0szi2kbaivVAXBovm6gsaJgJx%2BKiIYqLZWMYZfhwH1L3xnqi2FnfKxxLfa4dahWTKI6qq0Ikn43TKm6dqPYJZ%2Fe%2FhxjMJXPXmAieQzz7ytCirisPtSyDKs1fXiOXttGk%3D85759847758836703849448790645265; __cas__rn__=461268219; __cas__st__212=ce45a22397ab3b3f351f6e090b9c32bbf2b90b83c65e014479ecf48c4847dd10271a4ff072eadfd673145885; __cas__id__212=54120342; CPTK_212=47702707; CPID_212=54120342; Hm_lpvt_d101ea4d2a5c67dab98251f0b5de24dc=1711255775; BDUSS_BFESS=E5RYjlubU91cTRzVUNwazF6VDh-dzlaeVVza2JwWHU5UkNQakcyZ1V5TEpnU1ptSUFBQUFBJCQAAAAAAQAAAAEAAABvNquEAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAMn0~mXJ9P5ld; ab_sr=1.0.1_ZDFkYjA5MGE4MjA4ZDY3ZGVjNzk1MGYwMTA1YzdmMmI1NWIxN2E1MmQzNDRlZmI1N2FmMjYzMTViZjM4OWFjNjdhMmQyMDUzZmY4MDdjOGI2NzMwN2NkYTI2MGMxMGYxMTBjOWY1MjhhYjJmYTIyZDhmNmFlMGYyNzZjNTMxYTg5MGM0ZWE5NTI5ZmQ4OWJhNDEyNWEyMGI1NzRlNzQ5MQ==; PSTM=1711255899; H_PS_PSSID=40169_40211_40320_40079_40364_40351_40375_40366_40416_40299_40467_40459_40317_39661_40506_40487_40512; BIDUPSID=38F5338FA8E28C949649AB1687617AF7; BA_HECTOR=2l808121252425ag852h208lg83u7n1ivvcas1s; BDORZ=B490B5EBF6F3CD402E515D22BCDA1598; """

def get_clear_keywords_list(keywords_list: List[List[str]]) -> List[List[str]]:
    q = Queue(-1)

    cur_keywords_list = []
    for keywords in keywords_list:
        cur_keywords_list.extend(keywords)

    # 先找到所有未收录的关键词
    for start in range(0, len(cur_keywords_list), 15):
        q.put(cur_keywords_list[start:start + 15])

    not_exist_keyword_set = set()
    while not q.empty():
        keywords = q.get()
        try:
            check_result = check_keywords_exists(keywords, cookies)
            time.sleep(5)
        except:
            traceback.print_exc()
            q.put(keywords)
            time.sleep(90)

        for keyword in check_result["not_exists_keywords"]:
            not_exist_keyword_set.add(keyword)

    # 在原有的keywords_list拎出没有收录的关键词
    new_keywords_list = []
    for keywords in keywords_list:
        not_exists_count = len([None for keyword in keywords if keyword in not_exist_keyword_set])
        if not_exists_count == 0:
            new_keywords_list.append(keywords)

    return new_keywords_list


def save_to_excel(datas: List[Dict]):
    pd.DataFrame(datas).to_excel("index.xlsx")


def get_search_index_demo(keywords_list: List[List[str]]):
    """
        1. 先清洗keywords数据，把没有收录的关键词拎出来
        2. 然后split_keywords关键词正常请求
        3. 数据存入excel
    """
    print("开始清洗关键词")
    requested_keywords = []
    keywords_list = get_clear_keywords_list(keywords_list)
    q = Queue(-1)

    for splited_keywords_list in split_keywords(keywords_list):
        q.put(splited_keywords_list)

    print("开始请求百度指数")
    datas = []
    while not q.empty():
        cur_keywords_list = q.get()
        try:
            print(f"开始请求: {cur_keywords_list}")
            for index in get_search_index(
                    keywords_list=cur_keywords_list,
                    start_date='2019-01-01',
                    end_date='2024-03-23',
                    cookies=cookies
            ):
                index["keyword"] = ",".join(index["keyword"])
                datas.append(index)
            requested_keywords.extend(cur_keywords_list)
            print(f"请求完成: {cur_keywords_list}")
            time.sleep(1)
        except:
            traceback.print_exc()
            print(f"请求出错, requested_keywords: {requested_keywords}")
            save_to_excel(datas)
            q.put(cur_keywords_list)
            time.sleep(3)

    save_to_excel(datas)
    return datas


import pymysql


def save_sql(datas):
    conn = pymysql.connect(
        host="localhost",
        port=3306,
        user="root",
        password="root",
        database="baiduindex"
    )

    cursor = conn.cursor()

    sql = '''create table if not exists keywords(
    keyword varchar(200) not null,
    Type varchar(200) not null,
    Date datetime,
    Nums int);'''
    cursor.execute(sql)

    for data in datas:
        if data["type"] == "all":
            sql = """
                insert into keywords(keyword,Type,Date,Nums)
                values ({},{},{},{})
                """.format("'" + data['keyword'] + "'",
                           "'" + data['type'] + "'",
                           "'" + data['date'] + "'",
                           "'" + data['index'] + "'")

            cursor.execute(sql, data)

    conn.commit()

    cursor.close()

    conn.close()




