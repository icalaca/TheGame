import sys
import math
import random
from typing import Set
from Engine.Window import *
from Engine.Layer import *
from Engine.Object import *
from Engine.Physics.Collision import *
from Engine.Physics.Force import *
from PyQt5.QtWidgets import QApplication
#import keyboard

score = 0
cd = 50
shoot_cooldown = cd
able_to_shoot = True
dx = 0
dy = 0
keys_pressed = set()
inst = None
jump_limit = 1
jumps = 0
life = 3
firstrelease = False
PLAYER_SPEED = 8
frame = 1
def animate():
    global frame
    for obj in inst.objs:
        
        if obj.id == "enemy":
            
            if obj.state == "idle":
                obj.set_img('enemy/idle/gray__0000_idle_' +str(frame)+'.png')
            if obj.state == 'walkLeft':
                obj.set_img('enemy/walkLeft/gray__0000_walk_' +str(frame)+'.png')
            if obj.state == 'walkRight':
                obj.set_img('enemy/walkRight/gray__0000_walk_' +str(frame)+'.png')
            if obj.state == 'attack':
                obj.set_img('enemy/attack/gray__0000_attack_' +str(frame)+'.png')
        if obj.id == "projectile":
            if obj.state == 'shotRight':
                obj.set_img('char/bulletRight/Bullet_00'+str(frame)+'.png')
            if obj.state == 'shotLeft':
                obj.set_img('char/bulletLeft/Bullet_00'+str(frame)+'.png')
            if obj.state == 'shotUp':
                obj.set_img('char/bulletUp/Bullet_00'+str(frame)+'.png')
            if obj.state == 'shotDown':
                obj.set_img('char/bulletDown/Bullet_00'+str(frame)+'.png')
        if obj.id == "player":
            if obj.state == "idle":
                
                
                obj.set_img('char/idle/Idle ('+str(frame)+').png')
            elif obj.state == "runLeft":
                
                
                obj.set_img('char/runLeft/Run ('+str(frame)+').png')
            elif obj.state == "runRight":
                
                
                obj.set_img('char/runRight/Run ('+str(frame)+').png')
            elif obj.state == "jump":
                
                
                obj.set_img('char/jump/Jump ('+str(frame)+').png')    
            elif obj.state == "dead":
                
                
                obj.set_img('char/dead/Dead ('+str(frame)+').png')
            elif obj.state == 'shot':
                
                
                obj.set_img('char/shoot/Shoot ('+str(frame)+').png')  
                
    frame += 1  
    if frame > 10:
        frame = 1   
def update(layer):
    animate()
    global able_to_shoot
    global shoot_cooldown
    global jump_limit
    global jumps
    h_collision = False
    if not able_to_shoot:
            shoot_cooldown -= 1    
            if shoot_cooldown <= 0:
                able_to_shoot = True
    for o in inst.objs:
        if o.id == 'enemy':
            if o.timer == 0:
                o.timer = random.randint(17, 35)
                o.side = o.side * -1
            if o.side == -1:
                o.move(AXIS_X, -3)
                o.timer -= 1
            else:
                o.move(AXIS_X, 3)
                o.timer -= 1
                
        if o.id == 'player':
            if o.pos_y > inst.height:
                print('perdeu')
            if len(keys_pressed) == 0:
                if jumps == 0:
                    o.state = 'idle'
            global dx, dy
            if Qt.Key_A in keys_pressed:
                if jumps == 0:
                    o.state = 'runLeft'
                if o.pos_x <= 0:
                    return
                dx -= PLAYER_SPEED
            if Qt.Key_D in keys_pressed:
                if jumps == 0:
                    o.state = 'runRight'
                if o.pos_x >= inst.width*0.5:
                    for obj in inst.objs:
                        if obj.id == 'life':
                            print('liiiiffee')
                            continue
                        if obj.id != 'player' and obj.id != 'potion' and obj.id != 'item1' and obj.id != 'item2':

                            obj.pos_x -= 3
                            if o.collision is not None:
                                check = o.collision.check(o)
                                print('check')
                                print(check)
                                if check is not None:
                                    print('xavasca')
                                    if o.oncollide is not None:
                                        print('xoxota')
                                        o.oncollide(o, check)
                                    h_collision = True
                                    obj.pos_x += 3
                                    break
                                obj.pos_x += 3
                    if not h_collision:
                        for obj in inst.objs:
                            if obj.id != 'player':
                                obj.move(AXIS_X, -10)
                    else:
                        h_collision = False
                else:
                    dx += PLAYER_SPEED
            if Qt.Key_W in keys_pressed:
                o.state = 'jump'
                if jumps < jump_limit:
                    # print('jump')
                    jump = Force(AXIS_Y, 15, -10, 'jump')
                    dforce = ('gravity', jump)
                    o.add_dforce(dforce)
                    o.add_force(jump)
                    jumps += 1
                    # dy -= PLAYER_SPEED
            if Qt.Key_S in keys_pressed:
                dy += PLAYER_SPEED
            if Qt.Key_Up in keys_pressed:
                
                if able_to_shoot:
                    o.state = 'shot'
                    proj_col = Collision(inst)
                    projectile = Object(o.pos_x, o.pos_y + 10, 20, 20, inst, 'projectile')
                    projectile.state = 'shotUp'
                    h_comp = Force(AXIS_Y, -1, 8, 'h_comp')
                    projectile.add_force(h_comp)
                    projectile.add_collision(proj_col)
                    projectile.oncollide = projectile_collide
                    able_to_shoot = False
                    shoot_cooldown = cd
                    inst.add_obj(projectile)
            if Qt.Key_Left in keys_pressed:
                
                if able_to_shoot:
                    # print('entrou')
                    o.state = 'shot'
                    proj_col = Collision(inst)
                    projectile = Object(o.pos_x, o.pos_y, 20, 20,inst, 'projectile')
                    projectile.state = 'shotLeft'
                    h_comp = Force(AXIS_X, -1, -8, 'i_comp')
                    projectile.add_force(h_comp)
                    projectile.add_collision(proj_col)
                    projectile.oncollide = projectile_collide
                    able_to_shoot = False
                    shoot_cooldown = cd
                    projectile.move(AXIS_X, -100)
                    inst.add_obj(projectile)
            if Qt.Key_Right in keys_pressed:
                
                if able_to_shoot:
                    o.state = 'shot'
                    proj_col = Collision(inst)
                    projectile = Object(o.pos_x + o.width + 1, o.pos_y, 20, 20,inst, 'projectile')
                    projectile.state = 'shotRight'
                    h_comp = Force(AXIS_X, -1, 8, 'h_comp')
                    projectile.add_force(h_comp)
                    projectile.add_collision(proj_col)
                    projectile.oncollide = projectile_collide
                    able_to_shoot = False
                    shoot_cooldown = cd
                    inst.add_obj(projectile)
                    
            if Qt.Key_Down in keys_pressed:
                
                if able_to_shoot:
                    o.state = 'shot'
                    proj_col = Collision(inst)
                    projectile = Object(o.pos_x + o.width + 1, o.pos_y, 20, 20,inst, 'projectile')
                    projectile.state = 'shotDown'
                    h_comp = Force(AXIS_Y, -1, 8, 'h_comp')
                    projectile.add_force(h_comp)
                    projectile.add_collision(proj_col)
                    projectile.oncollide = projectile_collide
                    able_to_shoot = False
                    shoot_cooldown = cd
                    inst.add_obj(projectile)
                    
                
            if Qt.Key_J in keys_pressed:
                for o in inst.objs:
                    o.move(AXIS_X, 50)
            if Qt.Key_K in keys_pressed:
                for o in inst.objs:
                    o.move(AXIS_X, -50)

            if Qt.Key_Q in keys_pressed:
                sys.exit()
            o.move(AXIS_Y, dy)
            o.move(AXIS_X, dx)
            dx = 0
            dy = 0
        if o.id == 'projectile':
            o.apply_forces()
        o.apply_forces()
        


def keyPressEvent(event, o):
    firstrelease = True
    astr = "pressed: " + str(event.key())
    keys_pressed.add(event.key())


def keyReleaseEvent(event, o):
    # if firstrelease == True:
    #     processmultikeys(keylist)

    firstrelease = False

    keys_pressed.discard(event.key())
    # del keylist[-1]





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

def create_item(pos):
    gravity = Force(AXIS_Y, -1, 3, 'gravity')
    colision = Collision(inst)
    rand = random.randint(0, 5)
    if rand % 2 == 0:
        
        
        item = Object(pos[0], pos[1]-20, 24, 24,inst, 'item1')
        
        item.set_img('item.png')
    else:
        item = Object(pos[0], pos[1]-20, 24, 24,inst, 'item2')
        
        item.set_img('potions1.png')
        
    item.add_force(gravity)
    item.add_collision(colision)
    inst.add_obj(item)
    
def create_potion(pos):
    gravity = Force(AXIS_Y, -1, 3, 'gravity')
    colision = Collision(inst)
    potion = Object(pos[0], pos[1]-20, 24,24,inst, 'potion')
    
    potion.set_img('potions.png')
    potion.add_force(gravity)
    potion.add_collision(colision)
    inst.add_obj(potion)


def projectile_collide(obj1, obj2):
    global inst
    global score
    # print(obj1.id)
    if obj1 in inst.objs:
        inst.objs.remove(obj1)
    if obj2.id == 'enemy':
        score += 100
        inst.objs.remove(obj2)
        rand = random.randint(0, 100)
        if rand < 5:
            create_item((obj2.pos_x, obj2.pos_y))
            create_potion((obj2.pos_x + 40, obj2.pos_y))
        elif rand < 20:
            create_item((obj2.pos_x, obj2.pos_y))
        elif rand < 50:
            create_potion((obj2.pos_x, obj2.pos_y))
        


def player_collide(obj1, obj2):
    print('obj1')
    print(obj1.id)
    print('obj2')
    print(obj2.id)
    global jumps
    global jump_limit
    global life
    global cd

    # print(obj1.id)
    if (obj2.id == 'platform' or obj2.id == 'ground' or obj2.id == 'obstacle') and jumps > 0:
        if obj2.id == 'ground':
            jumps = 0
        if (obj1.pos_x > obj2.pos_x and obj1.pos_x < obj2.pos_x + obj2.width) and (obj1.pos_y < obj2.pos_y):
            # print('ei')
            jumps = 0
    if obj2.id == 'potion':
        # print('colisão com a poção')
        life += 1
        inst.objs.remove(obj2)
    if obj2.id == 'item2':
        jump_limit +=1
        inst.objs.remove(obj2)
    if obj2.id == 'item1':
        # print('item')
        if cd > 10:
            cd = cd/2
        inst.objs.remove(obj2)
    if obj2.id == 'enemy':
        # print('enemy')
        life -= 1
        inst.objs.remove(obj2)
        if life == 0:
            sys.exit()



def arm_mousepressevent(event, obj):
    r = 50
    for i in range(360):
        x = r*math.cos(math.radians(i))


def first_level(window):
    gravity = Force(AXIS_Y, -1, 10, 'gravity')
    colision = Collision(inst)
    # CHÃO DO PRIMEIRO NIVEL
    ground = Object(0, window.height - 51, window.width * 3, 50, inst,'ground', img='terrain.png')
    
    ground2 = Object(ground.width + 50, window.height - 51,
                     window.width + 700, 50,inst, 'ground', img='terrain.png')
    # ground2.set_img = "/Users/enriquebozzadutra/Documents/TheGame/terrain.png"
    ground3 = Object(ground.width + 50 + ground2.width + 50,
                     window.height - 51, window.width + 1400, 50,inst, 'ground', img='terrain.png')
    ground4 = Object(ground.width + 50 + ground2.width + 50 + ground3.width +
                     50, window.height - 51, window.width + 1400, 50,inst, 'ground', img='terrain.png')
    
    inst.add_obj(ground)
    inst.add_obj(ground2)
    inst.add_obj(ground3)
    inst.add_obj(ground4)

    # PLATAFORMAS
    platform = Object(760, 430, 100, 20,inst, 'platform', img='Group.png')
    platform2 = Object(ground.width + 50 + ground2.width /
                       3, 430, 100, 20, inst,'platform', img='Group.png')
    platform3 = Object(platform2.pos_x + platform2.width,
                       350, 270, 20,inst, 'platform', img='Group.png')
    platform4 = Object(platform3.pos_x + platform3.width +
                       50, 200, 170, 20,inst, 'platform', img='Group.png')
    platform5 = Object(platform4.pos_x + platform4.width -
                       50, platform2.pos_y, 50, 20,inst, 'platform', img='Group.png')
    platform6 = Object(platform3.pos_x + 3 * platform3.width,
                       200, 100, 20, inst,'platform', img='Group.png')
    platform7 = Object(ground3.pos_x + ground3.width/2,
                       platform6.pos_y - 50, 50, 20, inst,'platform', img='Group.png')
    platform8 = Object(platform7.pos_x + platform7.width,
                       100, 200, 20,inst, 'platform', img='Group.png')
    platform9 = Object(platform8.pos_x + platform8.width *
                       2, platform8.pos_y, 200, 20, inst,'platform', img='Group.png')
    platform10 = Object(platform9.pos_x + platform9.width,
                        platform3.pos_y - 70, 300, 20, inst,'platform', img='Group.png')
    platform11 = Object(platform10.pos_x + platform10.width +
                        100, 300, 300, 20, inst,'platform', img='Group.png')

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
    

    targ1 = Object(700, 300, 44, 100,inst, 'enemy')
    
    inst.add_obj(targ1)
    
    targ2 = Object(1100, 300, 44, 100,inst, 'enemy')
    inst.add_obj(targ2)

    targ3 = Object(1400, 300, 44, 100,inst, 'enemy')
    targ4 = Object(1450, 300, 44, 100,inst, 'enemy')
    targ5 = Object(platform3.pos_x + 50, platform3.pos_y - 48, 44, 100,inst, 'enemy')
    targ6 = Object(platform3.pos_x + 100, platform3.pos_y - 48, 44, 100, inst,'enemy')
    targ7 = Object(ground3.pos_x + 5, platform3.pos_y - 48, 44, 100,inst, 'enemy')
    targ8 = Object(ground3.pos_x + 130, platform3.pos_y - 48, 44, 100,inst, 'enemy')
    targ9 = Object(ground3.pos_x + 300, platform3.pos_y - 48, 44, 100,inst, 'enemy')
    targ10 = Object(ground3.pos_x + 480, platform3.pos_y - 200, 44, 100,inst, 'enemy')
    targ11 = Object(ground3.pos_x + 700, platform3.pos_y - 48, 44, 100,inst, 'enemy')
    targ12 = Object(ground3.pos_x + 800, platform3.pos_y - 48, 44, 100,inst, 'enemy')
    targ13 = Object(ground3.pos_x + 900, platform3.pos_y - 48, 44, 100,inst, 'enemy')
    targ14 = Object(ground3.pos_x + 1100, platform3.pos_y - 48, 44, 100,inst, 'enemy')
    targ15 = Object(ground3.pos_x + 1300, platform3.pos_y - 48, 44, 100,inst, 'enemy')
    targ16 = Object(ground3.pos_x + 1500, platform3.pos_y - 48, 44, 100,inst, 'enemy')
    targ17 = Object(ground3.pos_x + 1600, platform3.pos_y - 48, 44, 100,inst, 'enemy')
    targ18 = Object(ground3.pos_x + 1832, 100 - 48, 44, 100,inst, 'enemy')
    targ19 = Object(ground3.pos_x + 2030, 15, 44, 100,inst, 'enemy')
    targ20 = Object(ground3.pos_x + 2200, 150 - 48, 44, 100,inst, 'enemy')
    targ21 = Object(ground3.pos_x + 2500, 300- 48, 44, 100,inst, 'enemy')
    targ22 = Object(ground3.pos_x + 2400, 200 - 48, 44, 100,inst, 'enemy')
    targ23 = Object(ground3.pos_x + 2300, platform3.pos_y - 48, 44, 100,inst, 'enemy')
    
    targ1.add_collision(colision)
    targ2.add_collision(colision)
    targ3.add_collision(colision)
    targ4.add_collision(colision)
    targ5.add_collision(colision)
    targ6.add_collision(colision)
    targ7.add_collision(colision)
    targ8.add_collision(colision)
    targ9.add_collision(colision)
    targ10.add_collision(colision)
    targ11.add_collision(colision)
    targ12.add_collision(colision)
    targ13.add_collision(colision)
    targ14.add_collision(colision)
    targ15.add_collision(colision)
    targ16.add_collision(colision)
    targ17.add_collision(colision)
    targ18.add_collision(colision)
    targ19.add_collision(colision)
    targ20.add_collision(colision)
    targ21.add_collision(colision)
    targ22.add_collision(colision)
    targ23.add_collision(colision)
    
    targ1.add_force(gravity)
    targ2.add_force(gravity)
    targ3.add_force(gravity)
    targ4.add_force(gravity)
    targ5.add_force(gravity)
    targ6.add_force(gravity)
    targ7.add_force(gravity)
    targ8.add_force(gravity)
    targ9.add_force(gravity)
    targ10.add_force(gravity)
    targ11.add_force(gravity)
    targ12.add_force(gravity)
    targ13.add_force(gravity)
    targ14.add_force(gravity)
    targ15.add_force(gravity)
    targ16.add_force(gravity)
    targ17.add_force(gravity)
    targ18.add_force(gravity)
    targ19.add_force(gravity)
    targ20.add_force(gravity)
    targ21.add_force(gravity)
    targ22.add_force(gravity)
    targ23.add_force(gravity)


    inst.add_obj(targ3)
    inst.add_obj(targ4)
    inst.add_obj(targ5)
    inst.add_obj(targ6)
    inst.add_obj(targ7)
    inst.add_obj(targ8)
    inst.add_obj(targ9)
    inst.add_obj(targ10)
    inst.add_obj(targ11)
    inst.add_obj(targ12)
    inst.add_obj(targ13)
    inst.add_obj(targ14)
    inst.add_obj(targ15)
    inst.add_obj(targ16)
    inst.add_obj(targ17)
    inst.add_obj(targ18)
    inst.add_obj(targ19)
    inst.add_obj(targ20)
    inst.add_obj(targ21)
    inst.add_obj(targ22)
    inst.add_obj(targ23)
    
    trophy = Object(ground4.pos_x + ground4.width - 100, ground4.pos_y - 65, 52, 52, inst, 'trophy', 'trophy.png')
    
    inst.add_obj(trophy)


def main():
    global inst
    global life
    global score
    
    update_interval = 30
    tick_rate = 0

    w = Window('1st Game :D', update, update_interval, tick_rate)
    w.set_keypressevent(key_pressevent)
    w.set_keyreleaseevent(key_releaseevent)
    w.set_mousepressevent(mousepress_event)
    inst = w.mainlayer_instance()
    
    gravity = Force(AXIS_Y, -1, 10, 'gravity')

    
    player = Object(90, 300, 32, 48,inst, 'player')
    player.set_keypressevent(keyPressEvent)
    player.set_keyreleaseevent(keyReleaseEvent)
    # player.set_mousepressevent(player_mousepressevent)
    player.set_img("char/idle/Idle (1).png")
    

    lifetxt = Object(10, 15, 100, 50, inst, id='life')
    lifetxt.set_text('Lifes: ' + str(life))
    lifetxt.set_textsize(12)
    inst.add_obj(lifetxt)
    
    inst.add_obj(player)
    # inst.add_obj(arm)

    first_level(inst)

    col = Collision(inst)
    player.add_collision(col)
    player.add_force(gravity)
    player.oncollide = player_collide
    
    w.show()


if __name__ == '__main__':
    main()
