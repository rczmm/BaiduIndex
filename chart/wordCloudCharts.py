# 这段代码用于生成词云图，它首先从 demandchart 表中查询出所有不同的关键词，然后使用每个关键词生成一个词云图。下面是加上中文注释后的代码：
import os

import pyecharts
from pyecharts import options as opts
from pyecharts.charts import Page, Timeline
from qdata.sql import utilSql


def word_cloud_charts(old_styles, new_styles):
    utilSql.cursor_mysql.execute("""
        SELECT keyword FROM demandchart GROUP BY keyword
        """)

    # 定义一个 keywords 列表，用于存储查询出的关键词
    keywords = utilSql.cursor_mysql.fetchall()

    # 定义一个 charts 列表，用于存储生成的词云图对象
    charts = []

    # 遍历所有关键词，生成对应的词云图
    for keyword in keywords:
        # 定义一个 sql 语句，用于查询关键词对应的词和比例
        sql = """
                SELECT word,ratio FROM demandchart WHERE keyword="{}"
            """.format(keyword[0])
        # 执行 sql 语句，并将结果存储在 words 列表中
        utilSql.cursor_mysql.execute(sql)
        words = utilSql.cursor_mysql.fetchall()
        # 将 words 列表转换为数组
        words = list(words)
        # 使用 pyecharts 生成词云图
        wordcloud = (
            pyecharts.charts.WordCloud()
            .add("", data_pair=words, word_size_range=[6, 60],
                 textstyle_opts=opts.TextStyleOpts(font_family="Microsoft YaHei", font_size='bold'))
            .set_global_opts(title_opts=opts.TitleOpts(title="{}新词".format(keyword[0]),
                                                       title_textstyle_opts=opts.TextStyleOpts(font_size=25,color="blue")
                                                       ))
        )
        # 将生成的词云图添加到 charts 列表中
        charts.append(wordcloud)

    # 生成词云图的函数结束

    # 使用 Timeline 组件将生成的词云图组合在一起
    page = Timeline()
    for chart in charts:
        page.add(
            chart,
            time_point="-"
        )
    # 使用 render 函数将生成的词云图保存为 HTML 文件
    path = os.getcwd() + "/html/wordCloudCharts.html"
    page.add_schema(
        is_auto_play=True,
        is_timeline_show=False
    )
    page.render(path)
    # 打开生成的 HTML 文件，并将其中的 https://assets.pyecharts.org/assets/v5 路径替换为 ../js
    with open(path, "r", encoding="utf-8") as f:
        data = f.read()
        for old_style, new_style in zip(old_styles, new_styles):
            data = data.replace(old_style, new_style)
        with open(path, "w", encoding="utf-8") as w:
            w.write(data)
