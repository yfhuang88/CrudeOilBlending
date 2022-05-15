# CrudeOilBlending

## Description
Estimating the distillation profile of crude oil mixtures based on the distillation profiles of different crude oil streams. 

## Approach
Distillation profile of selected crude oil streams found on CrudeMonitor.ca are modelled independently through polynomial regression. A polynomial function (f) with temperature as input and percent mass recovered as output is fitted for each crude oil stream. 

The distillation profile of a mixture with i crude oil stream is calculated using the below equation, where mi is the mass fraction of crude oil stream i. <br />
![equation](https://latex.codecogs.com/svg.image?\bg{white}\textit{f}_{mix}&space;=&space;\sum&space;\textit{m}_{i}\textit{f}_{i})

## Assumption
It is assumed that the enthalpy of mixing is negligible, and the molecules interact in a similar manner in original and mixed crude oil streams. Based on these assumptions, the specific heat and enthalpy of vaporization of the mixture can be approximated using the weighted average of feeder streams. <br />
![equation](https://latex.codecogs.com/svg.image?\bg{white}\textit{C}_{p,&space;mix}&space;=&space;\textit{m}_{i}\textit{C}_{p,&space;i}) <br />
![equation](https://latex.codecogs.com/svg.image?\bg{white}\Delta&space;\textsl{H}_{vap,&space;mix}&space;=\sum&space;&space;\textit{m}_{i}\Delta&space;\textsl{H}_{vap,&space;i}) <br />
Although the specific heat and enthalpy of vaporization is not directly available for the feeder streams, it is presumed that the distillation profile of feeder streams implicitly contains this information. Therefore, the weighted average of distillation profile functions of feeder stream is used to estimate that of the mixture. 

## Running the code 
To install to code, the user needs to be in the top directory of the code folder and execute the following command 
```bash
pip install -e .\
```
Then run the code. Create a new directory and make sure you create a folder called data/. Then run the following command and an example for input.json file will be provided in the scripts folder. 
```bash
mkdir -p NewDirectory
cd NewDirectory
mkdir -p data
python -m CrudeOilBlending input.json
```
The sample input.json file is provided below. Feeder oil stream and volume can be updated as desired. 
```bash
"Oil" : ["Rainbow", "Bow River North", "Fosterton"],
"Volume" : [100, 50, 50],
"numfiles" : 10,
"page_url" : "https://www.crudemonitor.ca/crudes/index.php?acr=",
"degree"   : 4
```
Note that feeder oil stream can only be chosen from the streams included in the MapFromRealNameToWebsiteName dictionary in main.py. To include a new stream, add its full name and website name to the dictionary. 

### Example output
The output includes a distillation profile plot like the following
![mixture_profile](/scripts/"Rainbow_Bow River North.txt")
as well as a .txt file with the plotted data. 