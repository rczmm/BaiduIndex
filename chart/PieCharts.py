from qdata.sql import cursor, conn
from pyecharts.charts import Pie, Grid, Timeline
from pyecharts import options as opts

cursor.execute("""
SELECT word FROM personchartgender GROUP BY word
""")

words = cursor.fetchall()
page = Timeline()
charts = []

for word in words:
    cursor.execute("""
    SELECT * FROM personchartgender WHERE word='{}'
    """.format(word[0]))

    result = cursor.fetchall()
    print(result)
    sexs, tgis, rates = [], [], []
    for i in result:
        sexs.append(i[1])
        tgis.append(i[2])
        rates.append(i[3])


    data = [{"name": g, "tgi": h, "rate": w} for g, h, w in zip(sexs, tgis, rates)]

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

for chart in charts:
    page.add(chart, time_point="")
page.render("../html/pieCharts.html")
