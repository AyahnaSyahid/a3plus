#Project Description
    
    Project pengembangan Automator Barcode :
    - Sebagai alat bantu dalam aplikasi design seperti CorelDraw
    
->  LIBRARY:
    svgwrite                : Simpan file Barcode sebagai SVG file
    python-barcode          : Mendapatkan pattern Barcode 
    
    
->  KNOWN PROBLEM:
    • #1 Tidak Konsisten nya Ukuran
          SVG dalam Spesifikasinya menggunakan 96dpi, berbeda dengan
      printing yang menggunakan 300dpi, jadi mungkin semua lib yang  
      terlibat dengan SVG file juga menerapkan spesifikasi tsb
        -> 300 / 96  = 3.125
        -> 96  / 300 = 0.32

### STATUS ###

    • 11/06/2020
        Script sudah dapat di pakai dengan, namun seperti disebutkan
    diatas, Ukuran metrik dan font masih belum bisa di prediksi
    
    Cara pemanggilan :
        python3 bc.py [argument]
            Menghasilkan file barcode 'argument' (Gs1_128) dengan extensi SVG
    
