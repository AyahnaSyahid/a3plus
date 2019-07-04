from win32com import client

class ApplicationContext(object):
    def __init__(self, appID):
        self.appID = appID
    
    def __enter__(self):
        return client.gencache.EnsureDispatch(self.appID)
        
    def __exit__(self, *args):
        pass


def get_position( col, row):
    start_point = (19, 33.75)
    x_offset = 33.75
    y_offset = 66
    cpos_x = start_point[0] + (col * x_offset)
    cpos_y = start_point[1] + (row * y_offset)
    return (cpos_x, cpos_y)

with ApplicationContext("Coreldraw.Application.20") as corel:
    corel.ActiveDocument.Unit = 3
    corel.ActiveDocument.ReferencePoint = 9
    template = corel.ActiveDocument.ActiveShape
    #
    with open("list.txt") as data:
        lines = [ x.strip() for x in data.readlines()]
        col = 0
        row = 0
        for line in lines:
            n, a = line.split(";")
            #n = line.strip()
            shape = template.Duplicate()
            shape.SetPositionEx(9, *get_position(col, row))
            shape.CreateSelection()
            corel.ActiveDocument.ActivePage.TextReplace("<name>", n, True)
            corel.ActiveDocument.ActivePage.TextReplace("<addr>", a, True)
            corel.ActiveDocument.ActiveShape.ConvertToCurves()
            col += 1
            if col > 3:
                col = 0
                row += 1
                if row > 2:
                    row = 0
                    newPage = corel.ActiveDocument.AddPagesEx(1, 140, 200)
                    newPage.Activate()
                    
