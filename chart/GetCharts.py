from chart.BarCharts import bar_chart
from chart.BarAgeCharts import bar_age_charts
from .lineChartsCurrent import line_chart
from .mapCharts import map_chart
from .PieCharts import pie_chart
from .RadarCharts import radar_chart
from .wordCloudCharts import word_cloud_charts
from chart.AQICharts import aqi_charts

def get_charts():
    # bar_chart()
    # bar_age_charts()
    # line_chart()
    # map_chart()
    # pie_chart()
    # radar_chart()
    # word_cloud_charts()
    aqi_charts()

if __name__ == '__main__':
    get_charts()