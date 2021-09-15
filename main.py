import sys
from Engine.Window import *
from Engine.Layer import *
from Engine.Object import *
from PyQt5.QtWidgets import QApplication

import Engine

def update(layer):
    print('layer')

def main():
    update_interval = 500
    tick_rate = 0

    w = Window('1st Game :D', update, update_interval, tick_rate)
    ground = Object(0, w.height - 1, w.width - 1, -50)
    player = Object(10, 50, 32, 32)

    inst = w.mainlayer_instance()
    inst.add_obj(ground)
    inst.add_obj(player)
    # w.set_mainlayer(l)
    w.show()


if __name__ == '__main__':
    main()