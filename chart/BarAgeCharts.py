from pyecharts import options as opts
from pyecharts.charts import Timeline, Line, Bar, Grid
from qdata.sql import conn, cursor

cursor.execute("""
    SELECT word FROM personchartlike GROUP BY word
    """)

words = cursor.fetchall()

page = Timeline()

charts = []

for word in words:
    cursor.execute("""
        SELECT age,tgi,rate FROM personchartage WHERE word='{}'
        """.format(word[0]))
    data = cursor.fetchall()
    ages = []
    tgis = []
    rates = []
    for i in data:
        ages.append(i[0])
        tgis.append(i[1])
        rates.append(i[2])

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

    print(tgis)

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

    bar.overlap(line)
    charts.append(bar)

for chart in charts:
    page.add(chart, time_point="-")
page.render("../html/BarAgeCharts.html")