import os

with open(os.getcwd()+'/file/cookies.txt', encoding='utf8') as f:
# with open('../file/cookies.txt', encoding='utf8') as f:
    cookies = f.readlines()

cookies = [i.replace('\n', '') for i in cookies]
