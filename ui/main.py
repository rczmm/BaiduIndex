# # Form implementation generated from reading ui file 'main.ui'
# #
# # Created by: PyQt6 UI code generator 6.6.1
# #
# # WARNING: Any manual changes made to this file will be lost when pyuic6 is
# # run again.  Do not edit this file unless you know what you are doing.
import random

from PyQt6 import QtCore, QtWidgets, QtQuickWidgets, QtWebEngineWidgets
from PyQt6.QtWidgets import QPushButton
from qt_material import apply_stylesheet

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1000, 600)

        self.centralwidget = QtWidgets.QWidget(parent=MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        self.quickWidget = QtQuickWidgets.QQuickWidget(parent=self.centralwidget)
        self.quickWidget.setGeometry(QtCore.QRect(0, 250, 300, 200))
        self.quickWidget.setResizeMode(QtQuickWidgets.QQuickWidget.ResizeMode.SizeRootObjectToView)
        self.quickWidget.setObjectName("quickWidget")

        self.webEngineView = QtWebEngineWidgets.QWebEngineView(parent=self.centralwidget)
        self.webEngineView.setGeometry(QtCore.QRect(0, 60, 1000, 600))
        self.webEngineView.setUrl(QtCore.QUrl("file:///../html/lineChartsCurrent.html"))
        self.webEngineView.setObjectName("webEngineView")

        self.horizontalLayoutWidget = QtWidgets.QWidget(parent=self.centralwidget)
        self.horizontalLayoutWidget.setGeometry(QtCore.QRect(0, 0, 1000, 51))
        self.horizontalLayoutWidget.setObjectName("horizontalLayoutWidget")

        self.horizontalLayout = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")

        self.pushButton_1 = QtWidgets.QPushButton(parent=self.horizontalLayoutWidget)
        self.pushButton_1.setObjectName("pushButton")
        self.pushButton_1.clicked.connect(self.on_button_1_clicked)
        self.pushButton_1.setMinimumHeight(40)
        self.pushButton_1.setMinimumWidth(100)
        self.pushButton_1.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.horizontalLayout.addWidget(self.pushButton_1)

        self.pushButton_2 = QtWidgets.QPushButton(parent=self.horizontalLayoutWidget)
        self.pushButton_2.setObjectName("pushButton_5")
        self.pushButton_2.clicked.connect(self.on_button_2_clicked)
        self.pushButton_2.setMinimumHeight(40)
        self.pushButton_2.setMinimumWidth(100)
        self.pushButton_2.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.horizontalLayout.addWidget(self.pushButton_2)

        self.pushButton_3 = QtWidgets.QPushButton(parent=self.horizontalLayoutWidget)
        self.pushButton_3.setObjectName("pushButton_2")
        self.pushButton_3.clicked.connect(self.on_button_3_clicked)
        self.pushButton_3.setMinimumHeight(40)
        self.pushButton_3.setMinimumWidth(100)
        self.pushButton_3.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.horizontalLayout.addWidget(self.pushButton_3)

        self.pushButton_4 = QtWidgets.QPushButton(parent=self.horizontalLayoutWidget)
        self.pushButton_4.setObjectName("pushButton_3")
        self.pushButton_4.clicked.connect(self.on_button_4_clicked)
        self.pushButton_4.setMinimumHeight(40)
        self.pushButton_4.setMinimumWidth(100)
        self.pushButton_4.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.horizontalLayout.addWidget(self.pushButton_4)

        self.pushButton_5 = QtWidgets.QPushButton(parent=self.horizontalLayoutWidget)
        self.pushButton_5.setObjectName("pushButton_3")
        self.pushButton_5.clicked.connect(self.on_button_5_clicked)
        self.pushButton_5.setMinimumHeight(40)
        self.pushButton_5.setMinimumWidth(100)
        self.pushButton_5.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.horizontalLayout.addWidget(self.pushButton_5)

        self.pushButton_6 = QtWidgets.QPushButton(parent=self.horizontalLayoutWidget)
        self.pushButton_6.setObjectName("pushButton_3")
        self.pushButton_6.setMinimumHeight(40)
        self.pushButton_6.setMinimumWidth(100)
        self.pushButton_6.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.pushButton_6.clicked.connect(self.on_button_6_clicked)
        self.horizontalLayout.addWidget(self.pushButton_6)

        self.pushButton_7 = QtWidgets.QPushButton(parent=self.horizontalLayoutWidget)
        self.pushButton_7.setObjectName("pushButton_3")
        self.pushButton_7.clicked.connect(self.on_button_7_clicked)
        self.pushButton_7.setMinimumHeight(40)
        self.pushButton_7.setMinimumWidth(100)
        self.pushButton_7.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.horizontalLayout.addWidget(self.pushButton_7)

        # 添加一个刷新的按钮，这个按钮点击后会刷新所有的子元素
        self.button = QPushButton("Refresh")
        self.button.clicked.connect(self.webEngineView.reload)
        self.horizontalLayout.addWidget(self.button)

        self.pushButton_8 = QtWidgets.QPushButton(parent=self.horizontalLayoutWidget)
        self.pushButton_8.setObjectName("pushButton_3")
        self.pushButton_8.clicked.connect(self.on_button_8_clicked)
        self.pushButton_8.setMinimumHeight(40)
        self.pushButton_8.setMinimumWidth(100)
        self.horizontalLayout.addWidget(self.pushButton_8)

        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(parent=MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "主页"))
        self.pushButton_1.setText(_translate("MainWindow", "搜索指数"))
        self.pushButton_2.setText(_translate("MainWindow", "兴趣分布"))
        self.pushButton_3.setText(_translate("MainWindow", "地区分布"))
        self.pushButton_4.setText(_translate("MainWindow", "需求图谱"))
        self.pushButton_5.setText(_translate("MainWindow", "人群分布—性别"))
        self.pushButton_6.setText(_translate("MainWindow", "人群分布—年龄"))
        self.pushButton_7.setText(_translate("MainWindow", "兴趣分布—TGI"))
        self.pushButton_8.setText(_translate("MainWindow", "资讯关注"))


    def on_button_1_clicked(self):
        self.webEngineView.setUrl(QtCore.QUrl("file:///../html/lineChartsCurrent.html"))

    def on_button_2_clicked(self):
        self.webEngineView.setUrl(QtCore.QUrl("file:///../html/BarCharts.html"))

    def on_button_3_clicked(self):
        self.webEngineView.setUrl(QtCore.QUrl("file:///../html/MapCharts.html"))

    def on_button_4_clicked(self):
        self.webEngineView.setUrl(QtCore.QUrl("file:///../html/wordCloudCharts.html"))

    def on_button_5_clicked(self):
        self.webEngineView.setUrl(QtCore.QUrl("file:///../html/PieCharts.html"))

    def on_button_6_clicked(self):
        self.webEngineView.setUrl(QtCore.QUrl("file:///../html/BarAgeCharts.html"))

    def on_button_7_clicked(self):
        self.webEngineView.setUrl(QtCore.QUrl("file:///../html/RadarCharts.html"))

    def on_button_8_clicked(self):
        self.webEngineView.setUrl(QtCore.QUrl("file:///../html/AQICharts.html"))


def main():
    import sys

    app = QtWidgets.QApplication(sys.argv)
    themes = ['dark_amber.xml', 'dark_blue.xml', 'dark_cyan.xml', 'dark_lightgreen.xml', 'dark_pink.xml',
              'dark_purple.xml', 'dark_red.xml', 'dark_teal.xml', 'dark_yellow.xml', 'light_amber.xml',
              'light_blue.xml', 'light_cyan.xml', 'light_cyan_500.xml', 'light_lightgreen.xml', 'light_pink.xml',
              'light_purple.xml', 'light_red.xml', 'light_teal.xml', 'light_yellow.xml']
    theme = themes[random.randint(0, len(themes) - 1)]
    apply_stylesheet(app, theme=theme)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec())

