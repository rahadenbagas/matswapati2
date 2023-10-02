#!/bin/bash
stty erase ^H

printf '
=============================================
Selamat datang di sistem MATSWAPATI!

MATSWAPATI - Marine and Atmospheric Data
Download and Processing Automation System
merupakan suatu sistem otomatisasi
berbasis linux dan bahasa pemrograman python
untuk mengunduh  dan mengolah data atmosfer
dan laut dari sumber terbuka Copernicus EU.
=============================================
(c) Hatmaja, 2022
'

printf '
\nSilakan pilih penyedia data
1. CMEMS (marine.copernicus.eu)
2. ERA5 (cds.climate.copernicus.eu)
' 

read -r -p "Penyedia data: " ansProv

case $ansProv in
    1)
      python downloadCMEMSData.py
      ;;

    2)
      python downloadECMWFData.py
      ;;
esac