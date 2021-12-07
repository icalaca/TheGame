class Collision:
    def __init__(self, inst):
        self.inst = inst

    def check(self, o1):
        for o2 in self.inst.objs:
            if o1 is not o2:
                if o2.id == 'potion' and o1.id == 'player':
                    print('o1')
                    print(str(o1.pos_x) + 'posx')
                    print(str(o1.pos_y) + 'posy')
                    print(str(o1.id))
                    print('o2')
                    print(str(o2.pos_x) + 'posx')
                    print(str(o2.pos_y) + 'posy')
                    print(o2.id)
                
                if o1.pos_x < o2.pos_x + o2.width and \
                        o1.pos_x + o1.width > o2.pos_x and \
                        o1.pos_y < o2.pos_y + o2.height and \
                        o1.height + o1.pos_y > o2.pos_y:
                    print('entrou')
                    return o2
                
        return None
