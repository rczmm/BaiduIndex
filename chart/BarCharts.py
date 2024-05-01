# 这段代码用于生成柱状图和折线图的时间线，代码主要包括以下几个步骤：
# 1. 首先使用 pyecharts 库中的 Timeline 组件创建一个时间线对象。
# 2. 然后使用循环遍历一个包含单词列表的变量，并使用单词作为 Timeline 的时间点。
# 3. 在每个时间点中，使用 Bar 和 Line 组件分别生成一个柱状图和折线图。
# 4. 使用 add() 方法将每个图表添加到时间线中。
from pyecharts import options as opts
from pyecharts.charts import Timeline, Line, Bar
from qdata.sql import utilSql
import os

# 定义一个生成柱状图和折线图的时间线
def bar_chart(old_styles,new_styles):

    utilSql.cursor_mysql.execute("""
        SELECT word FROM personchartlike GROUP BY word
        """)

    # 遍历单词列表，并生成柱状图和折线图
    words = utilSql.cursor_mysql.fetchall()

    page = Timeline()

    charts = []

    for word in words:
        utilSql.cursor_mysql.execute("""
            SELECT interest,tgi,rate FROM personchartlike WHERE word='{}'
            """.format(word[0]))
        data = utilSql.cursor_mysql.fetchall()
        interests = []
        tgis = []
        rates = []
        for i in data:
            interests.append(i[0])
            tgis.append(i[1])
            rates.append(i[2])

        # 生成柱状图
        bar = (
            Bar()
            .set_global_opts(title_opts=opts.TitleOpts(title=word[0]))
            .add_xaxis(xaxis_data=interests)
            .add_yaxis(
                series_name="rate",
                y_axis=rates,
                label_opts=opts.LabelOpts(is_show=False)
            )
        )

        # 生成折线图
        line = (
            Line()
            .set_global_opts(title_opts=opts.TitleOpts(title=word[0]))
            .add_xaxis(xaxis_data=interests)
            .add_yaxis(
                series_name="tgi",
                y_axis=tgis,
                label_opts=opts.LabelOpts(is_show=False)
            )
        )

        # 合并柱状图和折线图
        bar.overlap(line)
        charts.append(bar)

    # 调用定义的函数生成柱状图和折线图的时间线
    for chart in charts:
        page.add(chart, time_point="")

    # 最后将生成的柱状图和折线图的时间线保存为 HTML 文件
    current_path = os.getcwd()
    page.render(current_path+"/html/BarCharts.html")

    path = current_path+"/html/BarCharts.html"

    # 打开生成的 HTML 文件，并将其中的 https://assets.pyecharts.org/assets/v5 路径替换为 ../js
    with open(path, encoding="utf-8") as f:
        data = f.read()
        for old_style,new_style in zip(old_styles,new_styles):
            data = data.replace(old_style,new_style)
        with open(path, "w", encoding="utf-8") as w:
            w.write(data)