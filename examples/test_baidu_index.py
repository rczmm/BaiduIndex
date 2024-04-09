from qdata.baidu_index import (
    get_feed_index,
    get_news_index,
    get_search_index,
    get_live_search_index
)
from qdata.baidu_index.common import check_keywords_exists

keywords_list = [['大米']]
cookies = """BIDUPSID=38F5338FA8E28C949649AB1687617AF7; PSTM=1676143631; BAIDU_WISE_UID=wapp_1678162318556_633; BAIDUID=93FCA382B4563B8F51CDE204952C057E:FG=1; ab_jid=e4abc08fa33c106ce7d4fadfbd4328ae909f; ab_jid_BFESS=e4abc08fa33c106ce7d4fadfbd4328ae909f; __bid_n=1883243f92ac366ef74207; FPTOKEN=KOR8WhDJ0TErgEq6xG2cKv2uL9wlq9W66GBmnyW8IDa/OuNHGxqs9VxwwedUjebk0KkAn9gcODQHIizgJ/2BvylnOuutRpE0S8EcgCqiHpcZIXKcOQgt5bO5juTWiKSWFORjFY1XN16ER9bGMLBAqkPpoVbw5fmMTSQ7ds0V3YX34LHGBlBT04TXFeZsDn9hREroPm/gThtHF/9zUkAGyEUwS9V7hPlZMXQiE3fZPVXleRr70qltOvKsHa7EFSY03HLGM9+cwihQ78O1gFLY6LzX3ORS6bphwLV1UqqdCxdH3ZQjzqdcM2BgU8fhsfEGXbs5xsiWVzxtapMgwc0GXn6kG78Z2MCGVp4/hDVX1ZKJyZ2rX2s7M9jG9ZlZzi6yBEF/nH/5FaN3oCbJUaE7cw==|knhHzc2YDa1Iw2lVKeGHpyBpViTBszQfCMI9WhJmYl8=|10|0b84ea4b2244066ea71dc722b8d5c779; BAIDUID_BFESS=93FCA382B4563B8F51CDE204952C057E:FG=1; ZFY=zGGThvmmp2flsA9Kq0EYnK6n1hv5esOyd106m96fxH0:C; BDUSS=VRGMTRNUENlOXdCaXlGYjh1UDZqNVRmby0wejRsVWo2Yk1saHNsWURnckRVZUZsRVFBQUFBJCQAAAAAAAAAAAEAAAABVhBfxM66zrHKxKsAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAMPEuWXDxLllU; SIGNIN_UC=70a2711cf1d3d9b1a82d2f87d633bd8a04592714977I00FMrnYsdNpNn9JsaMZLoVrojWp7FXDDay3hhywkIh9%2F%2FCajJBXn3mib9ZvZ6XYFUa87WeuwpZQJqzVY7TEdzB4TqZarpHHxi3UbMeImE%2F7G4n%2FqcDw8jYqJPFDustedFDdXTCyaztJl6%2BPwDzUU761KQzBzc4N%2FyEJUGHYNErNxvxizJgCdm4lTqGJgQatTj9L69P9K6qSBdwDTR1sMUAsao0kTl7kyHwM2bnMX%2FB8Vc%2F9XPBaZsfehrcRqetZbeSucxn7EhD%2BZMM%2BHyrUhYPnqBecj1OlNd10qimdezH8pJe1s%2FGCetCL%2FZ91nX4E71660647481804412301593990903166; bdindexid=g0gm63dlptu7dthdjvo98rk014; ab_bid=065ac0f63a02df52a30340b2384e193d8cc9; ab_sr=1.0.1_ZTM2ZTA1Y2Q4ZTNmYzk1YzE0NDVlZDIwNWQ5NDZmODcwZWY4OWEwOTU5NTI5ODlhM2I2OTFlYjYwZTJkYzZkOWQzZjg5NWRhNTZlM2ZiNDE0ODhjMWYwMTBkNjliYzMxYWZlMzAxZTA1ZDM3OTkyZjZlYjhjZjUzMTRjNWU5NmI1MWFiOTAxZmYyNjA2ZmRhNDc5ZmM3Mjk5YTYzYzA3Yg==; H_PS_PSSID=40169_39662_40207_40211_40217_40222_40275_40283_40294_40289_40285_40317_40320_40079; BA_HECTOR=2585210l2g8400802505010khgutoe1iu2eka1t; BDORZ=B490B5EBF6F3CD402E515D22BCDA1598; BDRCVFR[feWj1Vr5u3D]=I67x6TjHwwYf0; PSINO=1; delPer=0; RT="z=1&dm=baidu.com&si=f4e23756-779a-4a04-8982-66686828deb1&ss=lt80pdfk&sl=4&tt=7i7&bcn=https%3A%2F%2Ffclog.baidu.com%2Flog%2Fweirwood%3Ftype%3Dperf"; BDUSS_BFESS=VRGMTRNUENlOXdCaXlGYjh1UDZqNVRmby0wejRsVWo2Yk1saHNsWURnckRVZUZsRVFBQUFBJCQAAAAAAAAAAAEAAAABVhBfxM66zrHKxKsAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAMPEuWXDxLllU"""


def test_get_feed_index():
    """获取资讯指数"""
    for index in get_feed_index(
            keywords_list=keywords_list,
            start_date='2019-01-01',
            end_date='2024-03-01',
            cookies=cookies
    ):
        print(index)


def test_get_news_index():
    """获取媒体指数"""
    for index in get_news_index(
            keywords_list=keywords_list,
            start_date='2019-01-01',
            end_date='2024-03-01',
            cookies=cookies
    ):
        print(index)


def test_get_search_index():
    """获取搜索指数"""
    for index in get_search_index(
            keywords_list=keywords_list,
            start_date='2019-01-01',
            end_date='2024-03-01',
            cookies=cookies
    ):
        print(index)


def test_get_live_search_index():
    """获取搜索指数实时数据"""
    for index in get_live_search_index(
            keywords_list=keywords_list,
            cookies=cookies,
            area=0
    ):
        print(index)

    for index in get_live_search_index(
            keywords_list=keywords_list,
            cookies=cookies,
            area=911
    ):
        print(index)


def test_check_keywords():
    test_keywords = [
        "狗狗国故", "狗狗国的", "狗狗国的的", "狗狗国解决的", "男的女的给你吧大实现",
        "对你的回复", "电脑看是否", "面对面方法的", "那地方法规股份", "的那女的",
        "英短", "CF", "新冠疫苗", "极限挑战", "大家大家都"
    ]
    result = check_keywords_exists(test_keywords, cookies)
    print(result["not_exists_keywords"])
    print(result["exists_keywords"])


if __name__ == "__main__":
    # test_get_feed_index()
    # test_get_news_index()
    test_get_search_index()
    # test_get_live_search_index()
    # test_check_keywords()
