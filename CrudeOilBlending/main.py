from CrudeOilBlending.utils import *
import os 
from CrudeOilBlending.numeric import *
import matplotlib.pyplot as plt
import matplotlib as mpl
import json
import sys

#### Specifying plotting parameters ###
mpl.rcParams['lines.linewidth'] = 3
    #set font size for titles 
mpl.rcParams['axes.titlesize'] = 15
    #set font size for labels on axes
mpl.rcParams['axes.labelsize'] = 17
    #set size of numbers on x-axis
mpl.rcParams['xtick.labelsize'] = 15
    #set size of numbers on y-axis
mpl.rcParams['ytick.labelsize'] = 15
   #set size of ticks on x-axis
mpl.rcParams['xtick.major.size'] = 7
    #set size of ticks on y-axis
mpl.rcParams['ytick.major.size'] = 7
    #set size of markers
mpl.rcParams['lines.markersize'] = 5
    #set number of examples shown in legends
mpl.rcParams['legend.numpoints'] = 2
    #set the size of the legend
mpl.rcParams['legend.fontsize']=20
    #Set the color of the edges
mpl.rcParams["axes.edgecolor"] = "0.15"
mpl.rcParams["axes.linewidth"]  = 3
plt.rcParams["figure.figsize"] = (12,4)

MapFromRealNameToWebsiteName = {
    "Federated"    :    "FD",
    "Light Smiley"   :  "MSY", 
    "Peace"   :     "MPR", 
    "Pembina" :     "P", 
    "Secure Sask Light" :   "MSE", 
    "Mixed Sweet Blend" :   "MSW", 
    "Rainbow"   :   "RA", 
    "BC Light"  :   "BCL", 
    "Boundary Lake" :   "BDY", 
    "Koch Alberta"  :   "CAL", 
    "Moose Jaw Tops"    :   "MJT", 
    "Pembina Light Sour"    : "PLS", 
    "Hardisty Light"    :   "MBL", 
    "Medium Gibson Sour" :  "MGS", 
    "Midale"    :   "MSM", 
    "Peace Pipe Sour"   : "SPR", 
    "Bow River North"   : "BRN",
    "Bow River South"   : "BRS", 
    "Fosterton" :   "F", 
    "Lloyd Blend"   : "LLB", 
    "Access Western Blend"  :   "AWB", 
    "Borealis Heavy Blend"  :   "BHB", 
    "Canadian Natural High Tan":    "CNX"
}


def main():
    with open(sys.argv[1], "rb") as jsonfile:
        input =json.load(jsonfile)
    oiltype = input["Oil"]
    Volumes = input["Volume"]
    numfiles = input["numfiles"]
    page_url = input["page_url"]
    degree   = input["degree"]

    download_path = os.getcwd() + "\data\\"
    websiteName = []
    for t in oiltype:
        websiteName.append(MapFromRealNameToWebsiteName[t])

    # Obtain the data files 
    GetCrudeProfile(websiteName, page_url, download_path, num_files=numfiles, rm_files=True)

    # Create data dictionary (Key: Stream, Value: Distillation Profile & Stream Properties)
    dic = ProcessCrudeOilData(download_path)
    
    # Get average distillation temperature dictionary
    AvgTemp = CalculatedAverageTemperature(dic)
    
    # Obtain the polynomial fitting of (Temperature, COmposition)
    fitParameters = polyfit(AvgTemp,deg=degree)

    GRAV = GetAvgOilProperty(dic, 'GRAV')
    PureFrac , Frac, T = GetMixtureProfile(oiltype, Volumes, GRAV,fitParameters)

    ax = plt.figure(figsize=(10,8)).add_subplot()
    for (i,t) in enumerate(oiltype):
        ax.plot(T, PureFrac[i], label=t)
    ax.plot(T, Frac, label='Mixture')
    ax.legend(fontsize=15)
    plt.xlim([0,750])
    plt.ylim([0,100])
    plt.xlabel("Temperature (C)")
    plt.ylabel("Percent Mass Recovery")

    arr = np.column_stack((Frac, T))

    filename = '_'.join(oiltype)
    plt.savefig(filename+'.png')
    np.savetxt(filename+'.txt', arr, fmt='%f', header='Mass Recovered (%), Temperature (C)')