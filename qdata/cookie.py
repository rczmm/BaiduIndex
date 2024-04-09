with open('../file/cookies.txt', 'r', encoding='utf8') as f:
    cookies = f.readlines()

cookies = cookies[0]
cookies = cookies.replace('\n','')
