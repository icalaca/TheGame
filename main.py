import sys
import math
from Engine.Window import *
from Engine.Layer import *
from Engine.Object import *
from Engine.Physics.Collision import *
from Engine.Physics.Force import *
from PyQt5.QtWidgets import QApplication
#import keyboard

inst = None
jump_limit = 2
jumps = 0
life = 3


def update(layer):
    for o in inst.objs:
        o.apply_forces()
        
def keyPressEvent(self, event):
    self.firstrelease = True
    astr = "pressed: " + str(event.key())
    self.keylist.append(astr)

def keyReleaseEvent(self, event):
    if self.firstrelease == True: 
        self.processmultikeys(self.keylist)

    self.firstrelease = False

    del self.keylist[-1]

def processmultikeys(self,keyspressed):
    print(keyspressed)

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
    
    if (obj2.id == 'platform' or obj2.id == 'ground' or obj2.id == 'obstacle') and jumps > 0:
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
    if event.key() == Qt.Key_W:
        if jumps < jump_limit:
            print('jump')
            jump = Force(AXIS_Y, 15, -3, 'jump')
            dforce = ('gravity', jump)
            obj.add_dforce(dforce)
            obj.add_force(jump)
            jumps += 1
    if event.key() == Qt.Key_A:
        if obj.pos_x <= 0:
            return
        obj.move(AXIS_X, -10)
        
    if event.key() == Qt.Key_S:
        obj.move(AXIS_Y, 3)
    if event.key() == Qt.Key_D:
        if obj.pos_x >= inst.width*0.5:
            for o in inst.objs:
                if o.id != 'player':
                    o.move(AXIS_X, -10)
        else:
            obj.move(AXIS_X, 10)
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
            o.move(AXIS_X, 50)
    if event.key() == Qt.Key_K:
        for o in inst.objs:
            o.move(AXIS_X, -50)
        
    if event.key() == Qt.Key_Q:
        sys.exit()


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

def first_level(window):
    
    # CHÃO DO PRIMEIRO NIVEL
    ground = Object(0, window.height - 51, window.width+ 1400, 50, 'ground')
    ground2 = Object(ground.width + 50, window.height - 51, window.width/3 + 100, 50, 'ground')
    ground3 = Object(ground.width + 50 + ground2.width + 50, window.height - 51, window.width+ 1400, 50, 'ground')
    ground4 = Object(ground.width + 50 + ground2.width + 50 + ground3.width + 50, window.height - 51, window.width+ 1400, 50, 'ground')
    inst.add_obj(ground)
    inst.add_obj(ground2)
    inst.add_obj(ground3)
    inst.add_obj(ground4)
    
    
    
    # PLATAFORMAS 
    platform = Object(760, 430, 100, 20, 'platform')
    platform2 = Object(ground.width + 50 + ground2.width/3, 430, 100, 20, 'platform')
    platform3 = Object(platform2.pos_x + platform2.width, 350, 270, 20, 'platform')
    platform4 = Object(platform3.pos_x + platform3.width + 50, platform3.pos_y, 170, 20, 'platform')
    platform5 = Object(platform4.pos_x + platform4.width - 50, platform2.pos_y, 50, 20, 'platform' )
    platform6 = Object(platform5.pos_x + 3 * platform5.width, platform5.pos_y, 100, 20, 'platform' )
    platform7 = Object(ground3.pos_x + ground3.width/2, platform2.pos_y, 50, 20, 'platform' )
    platform8 = Object(platform7.pos_x + platform7.width, platform3.pos_y, 200, 20, 'platform' )
    platform9 = Object(platform8.pos_x + platform8.width * 2 , platform8.pos_y, 200, 20, 'platform' )
    platform10 = Object(platform9.pos_x + platform9.width , platform3.pos_y - 70, 300, 20, 'platform' )
    platform11 = Object(platform10.pos_x + platform10.width + 100, platform.pos_y, 300, 20, 'platform' )
    inst.add_obj(platform)
    inst.add_obj(platform2)
    inst.add_obj(platform3)
    inst.add_obj(platform4)
    inst.add_obj(platform5)
    inst.add_obj(platform6)
    inst.add_obj(platform7)
    inst.add_obj(platform8)
    inst.add_obj(platform9)
    inst.add_obj(platform10)
    inst.add_obj(platform11)
    obstacle = Object(900, window.height-100, 30, 100, 'obstacle')
    obstacle2 = Object(1300, window.height-120, 30, 100, 'obstacle')
    obstacle3 = Object(1700, window.height-140, 30, 100, 'obstacle')
    
    targ1 = Object(700, 500, 16, 48, 'enemy')
    
    inst.add_obj(targ1)
    targ2 = Object(1100, 500, 16, 48, 'enemy')
    inst.add_obj(targ2)
    
    targ3 = Object(1400, 500, 16, 48, 'enemy')
    targ4 = Object(1450, 500, 16, 48, 'enemy')
    
    inst.add_obj(targ3)
    inst.add_obj(targ4)
    inst.add_obj(obstacle)
    inst.add_obj(obstacle2)
    inst.add_obj(obstacle3)
    
    
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
    


    global inst
    inst = w.mainlayer_instance()
    inst.add_obj(player)
    # inst.add_obj(arm)
    
    first_level(inst)
    
    col = Collision(inst)
    player.add_collision(col)
    player.add_force(gravity)
    player.oncollide = player_collide

    # w.set_mainlayer(l)
    w.show()


if __name__ == '__main__':
    main()