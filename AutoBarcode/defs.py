from barcode.writer import (
                        BaseWriter,
                        create_svg_object,
                        _set_attributes,
                        pt2mm,
                        os
                        )

SIZE = "{:0.2f}"

class CustomWriter(BaseWriter):
    
    def __init__(self):
        BaseWriter.__init__(
            self,
            self._init,
            self._create_module,
            self._create_text,
            self._finish
            )
        self.compress = False
        self.dpi = 300
        self._document = None
        self._root = None
        self._group = None
        
        
    def _init(self, code,
        width = 120,
        height = 55 ):
            
        width, height = width, height
        self.module_height = height * 7.5 / 10
        self.quite_zone = width / 10
        self.module_area_width = width - (self.quiet_zone * 2)
        self.font_size = 3
        self._document = create_svg_object()
        self._root = self._document.documentElement
        attr = {
            'width': SIZE.format(width),
            'height': SIZE.format(height),
        }
        _set_attributes(self._root, **attr)
        # self._root.appendChild(self._document.createComment(COMMENT))
        # create group for easier handling in 3rd party software
        # like corel draw, inkscape, ...
        
        group = self._document.createElement('g')
        attributes = {'id': 'barcode_group'}
        _set_attributes(group, **attributes)
        self._group = self._root.appendChild(group)
        background = self._document.createElement('rect')
        attributes = {
            'width': SIZE.format(width),
            'height': SIZE.format(height),
            'style': 'fill:{0}'.format(self.background)
        }
        _set_attributes(background, **attributes)
        self._group.appendChild(background)
    
    def _create_module(self, xpos, ypos, width, color):
        element = self._document.createElement('rect')
        attributes = {
            'x': SIZE.format(xpos),
            'y': SIZE.format(ypos),
            'width': SIZE.format(width),
            'height': SIZE.format(self.module_height),
            'style': 'fill:{0};'.format(color)
        }
        _set_attributes(element, **attributes)
        self._group.appendChild(element)
        
    def render(self, code): ###### HERE
        
        if self._callbacks['initialize'] is not None:
            self._callbacks['initialize'](code)
        mlist = self.get_modules(code[0])
#print(mlist)
        ypos = 0
        painter = self._callbacks['paint_module']
        xpos = self.quiet_zone
        module_width = self.module_area_width / len(code[0])
        for ch, m in mlist:
            if ch == 1:
                painter(xpos, ypos, module_width * m, 'black')
            xpos += module_width * m
        ypos += self.module_height
        self.font_size = 3
        if self.text and self._callbacks['paint_text'] is not None:
            ypos = self.module_height / 6 * 7
            if self.center_text:
                # better center position for text
                xpos = ((self.quiet_zone * 2) + self.module_area_width) / 2
            else:
                xpos = bxs
            self._callbacks['paint_text'](xpos, ypos)
        return self._callbacks['finish']()
        
    def _create_text(self, xpos, ypos):
        if self.human != '':
            barcodetext = self.human
        else:
            barcodetext = self.text
        for subtext in barcodetext.split('\n'):
            element = self._document.createElement('text')
            attributes = {
                'x':
                SIZE.format(xpos),
                'y':
                SIZE.format(ypos),
                'style':
                'fill:{0};font-size:{1}pt;text-anchor:middle;'.format(
                    self.foreground,
                    self.font_size,
                )
            }
            _set_attributes(element, **attributes)
            text_element = self._document.createTextNode(subtext)
            element.appendChild(text_element)
            self._group.appendChild(element)
            ypos += pt2mm(self.font_size) + self.text_line_distance
            

    
    def _finish(self):
        if self.compress:
            return self._document.toxml(encoding='UTF-8')
        else:
            return self._document.toprettyxml(
                indent=4 * ' ', newl=os.linesep, encoding='UTF-8'
            )
    
    def save(self, filename, output):
        if self.compress:
            _filename = '{0}.svgz'.format(filename)
            f = gzip.open(_filename, 'wb')
            f.write(output)
            f.close()
        else:
            _filename = '{0}.svg'.format(filename)
            with open(_filename, 'wb') as f:
                f.write(output)
        return _filename
    
    def conv_desired(self, a):
        return a * 3.125
    
    def get_modules(self, code):
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
