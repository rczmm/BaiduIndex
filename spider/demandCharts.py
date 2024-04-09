import requests
from qdata.cookie import cookies
from qdata.sql import cursor, conn

select_sql = """
    SELECT keyword FROM `keywords` GROUP BY keyword
    """

cursor.execute(select_sql)

keywords = cursor.fetchall()

cursor.close()

cookies = cookies.replace('\n', '')

headers = {
    "cookie": cookies
}

for key in keywords:
    key = key[0]
    cursor = conn.cursor()
    url = 'https://index.baidu.com/api/WordGraph/multi?wordlist={}'.format(key)
    print(url)
    data = requests.get(url, headers=headers).json()["data"]
    start_date = data["period"].split('|')[0]
    end_date = data['period'].split('|')[1]
    keyword = data['wordlist'][0]["keyword"]
    wordlists = data['wordlist'][0]['wordGraph']
    sql = """
                create table if not exists demandChart(
                keyword varchar(100) not null,
                word varchar(100) not null,
                pv int not null,
                sim int not null,
                ratio int not null,
                start_date date not null,
                end_date date not null
                );
            """
    cursor.execute(sql)

    for wordlist in wordlists:
        sql = """
                    insert into demandChart(keyword,word,pv,sim,ratio,start_date,end_date)
                    values({},{},{},{},{},{},{})
                    """.format(
            "'" + keyword + "'",
            "'" + wordlist['word'] + "'", wordlist['pv'],
            wordlist['ratio'],
            wordlist['sim'],
            "'" + start_date + "'",
            "'" + end_date + "'"
        )
        cursor.execute(sql)
conn.commit()
cursor.close()
conn.close()
