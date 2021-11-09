import sys
from Engine.Window import *
from Engine.Layer import *
from Engine.Object import *
from Engine.Physics.Collision import *
from Engine.Physics.Force import *
from PyQt5.QtWidgets import QApplication

inst = None


def update(layer):
    for o in inst.objs:
        o.apply_forces()


def key_event(event):
    for o in inst.objs:
        if o.keyevent is not None:
            o.keyevent(event, o)


def player_keyevent(event, obj):
    # if event.key() == Qt.Key_W:
    #     JUMP ANIM
    #     obj.move(AXIS_Y, -1)
    if event.key() == Qt.Key_A:
        obj.move(AXIS_X, -1)
    if event.key() == Qt.Key_S:
        obj.move(AXIS_Y, 1)
    if event.key() == Qt.Key_D:
        obj.move(AXIS_X, 1)


def main():
    update_interval = 20
    tick_rate = 0

    w = Window('1st Game :D', update, update_interval, tick_rate)
    w.set_keypressevent(key_event)

    gravity = Force(AXIS_Y, 1, 3)

    ground = Object(0, w.height - 51, w.width - 1, 50)
    player = Object(60, 430, 32, 32)
    player.set_keyevent(player_keyevent)
    box1 = Object(100, 500, 22, 32)
    box2 = Object(60, 400, 32, 32)
    box3 = Object(20, 500, 32, 32)

    global inst
    inst = w.mainlayer_instance()
    inst.add_obj(player)
    inst.add_obj(ground)
    inst.add_obj(box1)
    inst.add_obj(box2)
    inst.add_obj(box3)
    col = Collision(inst)
    player.add_collision(col)
    player.add_force(gravity)

    # w.set_mainlayer(l)
    w.show()


if __name__ == '__main__':
    main()