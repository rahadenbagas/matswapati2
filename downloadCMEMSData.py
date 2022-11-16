import getpass
import motuclient
import matplotlib.pyplot as plt
import xarray as xr
import numpy as np
# import os
# os.environ['PROJ_LIB'] = '/Users/mb/anaconda3/envs/worklab/share/proj'
from mpl_toolkits.basemap import Basemap

class MotuOptions:
    def __init__(self, attrs: dict):
        super(MotuOptions, self).__setattr__("attrs", attrs)

    def __setattr__(self, k, v):
        self.attrs[k] = v

    def __getattr__(self, k):
        try:
            return self.attrs[k]
        except KeyError:
            return None

## Defining Function
def inputVar():
    listVar = ["uo", "vo", "thetao", "so", "zos"]
    
    if (inVar == 1):
        return listVar[0],listVar[1]

    elif (inVar > 1 and inVar<=4):
        return [listVar[inVar]]
   
    else:
        print("Maaf, pilihan anda tidak tersedia. Silakan input kembali.")
        return inputVar()

def nameVar():
    listVarName = ["arus laut permukaan", "suhu permukaan laut", "salinitas permukaan laut", "tinggi paras laut"]
    
    if (inVar == 1):
        return listVarName[0]

    elif (inVar > 1 and inVar<=4):
        return listVarName[inVar-1]

def codeVar():
    listVarcode = ["curro", "thetao", "so", "zos"]
    return listVarcode[inVar-1]

def downloadData():
    data_request_options_dict_manual = {
        "service_id": "GLOBAL_ANALYSIS_FORECAST_PHY_001_024-TDS",
        "product_id": "global-analysis-forecast-phy-001-024",
        "date_min": yStart+"-"+mStart+"-"+dStart+" 12:00:00",
        "date_max": yEnd+"-"+mEnd+"-"+dEnd+" 12:00:00",
        "longitude_min": west,
        "longitude_max": east,
        "latitude_min": south,
        "latitude_max": north,
        "depth_min": 0.493,
        "depth_max": 0.4942,
        "variable": Var,
        "motu": "https://nrt.cmems-du.eu/motu-web/Motu",
        "out_dir": ".",
        "out_name": output_filename,
        "auth_mode": "cas",
        "user": USERNAME,
        "pwd": PASSWORD
    }

    ## Request API
    motuclient.motu_api.execute_request(MotuOptions(data_request_options_dict_manual))

def varsAttrUnit():
    listVarUnit = ["m/s", "°C", "$10^{-3}$", "m"]
    return listVarUnit[inVar-1]

USERNAME = input('Enter your username: ')
PASSWORD = getpass.getpass('Enter your password: ')

# Variabel
print("""
Silakan pilih parameter yang akan diunduh!
1. Arus laut permukaan
2. Suhu permukaan laut
3. Salinitas permukaan laut
4. Tinggi muka laut
""")
inVar = int(input("Parameter: "))
Var = inputVar()
nVar = nameVar()
cVar = codeVar()

def varsMap():
    listVarMap = ["Blues", "RdYlBu_r", "GnBu", "RdBu_r"]
    return listVarMap[inVar-1]

# Input Domain
print("\nSilakan tentukan domain pengunduhan data!")
north = float(input("Utara: "))
south = float(input("Selatan: "))
west = float(input("Barat: "))
east = float(input("Timur: "))

# Input Rentang Waktu
print("\nSilakan tentukan waktu awal pengunduhan data!")
yStart = str(input("Tahun: "))
mStart = str(input("Bulan: "))
dStart = str(input("Hari: "))

print("\nSilakan tentukan waktu akhir pengunduhan data!")
yEnd = str(input("Tahun: "))
mEnd = str(input("Bulan: "))
dEnd = str(input("Hari: "))

## Membaca nama file
output_filename  = "./data/cmems_"+cVar+".daily."+yStart+mStart+yEnd+mEnd+".nc"

print("""
Anda akan mengunduh data""",nVar,"""dengan informasi sebagai berikut
Batas utara: """,str(north),"""
Batas selatan: """,str(south),"""
Batas barat: """,str(west),"""
Batas timur: """,str(east),"""
Waktu awal: """,str(yStart)+"-"+str(mStart)+"-"+str(dStart),"""
Waktu akhir: """,str(yEnd)+"-"+str(mEnd)+"-"+str(dEnd),"""
""")

confirm = input("Lanjutkan pengunduhan data? [y/n] ")
while (confirm == 'y'):
    ## Downloading Data
    downloadData()
    print("Pengunduhan data",nVar,"selesai!")
    print("Nama file data Anda adalah cmems_"+cVar+".daily."+yStart+mStart+yEnd+mEnd+".nc")
    break

confirm = input("Lanjutkan pengecekan data? [y/n]")
while (confirm == 'y'):
    ## Checking Data
    print("Nama File : cmems_"+cVar+".daily."+yStart+mStart+yEnd+mEnd+".nc")
    DS = xr.open_dataset(output_filename)

    print(DS)
    break

confirm = input("Lanjutkan pengolahan data? [y/n]")
while (confirm == 'y'):
    ## Plotting Data
    plt.rcParams["font.family"] = "Arial"
    plt.rcParams["font.size"] = 14
    
    var = list(DS.keys())[0]
    if (inVar == 1):
        vo = DS[list(DS.keys())[0]]
        uo = DS[list(DS.keys())[1]]
        curr = (uo**2+vo**2)**0.5
        vars = curr
        vars.attrs["long_name"] = "Current speed"
            
    else:
        vars = DS[var]

    ## Unit Variabel
    vars.attrs["units"] = varsAttrUnit()

    lats = DS[var]['latitude']
    lons = DS[var]['longitude']
    times = DS[var]['time']

    # Domain
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
        map.fillcontinents(color='white',lake_color='aqua')
        map.drawcoastlines(linewidth=1, color='black')
        map.drawmeridians(np.arange(lon_min,lon_max,10),labels=[0,0,0,1])
        map.drawparallels(np.arange(lat_min,lat_max,10),labels=[1,0,0,0])

        vars.sel(time=times[t]).plot(
            cmap=plt.cm.get_cmap(varsMap(),24),
            vmin=vars.min(),vmax=vars.max(),
            )
        
        if (inVar == 1):
            quiver = DS.isel(depth=0,time=t,longitude=slice(None, None, 12),latitude=slice(None, None, 12)).plot.quiver(x='longitude', y='latitude', u='uo', v='vo', add_guide = False)

        xlabel = 'Longitude'
        ylabel = 'Latitude'
        xlabelpad = 30
        ylabelpad = 30
        plt.xlabel(xlabel, labelpad=xlabelpad)
        plt.ylabel(ylabel, labelpad=ylabelpad)
        
        timestep = np.datetime_as_string(times[t],'h')
        plt.title(timestep)

        output_file = "./out/" + cVar +"_"+ (timestep.replace('-','')) + ".png"
        plt.savefig(output_file)
        plt.show()
    
    break