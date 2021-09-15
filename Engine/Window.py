import sys
from Engine.Layer import *
from PyQt5.QtWidgets import QApplication, QWidget
from PyQt5 import QtCore


class Window(object):
    def timerCallback(self):
        if self.t_tick == self.tick_rate:
            self.update(self.mainlayer_instance())
            self.t_tick = 0
        else: self.t_tick += 1
        # self.updateEntitiesNames()
        self.mainlayer_instance().update()

    def __init__(self, title, update, update_interval, tick_rate):
        self.tick_rate = tick_rate
        self.t_tick = 0
        self.update_interval = update_interval
        self.update = update
        self.app = QApplication(sys.argv)
        self.w = QWidget()
        self.width = 800
        self.height = 600
        self.w.resize(self.width, self.height)
        self.w.setWindowTitle(title)
        self.main_layer = Layer(None, self.width, self.height, 0, self.height)

        self.layout = QHBoxLayout()
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.addWidget(self.main_layer)


        self.main_timer = QTimer()
        self.main_timer.setInterval(self.update_interval)
        self.main_timer.timeout.connect(self.timerCallback)
        self.main_timer.start()

        self.w.setLayout(self.layout)

        self.w.show()

    def set_mainlayer(self, main_layer):
        self.main_layer = main_layer

    def show(self):
        if (sys.flags.interactive != 1) or not hasattr(QtCore, 'PYQT_VERSION'):
            QApplication.instance().exec_()

    def mainlayer_instance(self):
        return self.main_layer

    def get_width(self):
        return self.width

    def get_height(self):
        return self.height

