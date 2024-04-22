# 这段代码使用 Python 语言编写，主要是为了生成一个基于 pyecharts 的词云图，该词云图使用 MySQL 数据库中的数据。下面是加上中文注释后的代码：
import os

from qdata.sql import utilSql
from pyecharts.charts import Pie, Grid, Timeline
from pyecharts import options as opts

def pie_chart():
    # 使用 utilSql 工具类执行 SQL 查询，获取词云图需要的数据
    utilSql.cursor_mysql.execute("""
    SELECT word FROM personchartgender GROUP BY word
    """)
    # 遍历结果集，获取每个词的使用数量
    words =  utilSql.cursor_mysql.fetchall()
    page = Timeline() # 创建一个时间线组件
    charts = []
    # 遍历每个词，生成一个饼图
    for word in words:
        utilSql.cursor_mysql.execute("""
        SELECT * FROM personchartgender WHERE word='{}'
        """.format(word[0]))
        # 遍历结果集，获取每个词的性别、体质、得分等信息
        result =  utilSql.cursor_mysql.fetchall()
        sexs, tgis, rates = [], [], []
        for i in result:
            sexs.append(i[1])
            tgis.append(i[2])
            rates.append(i[3])
        # 将性别、体质、得分等信息转换为字典列表，方便后续使用
        data = [{"name": g, "tgi": h, "rate": w} for g, h, w in zip(sexs, tgis, rates)]
        # 使用饼图组件，添加两个系列，分别表示性别和得分
        pie = (
            Pie()
            .add(
                "tgi",
                [list(z) for z in zip([d["name"] for d in data], [d["tgi"] for d in data])],
                radius=["10%", "30%"],
                center=["25%", "50%"],
                label_opts=opts.LabelOpts(position="inside"),
            )
            .add(
                "rate",
                [list(z) for z in zip([d["name"] for d in data], [d["rate"] for d in data])],
                radius=["40%", "60%"],
                center=["75%", "50%"],
                label_opts=opts.LabelOpts(position="inside"),
            )
            .set_global_opts(
                title_opts=opts.TitleOpts(title=word[0]),
                legend_opts=opts.LegendOpts(
                    orient="vertical", pos_top="15%", pos_left="2%"
                ),
            )
            .set_series_opts(label_opts=opts.LabelOpts(formatter="{b}: {c}"))
        )
        charts.append(pie)
    # 使用时间线组件，将生成的饼图添加到时间线中
    for chart in charts:
        page.add(chart, time_point="")
    path = os.getcwd() + "/html/pieCharts.html"
    page.render(path)
    # 打开生成的 HTML 文件，并将其中的 https://assets.pyecharts.org/assets/v5 路径替换为 ../js
    with open(path, "r", encoding="utf-8") as f:
        data = f.read()
        data = data.replace('https://assets.pyecharts.org/assets/v5', '../js')
        with open(path, "w", encoding="utf-8") as w:
            w.write(data)
