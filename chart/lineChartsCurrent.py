import pyecharts
from pyecharts import options as opts
from pyecharts.charts import Page
from qdata.sql import conn, cursor
from sklearn.linear_model import LinearRegression
import numpy as np
from datetime import datetime, timedelta

cursor.execute("""
    SELECT keyword FROM keywords GROUP BY keyword
    """)

keywords = cursor.fetchall()

cursor.execute("""
    SELECT DATE_FORMAT(Date, '%Y-%m'), SUM(Nums), keyword 
    FROM keywords 
    GROUP BY DATE_FORMAT(Date, '%Y-%m'), keyword;
    """)
data = cursor.fetchall()
data = [list(i) for i in data]

cursor.close()
conn.close()

x_data = set()

for row in data:
    x_data.add(row[0])
x_data = sorted(x_data)
charts = []

next_time = datetime.now() + timedelta(days=30)

next_time = next_time.strftime("%Y-%m")

next_time1 = datetime.now() + timedelta(days=60)
next_time1 = next_time1.strftime("%Y-%m")
xdata, ydata = [], []

for keyword in keywords:

    y_data1 = [row[1] if row[2] == keyword[0] else "null" for row in data]

    y_data3 = []

    for i in y_data1:
        if i != "null":
            y_data3.append(i)
    x_data1 = []
    for i in x_data:
        x_data1.append(i)

    x_train = np.array([i for i in range(1, len(x_data) + 1)]).reshape(-1, 1)
    y_train = np.array([int(i) for i in y_data3])

    mode = LinearRegression().fit(x_train, y_train)
    future_time = np.array([11, 12]).reshape(-1, 1)
    future_data = mode.predict(future_time)

    for i in future_data:
        i = int(i)
        y_data3.append(i)

    x_data1.append(str(next_time))
    x_data1.append(str(next_time1))
    xdata = x_data1
    ydata.append(y_data3)

keywords = [''.join(i) for i in keywords]
print(keywords)
keywords = iter(keywords)
print(keywords)
line = (
    pyecharts.charts.Line()
    .set_global_opts(title_opts=opts.TitleOpts(title='指数变化'),
                     xaxis_opts=opts.AxisOpts(axislabel_opts=opts.LabelOpts(interval=0)),
                     datazoom_opts=opts.DataZoomOpts(is_show=True))
    .add_xaxis(xdata)
    .add_yaxis(next(keywords), ydata[0])
    .add_yaxis(next(keywords), ydata[1])
    .add_yaxis(next(keywords), ydata[2])
    .add_yaxis(next(keywords), ydata[3])
    .add_yaxis(next(keywords), ydata[4])
    .add_yaxis(next(keywords), ydata[5])
    .add_yaxis(next(keywords), ydata[6])
    .add_yaxis(next(keywords), ydata[7])
    .add_yaxis(next(keywords), ydata[8])
)

charts.append(line)

page = Page(layout=Page.SimplePageLayout)
for chart in charts:
    page.add(chart)
page.render("../html/lineChartsCurrent.html")

