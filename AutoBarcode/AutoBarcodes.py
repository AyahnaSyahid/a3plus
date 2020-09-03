#!/bin/python3
"""
*** R 3 SEPT 2020 ***

PREPARASI : (SUKA LUPA) -> 
    atur ukuran page ke 325 * 485 ;
    tentukan xpos dengan cara membuat bidang persegi (BASE) dari pojok kiri atas page
    sampai titik tengah tempat barcode
            maka -> XPOS[0] = lebar BASE
                 -> XPOS[1] = tinggi BASE
"""
import barcode
from barcode.writer import mm2px as px
from svgwrite import mm
import svgwrite

getElementSize = lambda x: ( x['width'], x['height'] )

def createPage(name, sizemm=None):
    if not name.endswith('.svg'):
        name += '.svg'
    page = svgwrite.Drawing(name,size=(325 * mm, 485 * mm),viewBox="0 0 {} {}".format(px(325), px(485)))
    #create edges
    x = px(325 - 318) / 2
    y = px(485 - 475) / 2
    page.add(page.rect(
                        (0,0),
                        (px(318), px(475)),
                        fill="white",
                        fill_opacity="0",
                        style='stroke-width:2px;stroke:black;',
                        transform="translate({} {})".format(x, y)))
    page.save()
    return page

def getModules(btype, code):
    '''"11100100001011" -> [[1,3],[0,2],[1,1],[0,4],[1,1],[0,1],[1,2]]'''
    code = barcode.get_class(btype)(str(code).strip()).build()[0] 
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

def textAlign(txt, cpos, ftsize, maxwidth, ssize):
    # anggap fh == fw
    space_size = ftsize * ssize / 100
    print(space_size, ssize, ftsize)
    tlength = (len(txt) * ftsize) + ((len(txt) - 1) * space_size)
    if maxwidth < tlength:
        return textAlign(txt, cpos, ftsize, maxwidth, ssize / 2)
    posArray = []
    xpos = cpos[0] - ( tlength / 2 )
    for ch in txt:
        posArray.append([(xpos, cpos[1]), ch])
        xpos += ftsize + space_size
    return posArray

def addBarcode(elem, txcode, size, pos, rot, btype="gs1_128"):
    modules = getModules(btype, str(txcode).strip())
    
    # width of barcode
    ## total width
    sw, sh = size
    cx = size[0] / 2 if size[0] else 0
    cy = size[1] / 2 if size[1] else 0
    #cy = [ (lambda c: c / 2 if c else 0) for x in size ] # center point
    ## width of barcode
    sbw = ( size[0] * 863 / 1000 )
    ## height of barcode
    sbh = ( size[1] * 800 / 1000 )
    ## font height
    fh = ( size[1] * 125 / 1000 )
    ### calculate width of modules
    mc = 0 #module count
    for _, m in modules:
        mc += m
    mw = sbw / mc #module width
    mh = sbh      #module height
    
    bgroup = elem.g(id=txcode)
    
    elem.defs.add(bgroup)
    xpos = 0                       #initial xposition bar
    ypos = ( size[0] * 10 / 1000 ) #initial yposition bar
    ### add bg white to the group
    bgroup.add(elem.rect((xpos,0), (sw,sh), fill="white", fill_opacity="0"))
    xpos += (size[0] - sbw) / 2
    for m, c in modules:
        if m:
            bgroup.add(elem.rect(
                (xpos, ypos),
                (c * mw, mh),
                fill='black'))
        xpos += mw * c
    ypos += sbh
    
    ''' Commented for strategi
    '''
    bgroup.add(elem.text(
                    txcode,
                    insert = (cx, ypos + fh),
                    fill='black',
                    #style='text-indent:10;text-align:center;',
                    font_weight='bold',
                    font_size=fh,
    # LETTER SPACING = Work on Inkscape But Weird on COrelDraw
                    #letter_spacing='10',
                    text_anchor='middle',
                    font_family='Times New Roman, Times'
                    ))
    '''
    for ps , ch in textAlign(txcode,(cx, ypos + fh), fh, sbw * 4 / 5, 50):
        bgroup.add(p.text(
                    ch,
                    insert = ps,
                    fill='black',
                    font_weight='bold',
                    font_size=fh,
                    text_anchor='middle',
                    font_family='Times New Roman, Times'
                    ))
    
    
    '''
    translate = "translate({} {})".format(pos[0]-cx, pos[1]-cy)
    rotate = "rotate({} {} {})".format(rot, cx, cy)
    elem.add(elem.use('#' + txcode,
                insert = (0,0),
                #transform="translate({} {}),rotate({} {} {})".format(pos[0]-sh, pos[1]+sw, rot, cx, cy) 
                transform= ','.join([translate,rotate]) 
                ))
    #p.save()
def bs4_simplify(lang, name):
    from bs4 import BeautifulSoup
    souvg = BeautifulSoup(lang, 'xml')
    use_attr = [ x['transform'] for x in souvg.find_all('use') ]
    for x in souvg.find_all('use'):
        x.decompose()
    g = souvg.defs.find_all('g')
    for i, att in zip(g, use_attr):
        i['transform']=att
        souvg.svg.insert(0, i)
    souvg.defs.decompose()
    with open(name, 'w') as ot:
        ot.write(souvg.prettify())

def a3p_make(codes, bsz=(33, 14), init_pos=(16.703, 461.324), offsets=(63.6, 95), rotation = 90):
    p = None
    col, row = 0, 0
    xsize = [ px(x) for x in bsz ]
    offsets = [px(x) for x in offsets]
    xpos = [px(n) for n in init_pos]
    for c in codes:
        if col == 0 and row == 0:
            p = createPage("{} - {}".format(c, codes[codes.index(c) + 24]))
        pos = xpos[0] + (offsets[0] * col), xpos[1] - ( offsets[1] * row ) 
        addBarcode(p, c, xsize , (pos[0],pos[1]), rotation)
        col += 1
        if col > 4:
            col = 0
            row += 1
            if row > 4:
                row = 0
                bs4_simplify(p.tostring(), p.filename)
        
        
if __name__ == "__main__":
    cds = [ "MRD10{:>04d}".format(x) for x in range(1001, 1026) ]
    a3p_make(cds,rotation=90)
    