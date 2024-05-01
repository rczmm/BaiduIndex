# 百度指数爬虫项目

该项目是一个用于爬取百度指数数据，并使用 Pyecharts 和 PyQt6 进行可视化的工具。百度指数是一个展示特定关键词在百度搜索引擎上的搜索趋势的指标，通过分析百度指数数据，可以了解关键词的热度变化情况。

## 功能特性

- 爬取指定关键词在百度指数的搜索数据。
- 使用 Pyecharts 将爬取的数据可视化展示，包括折线图、柱状图等。
- 使用 PyQt6 构建用户界面，方便用户交互和操作。

## 安装

1. 克隆项目到本地：

    ```bash
    git clone https://github.com/rczmm/BaiduIndex.git
    ```

2. 安装依赖：

    ```bash
    pip install -r requirements.txt
    ```

## 使用说明

1. 启动程序：

    ```bash
    python main.py
    ```

2. save_sql(get_search_index_demo(keywords_list))爬取关键词信息
3. 在spider目录下，可以爬取需求图谱与人群分布的信息
4. 在charts目录下，可以生成可视化界面
5. 界面引入了QSS，可自行更换
6. 在spider下的GetData文件中可选择更改数据的时间范围

## 注意事项
- 你需要自己定义cookies这样一个文本文件，并且在里面放置你自己的cookies

- 本项目仅供学习和研究使用，不得用于商业用途。
- 使用前请确保遵守百度指数数据的使用条款和规定。
- 如有任何问题或建议，欢迎在项目的 Issues 页面提出。