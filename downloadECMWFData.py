import cdsapi
import shutil
import xarray as xr
# import os
# os.environ['PROJ_LIB'] = '/Users/mb/anaconda3/envs/worklab/share/proj'
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap
import numpy as np

## Creating file cdsapirc
cdsFile = os.path.join(os.path.expanduser('~'),'.cdsapirc')
isFile = os.path.isfile(cdsFile)

while isFile != True:
    print("""File .cdsapirc belum tersedia.
Pastikan Anda telah memiliki akun di 
https://cds.climate.copernicus.eu/
          """)
    UID = input("Silakan masukkan UID Anda: ")
    APIkey = input("Silakan masukan API Key Anda: ")
    f = open(".cdsapirc","w")
    f.write("url: https://cds.climate.copernicus.eu/api/v2 \nkey: "+UID+":"+APIkey+"")
    f.close()
    shutil.move(".cdsapirc", os.path.expanduser('~'))
    break

print("File .cdsapirc telah tersedia.")

### Defining Functions
def inputLevel():
    inLevel = int(input("Level: "))
    
    if (inLevel == 1):
        return 'reanalysis-era5-single-levels'
    
    elif (inLevel == 2):
        return 'reanalysis-era5-pressure-levels'
   
    else:
        print("Maaf, pilihan anda tidak tersedia. Silakan input kembali.")
        return inputLevel()

  
def inputVarSing():
    listVarSing = ['10m_u_component_of_wind', '10m_v_component_of_wind', 
            '2m_temperature', 'mean_sea_level_pressure', 'total_precipitation',
            'sea_surface_temperature', 'significant_height_of_combined_wind_waves_and_swell', 'mean_wave_direction' 
            ]
    
    if (inVarSing == 1):
        return [listVarSing[0],listVarSing[1]]

    elif (inVarSing > 1 and inVarSing<6):
        return listVarSing[inVarSing]
    
    elif (inVarSing == 6):
        return [listVarSing[6],listVarSing[7]]
    
    else:
        print("Maaf, pilihan anda tidak tersedia. Silakan input kembali.")
        return inputVarSing()
    
def codeVarSing():
    listVarSingCode = ['wnd','t2m','msl','tp','sst','wve']
    
    if (inVarSing == 1):
        return listVarSingCode[0]

    elif (inVarSing > 1 and inVarSing<=6):
        return listVarSingCode[inVarSing-1]

def nameVarSing():
    listVarSingName = ['angin 10 m','temperatur permukaan','tekanan udara','curah hujan','suhu permukaan laut','gelombang laut']
    
    if (inVarSing == 1):
        return listVarSingName[0]

    elif (inVarSing > 1 and inVarSing<=6):
        return listVarSingName[inVarSing-1]

def inputVarPres():
    listVarPres = ['u_component_of_wind', 'v_component_of_wind',
               'temperature', 'relative_humidity', 'specific_humidity',
               'divergence', 'potential_vorticity']
    
    if (inVarPres == 1):
        return [listVarPres[0],listVarPres[1]]

    elif (inVarPres > 1 and inVarPres<=6):
        return listVarPres[inVarPres]
    
    else:
        print("Maaf, pilihan anda tidak tersedia. Silakan input kembali.")
        return inputVarPres()

def codeVarPres():
    listVarPresCode = ['wnd','t','r','q','d','pv']
    
    if (inVarPres == 1):
        return listVarPresCode[0]

    elif (inVarPres > 1 and inVarPres<=6):
        return listVarPresCode[inVarPres-1]

def nameVarPres():
    listVarPresName = ['angin','temperatur','kelembapan relatif','kelembapan spesifik','divergensi','vortisitas']
    
    if (inVarPres == 1):
        return listVarPresName[0]

    elif (inVarPres > 1 and inVarPres<=6):
        return listVarPresName[inVarPres-1]
        
def downloadData():
    c = cdsapi.Client()
    c.retrieve(
        level,
        {
            'product_type': 'reanalysis',
            'format': 'netcdf',
            'variable': var,
            'pressure_level': pres,
            'year': [yStart, yEnd],
            'month': [mStart, mEnd],
            'day': [
                '01', '02', '03',
                '04', '05', '06',
                '07', '08', '09',
                '10', '11', '12',
                '13', '14', '15',
                '16', '17', '18',
                '19', '20', '21',
                '22', '23', '24',
                '25', '26', '27',
                '28', '29', '30',
                '31',
            ],
            'time': [
            '00:00'
            ],
            'area': [
                north, west, south,
                east,
            ],
        },
        output_filename)
    return output_filename

def varsSing(DS):
    var = list(DS.keys())[0]
    vars = DS[var]
    if (inVarSing == 1):
        u10 = DS[list(DS.keys())[0]]
        v10 = DS[list(DS.keys())[1]]
        wnd = (u10**2+v10**2)**0.5
        vars = wnd
        vars.attrs["long_name"] = "10m Wind speed"

    elif (inVarSing == 2):
        vars = vars-273.15
        vars.attrs["long_name"] = "Air temperature"

    elif (inVarSing == 3):
        vars = vars/1e2
        vars.attrs["long_name"] = "Sea level pressure"

    elif (inVarSing == 4):
        vars = vars*1e3
        vars = vars.where(vars>5)
        vars.attrs["long_name"] = "Total precipitation"

    elif (inVarSing == 5):
        vars = vars-273.15
        vars.attrs["long_name"] = "Sea surface temperature"

    elif (inVarSing == 6):
        vars = vars
        vars.attrs["long_name"] = "Significant wave height"
    return vars

def varsPres(DS):
    var = list(DS.keys())[0]
    vars = DS[var]
    if (inVarPres == 1):
        u = DS[list(DS.keys())[0]]
        v = DS[list(DS.keys())[1]]
        wnd = (u**2+v**2)**0.5
        vars = wnd
        vars.attrs["long_name"] = "Wind speed"

    elif (inVarPres == 2):
        vars = vars-273.15
        vars.attrs["long_name"] = "Temperature"

    elif (inVarPres == 3):
        vars = vars
        vars.attrs["long_name"] = "Relative humidity"

    elif (inVarPres == 4):
        vars = vars*1e3
        vars.attrs["long_name"] = "Specific humidity"

    elif (inVarPres == 5):
        vars = vars*1e5
        vars.attrs["long_name"] = "Divergence"

    elif (inVarPres == 6):
        vars = vars
        vars.attrs["long_name"] = "Potential vorticity"
    return vars

def varsAttrSingUnit():
    listVarSingUnit = ["m/s", "°C", "hPa","mm", "°C", "m"]
    return listVarSingUnit[inVarSing-1]

def varsAttrPresUnit():
    listVarPresUnit = ["m/s", "°C", "%", "g/g", "× 10¯⁵ s¯¹", "K.m²/kg.s"]
    return listVarPresUnit[inVarPres-1]

def varsSingMap():
    listVarSingMap = ["Blues", "RdYlBu_r", "GnBu", "BuPu", "RdYlBu_r", "YlGnBu"]
    return listVarSingMap[inVarSing-1]

def varsPresMap():
    listVarPresMap = ["Blues", "RdYlBu_r", "BuGn", "winter_r", "PiYG", "PuOr"]
    return listVarPresMap[inVarPres-1]

### Main Program   
print("""
=============================================
Anda akan mengunduh data ERA5 daily
reanalysis data dari European Centre
for Medium-Range Weather Forecast (ECMWF).

Silakan pilih jenis level data yang ada inginkan!
1. Single level (Permukaan)
2. Pressure level (Kolom vertikal)
      """)

level = inputLevel()

if (level == 'reanalysis-era5-single-levels'):
    # Variabel
    print("""
Silakan pilih parameter yang akan diunduh!
1. Angin 10m 
2. Suhu udara
3. Tekanan udara
4. Curah hujan
5. Suhu permukaan laut
6. Gelombang laut
          """)
    inVarSing = int(input("Parameter: "))
    var = inputVarSing()
    cVar = codeVarSing()
    nVar = nameVarSing()
    pres = ''

else:
    # Variabel
    print("""
Silakan pilih parameter yang akan diunduh!
1. Angin 
2. Suhu vertikal
3. Kelembapan relatif
4. Kelembapan spesifik
5. Divergensi
6. Vortisitas potensial
          """)
    inVarPres = int(input("Parameter: "))
    var = inputVarPres()
    cVar = codeVarPres()
    nVar = nameVarPres()
    pres = input("\nSilakan tentukan ketinggian data Anda! ")
    nVar = str(nVar)+" pada ketinggian "+str(pres)+" mb"
    VarUnit = varsAttrPresUnit()
    VarMap = varsPresMap()

print("""Default domain Indonesia
- Utara = 20
- Selatan = -20
- Barat = 80
- Timur = 160
    """)

print("\nSilakan tentukan domain pengunduhan data!")
north = input("Utara: ")
south = input("Selatan: ")
west = input("Barat: ")
east = input("Timur: ")

# Rentang waktu
print("\nSilakan tentukan waktu awal pengunduhan data!")
yStart = input("Tahun: ")
mStart = input("Bulan: ")
# dStart = input("Hari: ")

print("\nSilakan tentukan waktu akhir pengunduhan data!")
yEnd = input("Tahun: ")
mEnd = input("Bulan: ")
# dEnd = input("Hari: ")

# Waktu terbaru
# startDate=$(date --date "-1 days"  +"%Y-%m-%d")" 00:00:00"
# endDate=$(date --date "-1 days"  +"%Y-%m-%d")" 00:00:00"

# Konfirmasi pengunduhan data
print("""
Anda akan mengunduh data""",nVar,"""dengan informasi sebagai berikut
Batas utara: """,str(north),"""
Batas selatan: """,str(south),"""
Batas barat: """,str(west),"""
Batas timur: """,str(east),"""
Waktu awal: """,str(yStart)+"-"+str(mStart),"""
Waktu akhir: """,str(yEnd)+"-"+str(mEnd),"""
""")

confirm = input("Lanjutkan pengunduhan data? [y/n] ")
while (confirm == 'y'):
    output_filename  = './data/era5_'+cVar+pres+'.daily.'+yStart+mStart+yEnd+mEnd+'.nc'
    ## Downloading Data
    downloadData()
    print("Pengunduhan data",nVar,"selesai!")
    print("Nama file data Anda adalah era5_"+cVar+pres+".daily."+yStart+mStart+yEnd+mEnd+".nc")
    break

confirm = input("Lanjutkan pengecekan data? [y/n]")
while (confirm == 'y'):
    ## Checking Data
    print("Nama File : era5_"+cVar+pres+".daily."+yStart+mStart+yEnd+mEnd+".nc")
    DS = xr.open_dataset(output_filename)
    print(DS)
    break

confirm = input("Lanjutkan pengolahan data? [y/n]")
while (confirm == 'y'):
    ## Plotting Data
    plt.rcParams["font.family"] = "Arial"
    plt.rcParams["font.size"] = 14

    if (level == 'reanalysis-era5-single-levels'):
        vars = varsSing(DS)
        VarUnit = varsAttrSingUnit()
        VarMap = varsSingMap()

    elif (level == 'reanalysis-era5-pressure-levels'):
        vars = varsPres(DS)
        VarUnit = varsAttrPresUnit()
        VarMap = varsPresMap()
        
    vars.attrs["units"] = VarUnit

    # Domain
    lats = DS['latitude']
    lons = DS['longitude']
    times = DS['time']

    lat_min = lats.min()
    lat_max = lats.max()
    lon_min = lons.min()
    lon_max = lons.max()

    # Rentang waktu
    time_min = times.min()
    time_max = times.max()

    map_config = {
        "projection": "merc",
        "llcrnrlat": lat_min,
        "llcrnrlon": lon_min,
        "urcrnrlat": lat_max,
        "urcrnrlon": lon_max,
        "resolution": 'i',
        "epsg": 4326
    }
    for t in range(0,len(DS.time)):
        plt.figure(figsize=(16, 8))
        map = Basemap(**map_config)
        map.drawcountries(linewidth=1, color='black')
        map.drawcoastlines(linewidth=1, color='black')
        map.drawmeridians(np.arange(lon_min,lon_max,10),labels=[0,0,0,1])
        map.drawparallels(np.arange(lat_min,lat_max,10),labels=[1,0,0,0])

        vars.sel(time=times[t]).plot(
            cmap=plt.cm.get_cmap(VarMap,24),
            vmin=vars.mean()-4*vars.std(),vmax=vars.mean()+4*vars.std(),
            )

        if (level == 'reanalysis-era5-single-levels' and inVarSing == 1):
            quiver = DS.isel(time=t,longitude=slice(None, None, 4),latitude=slice(None, None, 4)).plot.quiver(x='longitude', y='latitude', u='u10', v='v10', add_guide = False)
        
        elif (level == 'reanalysis-era5-single-levels' and inVarSing == 6):
            swh = DS[list(DS.keys())[0]]
            mwd = DS[list(DS.keys())[1]]
            wvu = xr.DataArray(swh*(np.sin(np.pi*(mwd/180))), name='wvu')
            wvv = xr.DataArray(-swh*(np.cos(np.pi*(mwd/180))), name='wvv')
            DSW = xr.merge([wvu, wvv], compat="identical")
            quiver = DSW.isel(time=t,longitude=slice(None, None, 4),latitude=slice(None, None, 4)).plot.quiver(x='longitude', y='latitude', u='wvu', v='wvv', add_guide = False)

        elif (level == 'reanalysis-era5-pressure-levels' and inVarPres == 1):
            quiver = DS.isel(time=t,longitude=slice(None, None, 4),latitude=slice(None, None, 4)).plot.quiver(x='longitude', y='latitude', u='u', v='v', add_guide = False)
        

        xlabel = 'Longitude'
        ylabel = 'Latitude'
        xlabelpad = 30
        ylabelpad = 30
        plt.xlabel(xlabel, labelpad=xlabelpad)
        plt.ylabel(ylabel, labelpad=ylabelpad)
        
        timestep = np.datetime_as_string(times[t],'h')
        plt.title(timestep)

        output_file = "./out/" + cVar + pres +"_"+ (timestep.replace('-','')) + ".png"
        plt.savefig(output_file)
        plt.show()
  
    break