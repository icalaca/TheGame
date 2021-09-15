class Object(object):
    def __init__(self, pos_x, pos_y, width, height):
        self.width = width
        self.height = height
        self.pos_x = pos_x
        self.pos_y = pos_y
        print(type(super()))

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

    def add_physics(self, physics):
        physics.apply_physics(self)
