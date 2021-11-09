AXIS_X = 0
AXIS_Y = 1


class Object(object):
    def __init__(self, pos_x, pos_y, width, height):
        self.width = width
        self.height = height
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.keyevent = None
        self.collision = None
        self.forces = []

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
            if self.collision.check(self):
                if axis == AXIS_X:
                    self.pos_x -= value
                if axis == AXIS_Y:
                    self.pos_y -= value

    def set_keyevent(self, keyevent):
        self.keyevent = keyevent

    def add_collision(self, col):
        self.collision = col

    def add_physics(self, physics):
        physics.apply_physics(self)

    def add_force(self, force):
        self.forces.append(force)

    def apply_forces(self):
        for f in self.forces:
            if f.iterate():
                self.move(f.axis, f.mag)
