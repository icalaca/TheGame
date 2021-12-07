import sys
import math
from Engine.Window import *
from Engine.Layer import *
from Engine.Object import *
from Engine.Physics.Collision import *
from Engine.Physics.Force import *
from PyQt5.QtWidgets import QApplication
import keyboard

inst = None
jump_limit = 2
jumps = 0
life = 3


def update(layer):
    for o in inst.objs:
        o.apply_forces()


def key_pressevent(event):
    for o in inst.objs:
        if o.keypressevent is not None:
            o.keypressevent(event, o)


def key_releaseevent(event):
    for o in inst.objs:
        if o.keyreleaseevent is not None:
            o.keyreleaseevent(event, o)


def mousepress_event(event):
    for o in inst.objs:
        if o.mousepressevent is not None:
            o.mousepressevent(event, o)


def create_potion(obj):
    # gravity = Force(AXIS_Y, -1, 3, 'gravity')
    # colision = Collision(inst)

    potion = Object(obj.pos_x, obj.pos_y, 16, 32, 'potion')
    # potion.add_force(gravity)
    # potion.add_collision(colision)
    inst.add_obj(potion)


def projectile_collide(obj1, obj2):
    global inst
    inst.objs.remove(obj1)
    if obj2.id == 'enemy':
        inst.objs.remove(obj2)
        create_potion(obj2)


def player_collide(obj1, obj2):
    global jumps
    global life
    if obj2.id == 'ground' and jumps > 0:
        jumps = 0
    if obj2.id == 'potion':
        print('colisão com a poção')
        life += 1
        inst.objs.remove(obj2)
    if obj2.id == 'enemy':
        print('enemy')
        life -= 1
        if life == 0:
            print('perdeu')


def player_keypressevent(event, obj):
    global jumps
    global jump_limit
    h_collision = False
    if event.key() == Qt.Key_W:
        if jumps < jump_limit:
            print('jump')
            jump = Force(AXIS_Y, 15, -3, 'jump')
            dforce = ('gravity', jump)
            obj.add_dforce(dforce)
            obj.add_force(jump)
            jumps += 1
    if event.key() == Qt.Key_A:
        obj.move(AXIS_X, -3)
    if event.key() == Qt.Key_S:
        obj.move(AXIS_Y, 3)
    if event.key() == Qt.Key_D:
        if obj.pos_x >= inst.width*0.5:
            for o in inst.objs:
                if o.id != 'player' and o.id != 'potion':
                    o.pos_x -= 3
                    if obj.collision is not None:
                        check = obj.collision.check(obj)
                        if check is not None:
                            h_collision = True
                            o.pos_x += 3
                            break
                    o.pos_x += 3
            if not h_collision:
                for o in inst.objs:
                    if o.id != 'player':
                        o.move(AXIS_X, -3)
            else:
                h_collision = False
        else:
            obj.move(AXIS_X, 3)
    if event.key() == Qt.Key_Space:
        proj_col = Collision(inst)
        projectile = Object(obj.pos_x + obj.width + 1, obj.pos_y, 2, 2)
        h_comp = Force(AXIS_X, -1, 4, 'h_comp')
        projectile.add_force(h_comp)
        projectile.add_collision(proj_col)
        projectile.oncollide = projectile_collide
        inst.add_obj(projectile)
    if event.key() == Qt.Key_J:
        for o in inst.objs:
            o.move(AXIS_X, 3)
    if event.key() == Qt.Key_K:
        for o in inst.objs:
            o.move(AXIS_X, -3)


def player_keyreleaseevent(event, obj):
    # print('release')
    pass

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
    w.set_keypressevent(key_pressevent)
    w.set_keyreleaseevent(key_releaseevent)
    w.set_mousepressevent(mousepress_event)

    gravity = Force(AXIS_Y, -1, 5, 'gravity')

    ground = Object(0, w.height - 51, w.width + 1000, 50, 'ground')
    player = Object(90, 300, 32, 32, 'player')
    player.set_keypressevent(player_keypressevent)
    player.set_keyreleaseevent(player_keyreleaseevent)
    player.set_mousepressevent(player_mousepressevent)

    arm = Object(player.pos_x, player.pos_y, 50, 1)
    box2 = Object(90, 400, 150, 32, 'ground')
    box3 = Object(20, 420, 8, 128)
    box4 = Object(160, 535, 150, 13, 'ground')

    targ1 = Object(400, 500, 16, 48, 'enemy')
    targ2 = Object(420, 500, 16, 48, 'enemy')
    targ3 = Object(440, 500, 16, 48, 'enemy')
    targ4 = Object(460, 500, 16, 48, 'enemy')
    targ5 = Object(480, 500, 16, 48, 'enemy')
    targ6 = Object(500, 500, 16, 48, 'enemy')
    targ7 = Object(520, 500, 16, 48, 'enemy')
    targ8 = Object(540, 500, 16, 48, 'enemy')
    targu1 = Object(400, 350, 16, 48, 'enemy')
    targu2 = Object(420, 350, 16, 48, 'enemy')
    targu3 = Object(440, 350, 16, 48, 'enemy')
    targu4 = Object(460, 350, 16, 48, 'enemy')

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
    player.add_collision(col)
    player.add_force(gravity)
    player.oncollide = player_collide

    # w.set_mainlayer(l)
    w.show()


if __name__ == '__main__':
    main()