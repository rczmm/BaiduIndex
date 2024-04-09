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
create table if NOT EXISTS personchartgender(
word varchar(100) not null ,
sex varchar(10) not null ,
tgi varchar(10) not null,
rate varchar(10) not null
);
""")

cursor.execute("""
create table if NOT EXISTS personchartage(
word varchar(100) not null,
age varchar(10) not null,
tgi varchar(10) not null ,
rate varchar(10) not null 
);
""")

print(keywords)

for keyword in keywords:
    url = 'https://index.baidu.com/api/SocialApi/baseAttributes?wordlist[]={}'.format(keyword[0])
    response = requests.get(url, headers=headers).json()
    key = response['data']['result'][0]['word']
    genders = response['data']['result'][0]['gender']
    ages = response['data']['result'][0]['age']
    print(genders)
    for gender in genders:
        cursor.execute("""
            insert into personchartgender() values('{}','{}','{}','{}'); 
        """.format(key, gender['desc'], gender['tgi'], gender['rate']))

    for age in ages:
        cursor.execute("""
                    insert into personchartage() values('{}','{}','{}','{}'); 
                """.format(key, age['desc'], age['tgi'], age['rate']))

conn.commit()
cursor.close()
conn.close()
