from .SearchApi import seachApi
from .SocialApi import socialApi
from .WordGraph import wordGraph
from .SocialApiInterest import socailApiInterest

def get_data():
    start_date = '2019-01-01'
    end_date = '2024-04-01'
    wordGraph()
    seachApi(start_date,end_date)
    socialApi()
    socailApiInterest()
