import requests

from qdata.sql import conn, cursor
from qdata.cookie import cookies

cursor.execute("""
SELECT keyword FROM regionchart
""")

headers = {
    'cookie': cookies
}

keywords = cursor.fetchall()

cursor.execute("""
create table if NOT EXISTS personchartlike(
word varchar(100) NOT NULL,
interest varchar(10) not null ,
tgi varchar(10) not null,
rate varchar(10) not null);
""")

print(keywords)

for keyword in keywords:
    url = 'https://index.baidu.com/api/SocialApi/interest?wordlist[]={}&typeid='.format(keyword[0])
    print(url)
    response = requests.get(url, headers=headers).json()
    key = response['data']['result'][0]['word']
    interests = response['data']['result'][0]['interest']
    for interest in interests:
        cursor.execute("""
        insert into personchartlike() values ('{}','{}','{}','{}')
        """.format(key, interest['desc'], interest['tgi'], interest['rate']))
conn.commit()
cursor.close()
conn.close()
