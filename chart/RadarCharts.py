# 这段代码用于生成雷达图，代码主要包括以下几个步骤：
# 1. 导入需要的模块
import os

from pyecharts.charts import Radar, Timeline
from pyecharts import options as opts

# 2. 定义一个 radar_chart 函数，用于生成雷达图
from qdata.sql import utilSql


def radar_chart(old_styles, new_styles):
    page = Timeline()

    # 3. 定义一个 utilSql 类，用于执行 MySQL 查询
    charts = []

    # 4. 遍历 keywords，根据每个关键词生成一个雷达图
    utilSql.cursor_mysql.execute(
        """
         select word from personchartlike group by word
        """
    )

    keywords = utilSql.cursor_mysql.fetchall()

    for keyword in keywords:
        utilSql.cursor_mysql.execute(
            """
            select interest,tgi,rate from personchartlike where word = %s and word not like %s
            """, (keyword[0], "全网分布%")
        )
        count = utilSql.cursor_mysql.fetchall()
        # 5. 如果 count 不为空，则生成一个雷达图
        if count != ():
            # 6. 根据 count 生成雷达图的 schema
            schema = [
                {"name": i[0], "max": 160, "min": 0} for i in count[:]
            ]
            # 7. 根据 count 生成雷达图的数据
            tgi = [[i[1] for i in count[:]]]
            standard = [[100 for i in count[:]]]
            # 8. 使用 pyecharts 库生成雷达图
            radar = Radar()
            radar.add_schema(schema)
            radar.add("TGI", tgi)
            radar.add("standard", standard)
            radar.set_global_opts(title_opts=opts.TitleOpts(title=keyword[0]))
            charts.append(radar)

    # 9. 使用 timeline 组件将生成的雷达图添加到页面中
    for chart in charts:
        page.add(chart, '')

    # 10. 最后，使用 with 语句将生成的 HTML 代码写入文件，并将 pyecharts.org 的资源路径替换为本地路径
    path = os.getcwd() + "/html/RadarCharts.html"
    page.render(path)

    with open(path, "r", encoding="utf-8") as f:
        data = f.read()
        for old_style, new_style in zip(old_styles, new_styles):
            data = data.replace(old_style, new_style)
        with open(path, "w", encoding="utf-8") as w:
            w.write(data)
