import json

import pyecharts
from pyecharts.charts import Timeline
from pyecharts import options as opts
from qdata.sql import cursor
from qdata.baidu_index.config import PROVINCE_CODE, CITY_CODE, convert_province_name

cursor.execute("""
    SELECT keyword FROM regionchart
    GROUP BY keyword
    """)

keywords = cursor.fetchall()

provinces = {v: k for k, v in PROVINCE_CODE.items()}
citys = {v: k for k, v in CITY_CODE.items()}

area = dict(provinces, **citys)

page = Timeline()

charts = []

for keyword in keywords:
    sql = """
        select prov,city from regionchart
        where keyword='{}'
        """.format(keyword[0])
    print(sql)
    cursor.execute(sql)
    data = cursor.fetchall()
    data_province = []
    data_city = []
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

        chinese = (
            pyecharts.charts.Map()
            .add(keyword, data_province, 'china')
            .set_global_opts(
                title_opts=opts.TitleOpts(title=keyword),
                visualmap_opts=opts.VisualMapOpts(
                    min_=0,
                    max_=1000,
                    is_piecewise=True
                ),
            )
        )

        charts.append(chinese)

for chart in charts:
    page.add(chart, time_point="-")
page.render("../html/MapCharts.html")
