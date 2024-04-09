import pyecharts
from pyecharts import options as opts
from pyecharts.charts import Page, Timeline
from qdata.sql import conn, cursor

cursor.execute("""
    SELECT keyword FROM demandchart GROUP BY keyword
    """)

keywords = cursor.fetchall()

charts = []

for keyword in keywords:
    sql = """
            SELECT word,ratio FROM demandchart WHERE keyword="{}"
        """.format(keyword[0])
    cursor.execute(sql)
    words = cursor.fetchall()
    words = list(words)
    wordcloud = (
        pyecharts.charts.WordCloud()
        .add("", data_pair=words, word_size_range=[6, 60],
             textstyle_opts=opts.TextStyleOpts(font_family="Microsoft YaHei", font_size='bold'))
        .set_global_opts(title_opts=opts.TitleOpts(title="{}新词".format(keyword[0]),
                                                   title_textstyle_opts=opts.TextStyleOpts(font_size=25,
                                                                                           color="midnightblue")))
    )
    charts.append(wordcloud)
cursor.close()
conn.close()

page = Timeline()
for chart in charts:
    page.add(
        chart,
        time_point="-"
    )
page.render("../html/wordCloudCharts.html")
