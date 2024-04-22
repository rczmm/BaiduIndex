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
from qdata.cookie import cookies

cookies = cookies[0]
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