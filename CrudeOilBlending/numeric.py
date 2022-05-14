import numpy as np

def polyfit(dic, deg=3):
    """
    Parameters
    ----------
    dic : dict
        Holds property data (Nfile, N,d ) for each crude oil type. 
    
    Returns
    ----------
    fitDict : polynomial coefficients fitted for the Temperature (X) Percent Mass Recovery (y) curve for each crude oil stream type
    
    """
    fitDict = {}
    for n in dic:
        data = dic[n]
        
        fit = np.polyfit(data[:,0], data[:,1], deg=deg)
        
        fitDict[n] = fit
    
    return fitDict