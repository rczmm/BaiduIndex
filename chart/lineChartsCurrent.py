# 这段代码用于生成一张包含多个折线图的 HTML 页面，其中每个折线图表示一个关键词的搜索量变化趋势。
# 首先，导入需要的库和模块：
import os

import pyecharts
from pyecharts import options as opts
from pyecharts.charts import Page
from qdata.sql import utilSql
from sklearn.linear_model import LinearRegression
import numpy as np
from datetime import datetime, timedelta

# 定义一个函数，用于生成折线图
def line_chart(old_styles, new_styles):
    # 使用 MySQL 数据库查询 keywords 表中的所有关键词，并将其保存在一个列表中
    utilSql.cursor_mysql.execute("""
        SELECT keyword FROM keywords GROUP BY keyword
        """)

    keywords = utilSql.cursor_mysql.fetchall()
    # 使用 MySQL 数据库查询 keywords 表中每日搜索量和关键词的数量，并将结果保存在一个列表中
    utilSql.cursor_mysql.execute("""
        SELECT DATE_FORMAT(Date, '%Y-%m'), SUM(Nums), keyword 
        FROM keywords 
        GROUP BY DATE_FORMAT(Date, '%Y-%m'), keyword;
        """)
    data = utilSql.cursor_mysql.fetchall()
    data = [list(i) for i in data]
    # 取出所有日期，并将其保存在一个集合中
    x_data = set()
    # 遍历数据集，并将关键词为 keyword 的每日搜索量添加到集合中
    for row in data:
        x_data.add(row[0])
    x_data = sorted(x_data)
    # 创建一个列表，用于保存生成的折线图
    charts = []
    # 遍历关键词列表，生成每张折线图
    next_time = datetime.now() + timedelta(days=30)
    # 将下一个月的日期转换为字符串，并将其添加到日期列表中
    next_time = next_time.strftime("%Y-%m")
    # 计算下一个三个月的日期
    next_time1 = datetime.now() + timedelta(days=60)
    next_time1 = next_time1.strftime("%Y-%m")
    xdata, ydata = [], []
    # 遍历关键词列表，生成每张折线图
    for keyword in keywords:
        # 定义两个列表，用于保存关键词的搜索量和日期
        y_data1 = [row[1] if row[2] == keyword[0] else "null" for row in data]
        # 遍历列表，将关键词为 keyword 的搜索量添加到列表中
        y_data3 = []
        # 遍历列表，将日期添加到列表中
        for i in y_data1:
            if i != "null":
                y_data3.append(i)
        x_data1 = []
        for i in x_data:
            x_data1.append(i)
        # 使用 Numpy 库将日期列表转换为数组，并添加一个列，用于保存搜索量
        x_train = np.array([i for i in range(1, len(x_data) + 1)]).reshape(-1, 1)
        # 使用 Numpy 库将搜索量列表转换为数组
        y_train = np.array([int(i) for i in y_data3])
        # 使用线性回归算法拟合数据，并预测未来三月的搜索量
        mode = LinearRegression().fit(x_train, y_train)
        future_time = np.array([11, 12]).reshape(-1, 1)
        future_data = mode.predict(future_time)
        # 将预测的搜索量添加到列表中
        for i in future_data:
            i = int(i)
            y_data3.append(i)
        # 将下一个月的日期添加到日期列表中
        x_data1.append(str(next_time))
        # 将下三个月的日期添加到日期列表中
        x_data1.append(str(next_time1))
        xdata = x_data1
        ydata.append(y_data3)
    # 将关键词转换为字符串，并将其添加到关键词列表中
    keywords = [''.join(i) for i in keywords]
    keywords = iter(keywords)
    # 使用折线图生成器创建折线图，并添加到列表中
    line = (
        pyecharts.charts.Line()
        .set_global_opts(title_opts=opts.TitleOpts(title='搜索指数'),
                         xaxis_opts=opts.AxisOpts(axislabel_opts=opts.LabelOpts(interval=0)),
                         datazoom_opts=opts.DataZoomOpts(),
                         legend_opts=opts.LegendOpts(pos_left='10%'),
                         )
        .add_xaxis(xdata)
        .add_yaxis(next(keywords), ydata[0])
        .add_yaxis(next(keywords), ydata[1])
        .add_yaxis(next(keywords), ydata[2])
        .add_yaxis(next(keywords), ydata[3])
        .add_yaxis(next(keywords), ydata[4])
        .add_yaxis(next(keywords), ydata[5])
        .add_yaxis(next(keywords), ydata[6])
        .add_yaxis(next(keywords), ydata[7])
    )
    # 创建一个页面，用于保存所有折线图
    charts.append(line)
    # 创建一个页面，用于保存所有折线图
    page = Page(layout=Page.SimplePageLayout)
    # 遍历折线图列表，将每个折线图添加到页面中
    for chart in charts:
        page.add(chart)
    # 保存页面，并将其保存在指定的 HTML 文件中
    path = os.getcwd() + "/html/lineChartsCurrent.html"
    page.render(path)
    # 打开生成的 HTML 文件，并将其中的 https://assets.pyecharts.org/assets/v5 路径替换为 ../js
    with open(path, "r", encoding="utf-8") as f:
        data = f.read()
        for old_style, new_style in zip(old_styles, new_styles):
            data = data.replace(old_style, new_style)
        with open(path, "w", encoding="utf-8") as w:
            w.write(data)

