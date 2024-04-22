import requests

from qdata.sql import utilSql
from qdata.cookie import cookies


def socailApiInterest():
    i = 0
    self = utilSql()

    keywords = utilSql.selectWords(self)

    headers = {
        'cookie': cookies[i]
    }

    utilSql.createTablePersonchartlike(self)

    for keyword in keywords:
        url = 'https://index.baidu.com/api/SocialApi/interest?wordlist[]={}&typeid='.format(keyword[0])
        responses = requests.get(url, headers=headers).json()
        responses = responses['data']['result']
        for response in responses:
            key = response['word']
            if key == '全网分布':
                key += keyword[0]
            interests = response['interest']
            for interest in interests:
                utilSql.insertePersonchartlike(self, key, interest)
if __name__ == '__main__':
    socailApiInterest()