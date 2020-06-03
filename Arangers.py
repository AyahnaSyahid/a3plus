# -*- coding: utf-8 -*-
"""
penyusun bb cetakan
--->>
    Panggil Script pada folder paling atas
    Case :
        Menyusun BB buku untuk dicetak
        
        susunan file sbb:
            Nama Konsumen/                      (Folder paling atas)
                Buku 1/
                    1.jpg
                    2.jpg
                    ...dst
                Buku 2/
                    1.jpg
                    2.jpg
                    ...dst
        output sbb:
            Nama Konsumen/                      (Folder paling atas)
                Buku 1/
                    HAL1.jpg
                    HAL2.jpg
                    ...
                Buku 2/
                    HAL1.jpg
                    HAL2.jpg
                    ...
        
        nantinya tinggal import masing2 halaman ke aplikasi CorelDraw
        Cheers !!
    
"""

import numpy as np
from math import ceil
from PIL import Image
from pathlib import Path
import os

# Path Checks
im_exists = lambda cp, x: (cp / (str(x) + '.jpg')).exists()

def mm_to_px(mm, dpi=450):
    """Milimeter to DPI Converter"""
    mul = dpi / 25.4
    return int(round(mm * mul))

def Arange(path):
    print("started")
    # Jumlah halaman diketahui dari jumlah gambar dalam folder
    jumlah_halaman = len([x for x in os.listdir(str(path)) if x.endswith('.jpg')])
    
    
    halaman_per_kertas = 2
    side = 2

    max_bb = halaman_per_kertas * ceil(jumlah_halaman / halaman_per_kertas)

    x = np.array(list(range(1, max_bb + 1)))
    x = x.reshape(side,int(max_bb/side))
    x[1] = np.flip(x[1],0)
    transp = np.flip(x,0).T

    for i in range(len(transp)):
        if i % 2 > 0:
            transp[i] = np.flip(transp[i],0)

    ltr = transp.tolist()

    for x in ltr:
        if im_exists(path, x[0]):
            leftImage = Image.open(path / (str(x[0]) + '.jpg'))
        else:
            leftImage = Image.new('L', (mm_to_px(215), mm_to_px(330)), 255)
            
        if im_exists(path, x[1]):
            rightImage = Image.open(path / (str(x[1]) + '.jpg'))
        else:
            rightImage = Image.new('L', (mm_to_px(215), mm_to_px(330)), 255)
        
        bg = Image.new('L', (mm_to_px(430), mm_to_px(330)), 255)
        bg.paste(leftImage,(0,0))
        bg.paste(rightImage,(mm_to_px(215),0))
        bg.save(path / "HAL{}.jpg".format(ltr.index(x)), dpi=(450,450),quality=80)
        print("done HAL{}.jpg".format(ltr.index(x)))
        
if __name__ == "__main__":
    # Thread & Queue digunakan untuk mempercepat proses 1 Directory 1 Thread
    from threading import Thread, Lock
    from queue import Queue
    
    
    que = Queue()
    threads = []
    
    
    def wrapper(q, tId):
        # Verbose
        print("Wrapper.started")
        while True:
            pth = q.get()
            if pth is None:
                break
            print("# {} on Process".format(threads[tId].name))
            Arange(pth)
            print("# {} done".format(threads[tId].name))
            q.task_done()
        
    for i in range(8):
        thr = Thread(target=wrapper, args=(que,len(threads)))
        thr.start()
        threads.append(thr)
        
    for x in [ Path(p) for p in os.listdir('.') if Path(p).is_dir()]:
        que.put(x)
    
    que.join()
    
    for i in range(len(threads)):
        que.put(None)
        
    for t in threads:
        print("Stoping Thread : \"{}\"".format(t.name))
        t.join()
    
    print("Tasks done....")