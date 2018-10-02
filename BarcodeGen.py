# -*- coding: utf-8 -*-
"""
By Cholize@Aksarajaya.tasik

"""
from time import sleep, time
from win32com import client
import win32gui
import win32api
import keyboard
#import ctypes


SendKey = lambda x : keyboard.press_and_release(x)
WinCheck = lambda : win32gui.FindWindow(None, "Barcode Wizard")
#VBA = ctypes.cdll.LoadLibrary(
#        "C:\Program Files\Common Files\Microsoft Shared\VBA\VBA7.1\VBE7.DLL")

CORELVERSION = "20"
BARCODEVERSION = "20"
ROTATE = 270
XOFFSET = 63.6
YOFFSET = 95.0
cver = CORELVERSION
bver = BARCODEVERSION

corel = client.gencache.EnsureDispatch("CorelDraw.Application." + cver)
document = corel.ActiveDocument
document.Unit = 3        #cdrMilimeters
document.ReferencePoint = 9        #cdrCenter

def draw_barcode(doc, code):
    barcode = doc.ActiveLayer.CreateOLEObject("CorelBarCode." + bver)
    hwnd = WinCheck()
    while not hwnd:
        sleep(0.1)
        hwnd = WinCheck()
    keyboard.press_and_release('alt')
    win32gui.SetForegroundWindow(hwnd)
    keyboard.write(code,0.05)
    SendKey("enter")
    sleep(0.1)
    SendKey("enter")
    sleep(0.1)
    SendKey("enter")
    while WinCheck():
        sleep(0.1)
    barcode.Cut()
    doc.ActiveLayer.PasteSpecial("Metafile")
    ret = doc.ActiveShape
    while ret is None:
        _ = input("Wait....")
    return ret

def Interactive_Barcode():
    import sys
    global document
    param_shape = document.ActiveShape
    if not param_shape:
        raise TypeError("Sepertinya tidak ada 1 format shape yang di pilih")
    initialPos = param_shape.GetPosition()
    initialSize = param_shape.GetSize()
    PREPEND = input("PREPEND TEXT = ")
    DIGIT = input("JUMLAH DIGIT = ")
    START = int(input("MULAI DARI = "))
    ENDS = int(input("SAMPAI = "))
    ##### MULAI
    process_start = time()
    CODE_LENGTH = ENDS - START + 1
    ROW = 1
    COL = 1
    for nth in range(CODE_LENGTH):
        if ROW > 5:
            ROW = 1
            COL += 1
        if COL > 5:
            COL = 1
            new_p = document.AddPages(1)
            new_p.Activate
            
        cod = PREPEND + str(START + nth).zfill(int(DIGIT))
        draw_shape = time()
        print(f"Generating {cod}", end="")
        shape = draw_barcode(document,cod)
        print(f"...done\n\ttime:{time()-draw_shape:.2f}"
               f"\telapsed:{time()-process_start:0.2f}\n")
        shape.Rotate(ROTATE)
        shape.SetSize(initialSize[0]-0.5, initialSize[1]-0.5)
        shape.SetPosition(initialPos[0] + (XOFFSET * (ROW - 1)),
                          initialPos[1] + (YOFFSET * (COL - 1)))

        ROW += 1
    took = time()-process_start
    print(f"took: {took:.2f}s {took/CODE_LENGTH:.2f}/code")
    corel = None
    document = None

        