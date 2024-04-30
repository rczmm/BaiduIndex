import datetime
import json
import sys
from qdata.sql import utilSql

import requests

def decrypt_func(key: str, data: str):
    a = key
    i = data
    n = {}
    s = []
    for o in range(len(a) // 2):
        n[a[o]] = a[len(a) // 2 + o]
    for r in range(len(data)):
        s.append(n[i[r]])
    return ''.join(s).split(',')

def get_ptbk(uniqid):
    url = 'http://index.baidu.com/Interface/ptbk?uniqid={}'
    resp = requests.get(url.format(uniqid), headers=headers)

    if resp.status_code != 200:
        print('获取uniqid失败')
        sys.exit(1)
    return resp.json().get('data')

def FeedApi():

    sql = """
    SELECT keyword FROM `regionchart`
    """

    utilSql.cursor_mysql.execute(sql)

    keywords = utilSql.cursor_mysql.fetchall()

    print(keywords)


    for keyword in keywords:

        url = 'https://index.baidu.com/api/FeedSearchApi/getFeedIndex?word=[[%7B"name":"{}","wordType":1%7D]]&area=0&startDate=2017-07-04&endDate=2024-04-28'.format(keyword[0])
        print(url)

        headers = {
            'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36',
            'cookie':'BAIDUID=7B5022DDADE42A699CF4DE24747B22F7:FG=1; BAIDUID_BFESS=7B5022DDADE42A699CF4DE24747B22F7:FG=1; PSTM=1713164760; BIDUPSID=38F5338FA8E28C949649AB1687617AF7; H_PS_PSSID=40368_40416_40511_40080; Hm_lvt_d101ea4d2a5c67dab98251f0b5de24dc=1713588764,1713685035,1713824824,1714442976; BDUSS=XVnbXJRUUFkWFIyZkhjcER3RTlGcEpRZEhURTdZMGUwVVMycm9oc2FGTWotRmRtSUFBQUFBJCQAAAAAAAAAAAEAAAATbf7wAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAACNrMGYjazBme; SIGNIN_UC=70a2711cf1d3d9b1a82d2f87d633bd8a04644616388t1q3crovl3TtwlCOY1ESS4M8cMO%2BUqD%2BC4FYG4wEKfEnTdC8nZYpghGtNnUDveT2klKr0yZIR9sBnibUn2naIZWzqhxgR5yHQb6%2FNXlEgxBOGJK1CXjqXK4leAK4v39kMk5LrV1Wm8l3oJGEgWf4sxRJtMN0HdVWFHgmOyrbknWUKuPaIutg6evo5DX%2FcF%2BRO%2ByW6F5BJeIRJyraHnECMdvwv1wHRrZLDqtvM4qeARckFXk8H3%2BBpcTdoBQK2zR0abmX7l2%2BvW76ybgzO2lMDaKHyz1PcKs1HefSiCDUFMc%3D67035361961946269103376099550245; __cas__rn__=464461638; __cas__st__212=8cc97d6bc14cb3966cbec92c1fde13864f29e5b990e9f0cb7d1ea0e184e0c1716be91226251f1f469f20c69d; __cas__id__212=55029529; CPTK_212=843990321; CPID_212=55029529; bdindexid=bd75oq1vi3n9ca8fo9aqjd8fk2; Hm_lpvt_d101ea4d2a5c67dab98251f0b5de24dc=1714449705; ab_sr=1.0.1_NWRlYWQwMTgxOTk2MGJjNDVmZWQ4OGRjZmI4MDVkNjUwYjZjMzg1NWY2YjFhNjMxZDcxZTk0MWQxNTBkODUwOGYzYjU2NGZjODM0NWEyMzMxZWZiZTQxMmYzZDQzOGVjNGFhNjk0MzIxNTgxZTgxZmQxN2YzYzJiYTQ1Mjg3OWM4MTllZjQwNDhmZGIwOWNmMDRiYzQzOTA2NzdhMDA3Yw==; BDUSS_BFESS=XVnbXJRUUFkWFIyZkhjcER3RTlGcEpRZEhURTdZMGUwVVMycm9oc2FGTWotRmRtSUFBQUFBJCQAAAAAAAAAAAEAAAATbf7wAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAACNrMGYjazBme; RT="z=1&dm=baidu.com&si=48605544-4c97-40be-a13e-7b89f5f5ee5b&ss=lvlr2y2a&sl=5j&tt=bd33&bcn=https%3A%2F%2Ffclog.baidu.com%2Flog%2Fweirwood%3Ftype%3Dperf&ld=40cjl"',
            'Cipher-Text' : '1652338834776_1714443873912_aal7J7yUZ9k/w7ytc3YysH1TfGwGt7yuoIrQ73DxACV0LURUpnrkXdvoH8ZXHQHRgTWREZ0rn0Idi/y9zERpQqSdovsBZfwLs1xFrtuGLNW1osBgf9/4I+gP8+JPMfh1D8mHUEf0xy7xPAMQrmXS13iJapPFHEiLeaxQtNazUoiD2E1//Yv4Vb836CEQMVZ0TLtrOLciRMnya6Lfi305Z05H7pk2v/7XiS4UjvTFHd11nzX8LLMvgneuIJ0/2a1y4MfKORBJ3RbeSiLe79aBKx/VMGcexECw77O8wdIXjeeSh9frMM58vcLnuYCErh3ovXD0mLPSkfzXuFUAxiCGdo8awJ/0cYX3douNq0zyW1MVjx7cZdTalCdgJa3jI049ubOj1Sqq169+JuZKKzciCOug1+YgNzzyhekPeeemFWk='
        }

        response = requests.get(url, headers=headers)

        print(response.text)

        data = response.text

        data = json.loads(data)

        uniqid = data['data']['uniqid']

        data = data['data']['index'][0]['data']

        feed_index = decrypt_func(get_ptbk(uniqid),data)

        feed_index = [i if i != '' else '0 ' for i in feed_index]

        print(len(feed_index))

        start_date = datetime.date(2017, 7, 1)

        print(start_date)

        for i in feed_index:
            insert = """
            insert into feed_index(keyword,date,value) values ('{}','{}','{}')
            """.format(keyword[0],start_date,i)
            start_date += datetime.timedelta(days=7)
            utilSql.cursor_mysql.execute(insert)

        utilSql.conn_mysql.commit()

        print(feed_index)