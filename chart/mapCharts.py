# 这段代码用于生成地图图表，它使用了 Python 的 Pyecharts 库。下面是加上中文注释后的代码：
import json
import os

import pyecharts
from pyecharts.charts import Timeline
from pyecharts import options as opts
from qdata.sql import utilSql
from qdata.baidu_index.config import PROVINCE_CODE, CITY_CODE, convert_province_name

# 定义一个函数，用于生成地图图表
def map_chart(old_styles, new_styles):
    # 使用 MySQL 数据库连接，查询地区热词
    utilSql.cursor_mysql.execute("""
        SELECT keyword FROM regionchart
        GROUP BY keyword
        """)

    # 定义一个变量，用于存储查询到的热词
    keywords = utilSql.cursor_mysql.fetchall()

    # 定义省市代码的映射关系
    provinces = {v: k for k, v in PROVINCE_CODE.items()}
    citys = {v: k for k, v in CITY_CODE.items()}

    area = dict(provinces, **citys)

    # 定义一个页面，用于存放多个图表
    page = Timeline()

    # 定义一个变量，用于存储生成的图表
    charts = []

    # 遍历热词，生成相应的地图图表
    for keyword in keywords:
        # 定义一个 SQL 语句，用于查询指定热词对应的省市数据
        sql = """
            select prov,city from regionchart
            where keyword='{}'
            """.format(keyword[0])
        # 使用 MySQL 数据库连接，执行 SQL 语句，并获取查询结果
        utilSql.cursor_mysql.execute(sql)
        data = utilSql.cursor_mysql.fetchall()
        # 定义两个列表，用于存储省市数据
        data_province = []
        data_city = []
        # 遍历查询结果，将省市数据添加到列表中
        for i in data:
            prov = i[0]
            city = i[1]
            prov = json.loads(prov)
            city = json.loads(city)

            if prov == "":
                break
            prov = {provinces[key]: value if key == value else value for key, value in prov.items()}
            city = {citys[key]: value if key == value else value for key, value in city.items()}
            data_province = list(prov.items())
            data_province = [(convert_province_name(name), value) for name, value in data_province]
            data_city = list(prov.items())
            data_city = [(convert_province_name(name), value) for name, value in data_city]

            # 调用函数，生成地图图表
            chinese = (
                pyecharts.charts.Map()
                .add(keyword, data_province, 'china')
                .set_global_opts(
                    title_opts=opts.TitleOpts(title=keyword),
                    visualmap_opts=opts.VisualMapOpts(max_=1000, is_piecewise=True),
                )
            )

            # 调用函数，生成地图图表
            charts.append(chinese)

    # 调用函数，生成地图图表
    for chart in charts:
        page.add(chart, time_point="-")

    # 调用函数，生成地图图表
    path = os.getcwd() + "/html/MapCharts.html"
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
