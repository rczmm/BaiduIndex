# 这段代码用于生成柱状图和折线图的时间线页面，其中柱状图表示用户对话中出现的词的年龄分布，折线图表示用户对话中出现的词的时序关系。下面是加上中文注释的代码：
import os

from pyecharts import options as opts
from pyecharts.charts import Timeline, Line, Bar
from qdata.sql import utilSql

# 定义一个函数，用于生成柱状图和折线图的时间线页面
def bar_age_charts(old_styles, new_styles):
    # 使用 MySQL 数据库的 cursor_mysql 对象执行以下 SQL 语句，获取词云图中使用的词列表
    utilSql.cursor_mysql.execute("""
        SELECT word FROM personchartlike GROUP BY word
        """)
    # 取出词列表
    words = utilSql.cursor_mysql.fetchall()
    # 创建一个时间线图
    page = Timeline()
    # 创建一个空列表，用于存储生成的柱状图和折线图
    charts = []
    # 遍历词列表，生成每个词的柱状图和折线图
    for word in words:
        # 使用 MySQL 数据库的 cursor_mysql 对象执行以下 SQL 语句，获取指定词的年龄分布和时序关系数据
        utilSql.cursor_mysql.execute("""
            SELECT age,tgi,rate FROM personchartage WHERE word='{}'
            """.format(word[0]))
        # 取出年龄分布和时序关系数据
        data = utilSql.cursor_mysql.fetchall()
        ages = []
        tgis = []
        rates = []
        # 遍历数据，将年龄分布和时序关系数据添加到列表中
        for i in data:
            ages.append(i[0])
            tgis.append(i[1])
            rates.append(i[2])
        # 生成柱状图和折线图
        bar = (
            Bar()
            .set_global_opts(title_opts=opts.TitleOpts(title=word[0]))
            .add_xaxis(xaxis_data=ages)
            .add_yaxis(
                series_name='rate',
                y_axis=rates,
                label_opts=opts.LabelOpts(is_show=False)
            )
        )
        # 叠加柱状图和折线图
        line = (
            Line()
            .set_global_opts(title_opts=opts.TitleOpts(title=word[0]))
            .add_xaxis(xaxis_data=ages)
            .add_yaxis(
                series_name='tgi',
                y_axis=tgis,
                label_opts=opts.LabelOpts(is_show=False)
            )
        )
        # 叠加柱状图和折线图
        bar.overlap(line)
        charts.append(bar)
    # 生成时间线页面，并将柱状图和折线图添加到页面中
    for chart in charts:
        page.add(chart, time_point="-")
    # 生成时间线页面，并将其保存为 HTML 文件
    path = os.getcwd() + "/html/BarAgeCharts.html"
    page.render(path)
    # 打开生成的 HTML 文件，并将其中的 https://assets.pyecharts.org/assets/v5 路径替换为 ../js
    with open(path, "r", encoding="utf-8") as f:
        data = f.read()
        for old_style, new_style in zip(old_styles, new_styles):
            data = data.replace(old_style, new_style)
        with open(path, "w", encoding="utf-8") as w:
            w.write(data)