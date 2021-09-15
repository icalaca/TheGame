from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from Engine.Object import *

class Layer(QWidget):
    def __init__(self, root_layer=None, width=-1, height=-1, x=0, y=0):
        super().__init__()
        self.root = root_layer
        self.width = width
        self.height = height
        self.x = x
        self.y = y
        self.objs = []

    def add_root(self, root_layer):
        self.root = root_layer

    def set_width(self, width):
        self.width = width

    def set_height(self, height):
        self.height = height

    def add_obj(self, obj):
        if obj.get_width() == -1:
            obj.set_width(self.width)
        if obj.get_height() == -1:
            obj.set_height(self.height)
        self.objs.append(obj)


    def draw_objects(self, event, qp):
        for o in self.objs:
            qp.drawRect(o.pos_x, o.pos_y, o.width, o.height)
            # qp.drawImage(x, y, QImage('imgs/entities/%s.png' % (e.name.lower())).scaledToWidth(32))

    def paintEvent(self, event):
        qp = QPainter()
        qp.begin(self)
        self.draw_objects(event, qp)
        qp.end()





