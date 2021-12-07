from Engine.Object import Object


class Projectile(Object):
    
    
    
    def __init__(self, pos_x, pos_y, width, height, direction, id = None):
        super().__init__(pos_x, pos_y, width, height, id=id)
        self.direction = direction
        self.dx = 0
        self.dy = 0
        self.speed = 10
        self.frame = 1
        
    def animate(self):
        if self.state == 'shot':
            self.frame += 1
            if self.frame > 4:
                self.frame = 1
            frame_str = 'char/bullet/Bullet_00'+ str(self.frame) +'.png'
            self.set_img(frame_str)
            
    def update(self):
        if self.direction == 'up':
            self.move(AXIS_X, 100)