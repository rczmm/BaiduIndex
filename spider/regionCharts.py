import requests

from qdata.sql import conn, cursor
from qdata.cookie import cookies
import json

sql = """
    create table if not exists regionchart(
    keyword varchar(100) not null,
    startdate date,
    enddate date,
    prov json not null,
    city json not null 
    );
"""

cursor.execute(sql)

headers = {
    "cookie": cookies
}

cursor.execute("""
SELECT keyword FROM demandchart 
GROUP BY keyword
""")

keywords = cursor.fetchall()
start_date = "2019-09-01"
end_date = "2024-03-01"

print(keywords)

for keyword in keywords:
    url = 'https://index.baidu.com/api/SearchApi/region?region=0&word={}&startDate={}&endDate={}&days'.format(
        keyword[0], start_date, end_date)
    r = requests.get(url, headers=headers).json()
    data = r['data']['region']
    key = data[0]['key']
    period = data[0]['period'].split('|')
    start_date = period[0]
    end_date = period[1]
    prov = data[0]['prov']
    city = data[0]['city']

    # 解决单双引号问题
    prov = json.dumps(prov)
    city = json.dumps(city)

    sql = """insert into regionchart(keyword,startdate,enddate,prov,city)
    values ({},{},{},'{}','{}');
    """.format(
        '"' + key + '"', "'" + start_date + "'", "'" + end_date + "'",
        prov, city)
    print(sql)
    cursor.execute(sql)

conn.commit()
cursor.close()
conn.close()
