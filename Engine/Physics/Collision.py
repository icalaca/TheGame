class Collision:
    def __init__(self, inst):
        self.inst = inst

    def check(self, o1):
        for o2 in self.inst.objs:
            if o1 is not o2:
                if o1.pos_x < o2.pos_x + o2.width and \
                        o1.pos_x + o1.width > o2.pos_x and \
                        o1.pos_y < o2.pos_y + o2.height and \
                        o1.height + o1.pos_y > o2.pos_y:
                    return o2
        return None
