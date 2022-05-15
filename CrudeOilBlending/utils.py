from selenium import webdriver
from selenium.webdriver.support.ui import Select
import pandas as pd
import os
import xlrd
import numpy as np
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
import time 

def GetCrudeProfile(stream:list, page_url:str, download_path:str,  num_files=20, rm_files=False):
    '''
    Parameters
    ----------
    stream : list
        List of abbreviations of desired crude oil stream type.
    page_url : str
        Link to the distillation profiles.
    download_path : str
        Directory to save the downloaded files.
    num_files : TYPE, optional
        Number of distillation profiles to download. The default is 20.
    rm_files : TYPE, optional
        Remove files in the download directory. The default is False.

    Returns
    -------
    None.

    '''
    # remove all files from download_path
    if rm_files:
        print("WARNING: Removing all files in {}".format(download_path))
        files = [f for f in os.listdir(download_path) if f.endswith("xls") or f.endswith("xlsx")] 
        for f in files:
            os.remove(download_path + f)
    
    # Add download preference 
    chromeOptions = webdriver.ChromeOptions()
    prefs = {"download.default_directory" : download_path}
    chromeOptions.add_experimental_option("prefs",prefs)
    
    # declare chrome driver 
    driver = webdriver.Chrome(ChromeDriverManager().install(), options=chromeOptions)
    length = len(stream)
    
    for i in range(length):
        driver.get(page_url+stream[i])
        ele = driver.find_element(by=By.XPATH,  value="//select[@id='haverlySelect']")
        sel = Select(ele)
        for j in range(0, num_files+1):
            sel.select_by_index(j)
            time.sleep(1)


def ProcessCrudeOilData(data_path:str):
    '''
    Parameters
    ----------
    data_path : str
        Path where the distillation profiles are stored.

    Returns
    -------
    dic : TYPE
        Holds the property data (Nfile, N, d) for each curde oil type.

    '''

    PROPERTY_LIST =  ['GRAV','SUL','V','NI','MCRT']  
    MapCrudeOilNameToProperties = {}
    files = [f for f in os.listdir(data_path) if f.endswith("xls") or f.endswith("xlsx")]
    
    for f in files:
        # Read pandas
        workbook = xlrd.open_workbook_xls(data_path+f, ignore_workbook_corruption=True)
        
        # Get stream name
        info = pd.read_excel(workbook, sheet_name='Information', header=None, index_col=0, usecols='A,B').T
        stream = info['Crude Name'].to_numpy()[0]
        
        #Get stream properties
        prop = pd.read_excel(workbook, sheet_name='Whole Crude', header=None, index_col=0, usecols='A,C').T
        prop = prop[PROPERTY_LIST]
        
        # Get distillation profile
        # Column 0: Yield, 1: Temp, 2: GRAV, 3:SUL, 4: V, 5: NI, 6: MCRT
        dist = pd.read_excel(workbook, sheet_name='Cum. Yield', names=['Yield', 'Temp'], header=None, usecols='A,B')
        dist['Yield'] = pd.to_numeric(dist['Yield'].str.replace('P',''))
        
        # Combine distillation profile and stream properties into one array
        dist_arr = dist.to_numpy()
        prop_arr = np.repeat(prop.to_numpy(), np.shape(dist_arr)[0], axis=0)
        data_arr = np.hstack((dist_arr, prop_arr))
        
        if stream in MapCrudeOilNameToProperties:
            MapCrudeOilNameToProperties[stream].append(data_arr)
        else:
            MapCrudeOilNameToProperties[stream] = [data_arr]
    
    dic = {a : np.array(MapCrudeOilNameToProperties[a]) for a in MapCrudeOilNameToProperties}

    return dic


def CalculatedAverageTemperature(dic:dict):
    """

    Parameters
    ----------
    dic : dict
        Holds property data (Nfile, N,d ) for each crude oil type. 

    Returns
    -------
    AvgTemp : dict
        Maps names of crude oil streams to [Average Temperature, Composition (% mass recovered)] data 

    """    
    # Create dictionary Oil Stream - Average Vaporization Temp
    DataDictionary = {}
    
    for name in dic:
        # of shape (Nfile,N,d) 
        data = dic[name]
        
        # extract out temperature (Nfile, N, 1)
        temperature = data[:,:,1:2]
        composition = data[:,:,0:1]
        
        # check nan mean
        temperatureMean = np.nanmean(temperature,axis=0)
        compositionMean = np.nanmean(composition,axis=0)
        
        # get rid of nan 
        index = ~np.isnan(temperatureMean)
        temperatureMean = temperatureMean[index]
        compositionMean = compositionMean[index]
        
        # hstack composition and tempertuare mean (N,1)
        d = np.vstack((temperatureMean, compositionMean)).T
        
        DataDictionary[name] = d
        
    # Return the average temperature needed to vaporize a stream based to different mass fractions (1*100)
    return DataDictionary

    
def GetAvgOilProperty(dic:dict, OilProperty:list):
    """
    
    Parameters
    ----------
    dic : dict
        Holds property data (Nfile, N,d ) for each crude oil type. 

    OilProperty: 
        Average oil property to be calculated.
        'GRAV': API Gravity, 'SUL': Sulfer %wt, 'V': Vanadium mg/kg, 'NI': Nickel mg/kg, 'MCRT': MCR wt%

    Returns
    -------
    OilProp : dict
        Holds the average of selected oil propery for each crude oil stream

    """
    PROPERTY_DICT =  {'GRAV': 2,'SUL': 3,'V': 4,'NI': 5,'MCRT': 6}
    column = PROPERTY_DICT[OilProperty]
    
    OilNames = list(dic.keys())
    length = len(OilNames)
    
    OilProp = {}
    
    for i in range(length): 
        data = dic[OilNames[i]]
        data = np.concatenate(data)
        prop = data[:, column].mean()
        OilProp[OilNames[i]] = prop
    
    return OilProp

def GetMixtureProfile(OilTypes:list, Volumes:list, GRAV:dict, polyparams:dict):
    """
    Parameters
    ----------
    OilTypes : list
        List of crude oil to be mixed (full text)

    Volume : list
        List of volume of each type of crude oil to be mixed
    
    GRAV : dict
        Dictionary hodling the average API Gravity of each crude oil stream
    
    Polyparams : dict
        Dictionary holding the polynomial coefficients fitted for the Temperature (X) Percent Mass Recovery (y) curve for each crude oil stream type

    """
    assert len(OilTypes) == len(Volumes), "Input error" 

    # m1, m2 , .. mk
    mass = []
    for (i,t) in enumerate(OilTypes):
        g = GRAV[t]
        mass.append(Volumes[i] * 141.5/(g+131.5)*1000) 
    mass = np.array(mass)

    # weight percentage n_i = w_i / \sum_{i} w_{i}
    weights = mass / mass.sum()

    # weight average of the parameters
    params = []
    pureEstimate = []
    T = np.linspace(30,750,100)
    for (i,t) in enumerate(OilTypes):
        params.append(polyparams[t]) 
        pureEstimate.append(np.poly1d(polyparams[t])(T))

    # N, num_deg
    params = np.concatenate(params,axis=0).reshape(len(OilTypes),-1)

    # weight average
    params = (params * weights[:,np.newaxis]).sum(axis=0)
    poly   = np.poly1d(params)


    return pureEstimate, poly(T), T