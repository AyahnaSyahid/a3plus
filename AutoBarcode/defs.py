



class Area():
    
    def __init__(self, x, y, w, h, parent=None):
        self.parent = parent
        self.posx = x
        self.posy = y
        self.width = w
        self.height = h
        
    def _set_parent(self, pr):
        self.parent = pr
    
    def