# -*- coding: utf-8 -*-
"""
Script untuk menggabungkan 2 file yang terpisah (1 depan 1 belakang)
menjadi 1 file depan belakang
"""
from PyPDF2.merger import PdfFileMerger as Merger
from PyPDF2.merger import PdfFileReader as Reader
from PyPDF2.merger import PdfFileWriter as Writer

import numpy as np

def Collate(pdf1, pdf2, out="collated.pdf"):
    
    writer = Writer()
    books = Reader(pdf1), Reader(pdf2)
    blength = books[0].getNumPages()
    assert books[0].getNumPages() == books[1].getNumPages(), "Pages length mismatch"
    # make collate signature
    pages = [ [x, y ] for x in range(len(books)) for y in range(blength)]
    npages = np.asarray(pages).reshape(2,blength, 2).T\
        .reshape(2, blength * 2).T.tolist()
    for b, p in npages:
        writer.addPage(books[b].getPage(p))
    return writer