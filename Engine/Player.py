from Engine.Object import Object

class Player(Object):
    
    
    def __init__(self, pos_x, pos_y, width, height, id=None):
        super().__init__(pos_x, pos_y, width, height, id=id)
        self.dx = 0
        self.dy = 0
        self.SPEED = 10
    
    def animate(self):
        
            if self.state == "idle":
                frame += 1
                if frame > 10:
                    frame = 1
                self.set_img('char/idle/Idle ('+str(frame)+').png')
            elif self.state == "runLeft":
                frame += 1
                if frame > 8:
                    frame = 1
                self.set_img('char/runLeft/Run ('+str(frame)+').png')
            elif self.state == "runRight":
                frame += 1
                if frame > 8:
                    frame = 1
                self.set_img('char/runRight/Run ('+str(frame)+').png')
            elif self.state == "jump":
                frame += 1
                if frame > 10:
                    frame = 1
                self.set_img('char/jump/Jump ('+str(frame)+').png')    
            elif self.state == "dead":
                frame += 1
                if frame > 10:
                    frame = 1
                self.set_img('char/dead/Dead ('+str(frame)+').png')
            elif self.state == 'shot':
                frame += 1
                if frame > 4:
                    frame = 1
                self.set_img('char/shoot/Shoot ('+str(frame)+').png')   
                
                
    def update(self):
            if len(keys_pressed) == 0:
                if jumps == 0:
                    o.state = 'idle'
            
            if Qt.Key_A in keys_pressed:
                if jumps == 0:
                    o.state = 'runLeft'
                if o.pos_x <= 0:
                    return
                dx -= self.SPEED
            if Qt.Key_D in keys_pressed:
                if jumps == 0:
                    o.state = 'runRight'
                if o.pos_x >= inst.width*0.5:
                    for obj in inst.objs:
                        if obj.id != 'player' and obj.id != 'potion':
                            obj.pos_x -= 3
                            if o.collision is not None:
                                check = o.collision.check(o)
                                if check is not None:
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
                    dx += self.SPEED
            if Qt.Key_W in keys_pressed:
                o.state = 'jump'
                if jumps < jump_limit:
                    print('jump')
                    jump = Force(AXIS_Y, 20, -7, 'jump')
                    dforce = ('gravity', jump)
                    o.add_dforce(dforce)
                    o.add_force(jump)
                    jumps += 1
                    # dy -= PLAYER_SPEED
            if Qt.Key_S in keys_pressed:
                dy += self.SPEED
            if Qt.Key_Up in keys_pressed:
                
                if able_to_shoot:
                    o.state = 'shot'
                    # proj_col = Collision(inst)
                    projectile = Projectile(o.pos_x, o.pos_y-100, 20, 20,'up', 'projectile')
                    projectile.state = 'shot'
                    force = Force(AXIS_Y, 1, 8, 'force')
                    projectile.add_force(force)
                    # projectile.add_collision(proj_col)
                    projectile.oncollide = projectile_collide
                    able_to_shoot = False
                    shoot_cooldown = cd
                    inst.add_obj(projectile)
            if Qt.Key_Left in keys_pressed:
                
                if able_to_shoot:
                    print('entrou')
                    o.state = 'shot'
                    proj_col = Collision(inst)
                    projectile = Projectile(o.pos_x - 100, o.pos_y, 20, 20,'left', 'projectile')
                    projectile.state = 'shot'
                    h_comp = Force(AXIS_X, 1, 8, 'i_comp')
                    projectile.add_force(h_comp)
                    projectile.add_collision(proj_col)
                    projectile.oncollide = projectile_collide
                    able_to_shoot = False
                    shoot_cooldown = cd
                    inst.add_obj(projectile)
            if Qt.Key_Right in keys_pressed:
                
                if able_to_shoot:
                    o.state = 'shot'
                    proj_col = Collision(inst)
                    projectile = Projectile(o.pos_x + o.width + 1, o.pos_y, 20, 20,'right', 'projectile')
                    projectile.state = 'shot'
                    h_comp = Force(AXIS_X, -1, 8, 'h_comp')
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
                
            self.move(AXIS_Y, dy)
            self.move(AXIS_X, dx)