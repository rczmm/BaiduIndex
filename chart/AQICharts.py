import os
import numpy as np

from qdata.sql import utilSql
from pyecharts import options as opts
from pyecharts.charts import Timeline, Line, Bar


def aqi_charts(old_styles, new_styles):
    page = Timeline()
    sql = """
    SELECT keyword FROM `feed_index` GROUP BY keyword
    """
    utilSql.cursor_mysql.execute(sql)
    keywords = utilSql.cursor_mysql.fetchall()

    charts = []

    for keyword in keywords:
        title = keyword[0]
        select = """
        select date,value from `feed_index` where keyword = '{}'
        """.format(title)
        utilSql.cursor_mysql.execute(select)
        datas = utilSql.cursor_mysql.fetchall()
        result = []
        values = []
        for data in datas:
            date = str(data[0])
            value = data[1]
            values.append(value)
            result.append([date, value])
        values = [int(i) for i in values]
        vas = np.array(values)
        min_value = np.min(vas)
        max_value = np.max(vas)
        num_bins = 5
        bin_width = (max_value - min_value) / num_bins
        bins = [min_value + i * bin_width for i in range(num_bins + 1)]

        line = (
            Line()
            .add_xaxis([item[0] for item in result])
            .add_yaxis(title, [item[1] for item in result])
            .set_global_opts(
                title_opts=opts.TitleOpts(title=title),
                tooltip_opts=opts.TooltipOpts(trigger="axis"),
                toolbox_opts=opts.ToolboxOpts(
                    feature={
                        "dataZoom": {"yAxisIndex": "none"},
                        "restore": {},
                        "saveAsImage": {}
                    }
                ),
                datazoom_opts=[
                    opts.DataZoomOpts(start_value="2017-06-01"),
                    opts.DataZoomOpts(type_="inside")
                ],
                visualmap_opts=opts.VisualMapOpts(
                    pieces=[
                        {"gt": 10000, "lte": 50000, "color": "#93CE07"},
                        {"gt": 50000, "lte": 100000, "color": "#FBDB0F"},
                        {"gt": 100000, "lte": 150000, "color": "#FC7D02"},
                        {"gt": 150000, "lte": 200000, "color": "#FD0100"},
                        {"gt": 200000, "lte": 300000, "color": "#AA069F"},
                        {"gt": 300000, "color": "#AC3B2A"}
                    ],
                    out_of_range={"color": "#999"}
                ),
            )
            .set_series_opts(
                markline_opts=opts.MarkLineOpts(data=[{"yAxis": i} for i in bins])
                ,markpoint_opts=opts.MarkPointOpts(data=[opts.MarkPointItem(type_="max", name="最大值"),
                                                                 opts.MarkPointItem(type_="min", name="最小值")])
            )
        )
        charts.append(line)
        # 生成时间线页面，并将柱状图和折线图添加到页面中
    for chart in charts:
        page.add(chart, time_point="-")
    page.add_schema(
        is_auto_play=True,
        is_timeline_show=False
    )
    # 生成时间线页面，并将其保存为 HTML 文件
    path = os.getcwd() + "/html/AQICharts.html"
    page.render(path)
    # 打开生成的 HTML 文件，并将其中的 https://assets.pyecharts.org/assets/v5 路径替换为 ../js
    with open(path, "r", encoding="utf-8") as f:
        data = f.read()
        for old_style, new_style in zip(old_styles, new_styles):
            data = data.replace(old_style, new_style)
        with open(path, "w", encoding="utf-8") as w:
            w.write(data)
