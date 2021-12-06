import sys
import math
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


def mousepress_event(event):
    for o in inst.objs:
        if o.mousepressevent is not None:
            o.mousepressevent(event, o)


def projectile_collide(obj1, obj2):
    global inst
    inst.objs.remove(obj1)
    inst.objs.remove(obj2)
    if(obj2.name == 'enemy'):
        gravity = Force(AXIS_Y, -1, 3, 'gravity')
        colision = Collision(inst)
        potion = Object(obj2.pos_x, obj2.pos_y, 16, 32)
        potion.name = 'potion'
        potion.add_force(gravity)
        potion.add_collision(colision)
        inst.add_obj(potion)
        


def player_keyevent(event, obj):
    if event.key() == Qt.Key_W:
        jump = Force(AXIS_Y, 15, -3, 'jump')
        dforce = ('gravity', jump)
        obj.add_dforce(dforce)
        obj.add_force(jump)
    if event.key() == Qt.Key_A:
        obj.move(AXIS_X, -10)
    if event.key() == Qt.Key_S:
        obj.move(AXIS_Y, 10)
    if event.key() == Qt.Key_D:
        obj.move(AXIS_X, 10)
    if event.key() == Qt.Key_R:
        obj.move(AXIS_Y, -50)
    if event.key() == Qt.Key_Space:
        proj_col = Collision(inst)
        projectile = Object(obj.pos_x + obj.width + 1, obj.pos_y, 2, 2)
        h_comp = Force(AXIS_X, -1, 4, 'h_comp')
        projectile.add_force(h_comp)
        projectile.add_collision(proj_col)
        projectile.oncollide = projectile_collide
        inst.add_obj(projectile)


def player_mousepressevent(event, obj):
    if event.button() == 1:
        projectile = Object(obj.pos_x, obj.pos_y, 1, 1)
        h_comp = Force(AXIS_X, 1, 4, 'h_comp')
        v_comp = Force(AXIS_Y, 1, 4, 'v_comp')
    print(event.button())
    print(event.pos())


def arm_mousepressevent(event, obj):
    r = 50
    for i in range(360):
        x = r*math.cos(math.radians(i))

def main():
    update_interval = 30
    tick_rate = 0

    w = Window('1st Game :D', update, update_interval, tick_rate)
    w.set_keypressevent(key_event)
    w.set_mousepressevent(mousepress_event)

    gravity = Force(AXIS_Y, -1, 3, 'gravity')

    ground = Object(0, w.height - 51, w.width - 1, 50)
    player = Object(90, 300, 32, 32)
    player.set_keyevent(player_keyevent)
    player.set_mousepressevent(player_mousepressevent)
    player.name = 'player'

    arm = Object(player.pos_x, player.pos_y, 50, 1)
    
    box2 = Object(90, 400, 150, 32)
    box3 = Object(20, 420, 8, 128)
    box4 = Object(160, 535, 150, 13)

    targ1 = Object(400, 500, 16, 48)
    targ1.name = 'enemy'
    targ2 = Object(420, 500, 16, 48)
    targ2.name = 'enemy'
    targ3 = Object(440, 500, 16, 48)
    targ3.name = 'enemy'
    targ4 = Object(460, 500, 16, 48)
    targ4.name = 'enemy'
    targ5 = Object(480, 500, 16, 48)
    targ5.name = 'enemy'
    targ6 = Object(500, 500, 16, 48)
    targ6.name = 'enemy'
    targ7 = Object(520, 500, 16, 48)
    targ7.name = 'enemy'
    targ8 = Object(540, 500, 16, 48)
    targ8.name = 'enemy'
    targu1 = Object(400, 350, 16, 48)
    targu1.name = 'enemy'
    targu2 = Object(420, 350, 16, 48)
    targu2.name = 'enemy'
    targu3 = Object(440, 350, 16, 48)
    targu3.name = 'enemy'
    targu4 = Object(460, 350, 16, 48)
    targu4.name = 'enemy'

    global inst
    inst = w.mainlayer_instance()
    inst.add_obj(player)
    # inst.add_obj(arm)
    inst.add_obj(ground)
    inst.add_obj(targ1)
    inst.add_obj(targ2)
    inst.add_obj(targ3)
    inst.add_obj(targ4)
    inst.add_obj(targ5)
    inst.add_obj(targ6)
    inst.add_obj(targ7)
    inst.add_obj(targ8)
    inst.add_obj(targu1)
    inst.add_obj(targu2)
    inst.add_obj(targu3)
    inst.add_obj(targu4)
    inst.add_obj(box2)
    inst.add_obj(box3)
    inst.add_obj(box4)
    col = Collision(inst)
    # player.add_collision(col)
    # player.add_force(gravity)
    for object in inst.objs:
        if object.name != '':
            object.add_force(gravity)
            object.add_collision(col)

    # w.set_mainlayer(l)
    w.show()


if __name__ == '__main__':
    main()