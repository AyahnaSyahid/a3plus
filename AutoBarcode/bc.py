from barcode import Code128
from svgwrite import cm, mm, px
import svgwrite

Drawing = svgwrite.Drawing
class Size():
    def __init__(self, w, h, unit='px'):
        self.width = w
        self.height = h
        self.unit = unit

    def getS(self, float_precision=2):
        """String Size -> width[unit], height[unit]"""
        FMT = "{:0." + str(float_precision) + "f}{}" if float_precision > 0 else "{}{}"
        #print(FMT)
        return [ FMT.format(s, self.unit) for s in self.getN ]

    @property
    def getN(self):
        return self.width, self.height

        
def calculate_size(code, size):
    w, h = size
    margin = int(w/5)
    rest = w - margin
    m_width = rest / len(code)
    modules = []
    cx = margin / 2
    mlist = []
    idx = 0
    while(True):
        if code[idx] == '1':
            c = 1
            while(idx + 1 < len(code)):
                if code[idx + 1] == '0':
                    break
                c += 1
                idx += 1
            mlist.append([1, c])
        else :
            c = 1
            while(idx + 1 < len(code)):
                if code[idx + 1] == '1':
                    break
                c += 1
                idx += 1
            mlist.append([0, c])
            
        if idx + 1 >= len(code):
            break
        idx += 1
    xpos = cx
    for r, c in mlist:
        if r:
            modules.append(((xpos, '0'), ( m_width * c, h )))
        xpos += c * m_width
            
    return (w, h), modules

def get_modules(code):
    ''''11100100001011' -> [[1,3],[0,2],[1,1],[0,4],[1,1],[0,1],[1,2]]'''    
    mlist = []
    idx = 0
    while(True):
        if code[idx] == '1':
            c = 1
            while(idx + 1 < len(code)):
                if code[idx + 1] == '0':
                    break
                c += 1
                idx += 1
            mlist.append([1, c])
        else :
            c = 1
            while(idx + 1 < len(code)):
                if code[idx + 1] == '1':
                    break
                c += 1
                idx += 1
            mlist.append([0, c])
            
        if idx + 1 >= len(code):
            break
        idx += 1
    return mlist

def test1():
    code = Code128("Test_Code128").build()[0]
    size, mod = calculate_size( code, (320, 140) )
    print(size)
    canvas = Drawing(filename="My.svg", size=( 320, 140 ))
    barcode = canvas.add(canvas.g(id='barcode_g'))
    barcode.add(canvas.rect( (0, 0), size, fill='white'))
    bc_part = barcode.add(canvas.g(id='bc_part'))
    for i in mod:
        bc_part.add(canvas.rect(i[0], i[1], fill='black'))
    canvas.save(pretty=True)

def test2(): 
    size = Size( 120 * 3.125, 55 * 3.125 ) # in 90dpi -> ' * 3.125 is for 300dpi 
    code = Code128("Holis_NHK").build()[0]
    modules = get_modules(code)
    Canv = Drawing(filename="Draw.svg", size = size.getS(float_precision=2))
    barcode = Canv.add(Canv.g(id="SomeID"))
    barcode.add(Canv.rect(('0','0'),size.getS(float_precision=2), fill='white'))
    xpos = int(size.getN[0] / 10)
    width = (size.getN[0] - ( size.getN[0] / 5)) / len(code)
    for ch, n in modules:
        pos = Size(xpos, 0)
        ms = Size(n * width, size.getN[1] * 7.5 / 10)
        if ch:
            barcode.add(Canv.rect((pos.getS()),(ms.getS()), fill="black"))
        xpos += ( n * width )
    barcode.add(Canv.text("Holis_NHK",x=["187.5px"], y=["162.5px"], style="fill:black;font-size:25pt;text-anchor:middle;"))
    Canv.save(pretty=True)
        

def test3(c):
    from defs import CustomWriter
    from barcode import Gs1_128
    
    c = Gs1_128(c)
    c.writer = CustomWriter()
    c.save(c)
    
if __name__ == "__main__":
    import sys
    code = sys.argv[1]
    test3(code)