from chart.GetCharts import get_charts
from spider.GetData import get_data
from ui.main import main
from examples.test_baidu_index import BaiduIndex

if __name__ == '__main__':
    with open('file/关键词.txt', 'r', encoding='utf') as f:
        keywords = f.readlines()

    keywords_list = keywords
    keywords_list = [i.replace('\n', '') for i in keywords_list]
    keywords_list = [i.split(',') for i in keywords_list]
    print(keywords_list)
    # save_sql(get_search_index_demo(keywords_list))
    # get_data()
    get_charts()
    main()
