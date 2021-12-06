AXIS_X = 0
AXIS_Y = 1


class Object(object):
    def __init__(self, pos_x, pos_y, width, height):
        self.width = width
        self.height = height
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.keyevent = None
        self.mousepressevent = None
        self.collision = None
        self.forces = []
        self.dforces = []
        self.oncollide = None
        self.name = ''

    def set_width(self, width):
        self.width = width

    def set_height(self, height):
        self.height = height

    def get_width(self):
        return self.width

    def get_height(self):
        return self.height

    def get_x(self):
        return self.pos_x

    def get_y(self):
        return self.pos_y

    def move(self, axis, value):
        if axis == AXIS_X:
            self.pos_x += value
        if axis == AXIS_Y:
            self.pos_y += value
        if self.collision is not None:
            check = self.collision.check(self)
            if check is not None:
                if self.oncollide is not None:
                    self.oncollide(self, check)
                if axis == AXIS_X:
                    self.pos_x -= value
                if axis == AXIS_Y:
                    self.pos_y -= value

    def set_keyevent(self, keyevent):
        self.keyevent = keyevent

    def set_mousepressevent(self, mousepressevent):
        self.mousepressevent = mousepressevent

    def add_collision(self, col):
        self.collision = col

    def add_physics(self, physics):
        physics.apply_physics(self)

    def add_force(self, force):
        self.forces.append(force)

    def add_dforce(self, f):
        self.dforces.append(f)

    def apply_forces(self):
        for f in self.forces:
            if f.id in [fd[0] for fd in self.dforces]:
                continue
            if f.it == -1:
                self.move(f.axis, f.mag)
                continue
            if f.iterate():
                self.forces.remove(f)
                for fd in self.dforces:
                    if fd[1] is f:
                        self.dforces.remove(fd)
            self.move(f.axis, f.mag)
