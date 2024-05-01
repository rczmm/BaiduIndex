import datetime
import random
import time

from qdata.baidu_index import (
    get_feed_index,
    get_news_index,
    get_search_index,
    get_live_search_index
)
from qdata.baidu_index.common import check_keywords_exists

from qdata.cookie import cookies
from qdata.sql import utilSql


class BaiduIndex:
    keywords_list = []
    cookies = cookies[7]

    def test_get_feed_index(self):
        utilSql.cursor_mysql.execute("""
        create table if not exists feed_index(
            keyword varchar(100) not null,
            date varchar(255) not null,
            value float not null);
        """)
        self.keywords_list = self.keywords_list[5:-1]
        for key in self.keywords_list:
            """获取资讯指数"""
            for index in get_feed_index(
                    keywords_list=[key],
                    start_date=str(datetime.date.today() - datetime.timedelta(days=30)),
                    end_date=str(datetime.date.today()),
                    cookies=self.cookies
            ):
                print(index)
                utilSql.cursor_mysql.execute(
                    """
                    insert into feed_index(keyword, date, value) values(%s, %s, %s)
                    """,(index['keyword'], index["date"], index["index"])
                )
                print("开始插入！")
            time.sleep(random.randint(1, 5))
            utilSql.conn_mysql.commit()

    def test_get_news_index(self):
        """获取媒体指数"""
        for index in get_news_index(
                keywords_list=self.keywords_list,
                start_date='2019-01-01',
                end_date='2024-03-01',
                cookies=self.cookies
        ):
            print(index)

    def test_get_search_index(self):
        """获取搜索指数"""
        for index in get_search_index(
                keywords_list=self.keywords_list,
                start_date='2019-01-01',
                end_date='2024-03-01',
                cookies=self.cookies
        ):
            print(index)

    def test_get_live_search_index(self):
        """获取搜索指数实时数据"""
        for index in get_live_search_index(
                keywords_list=self.keywords_list,
                cookies=self.cookies,
                area=0
        ):
            print(index)

        for index in get_live_search_index(
                keywords_list=self.keywords_list,
                cookies=self.cookies,
                area=911
        ):
            print(index)

    def test_check_keywords(self):
        result = check_keywords_exists(self.keywords_list, cookies)
        print(result["not_exists_keywords"])
        print(result["exists_keywords"])
