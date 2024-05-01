from chart.BarCharts import bar_chart
from chart.BarAgeCharts import bar_age_charts
from .lineChartsCurrent import line_chart
from .mapCharts import map_chart
from .PieCharts import pie_chart
from .PieChart import pie_charts
from .RadarCharts import radar_chart
from .wordCloudCharts import word_cloud_charts
from chart.AQICharts import aqi_charts

def get_charts():
    old_styles = ['https://assets.pyecharts.org/assets/v5','maps/','</head>\n<body >']
    new_styles = ['../js','maps_','</head><body ><style>body{background: #F6F6F6;}</style>']
    bar_chart(old_styles,new_styles)
    bar_age_charts(old_styles,new_styles)
    line_chart(old_styles,new_styles)
    map_chart(old_styles,new_styles)
    pie_chart(old_styles,new_styles)
    radar_chart(old_styles,new_styles)
    word_cloud_charts(old_styles,new_styles)
    aqi_charts(old_styles,new_styles)
    pie_charts(old_styles,new_styles)
