# crudeoilblending

## Description
Estimating the distillation profile of crude oil mixtures based on the distillation profiles of different crude oil streams. 

## Approach
Distillation profile of selected crude oil streams found on CrudeMonitor.ca are modelled independently through polynomial regression. A polynomial function (f) with temperature as input and percent mass recovered as output is fitted for each crude oil stream. 

The distillation profile of a mixture with i crude oil stream is calculated using the below equation, where mi is the mass fraction of crude oil stream i. <br />
![equation](https://latex.codecogs.com/svg.image?\bg{white}\textit{f}_{mix}&space;=&space;\sum&space;\textit{m}_{i}\textit{f}_{i})

## Assumption
It is assumed that the specific heat of the mixture is the sum of the specific heat of each crude oil stream multiplied by mass fraction, and the enthalpy of vaporization of the mixture is the sum of the enthalpy of vaporization of each crude oil stream multiplied by mass fraction, as the following equations show. <br />
![equation](https://latex.codecogs.com/svg.image?\bg{white}\textit{C}_{p,&space;mix}&space;=&space;\textit{m}_{i}\textit{C}_{p,&space;i}) <br />
![equation](https://latex.codecogs.com/svg.image?\bg{white}\Delta&space;\textsl{H}_{vap,&space;mix}&space;=\sum&space;&space;\textit{m}_{i}\Delta&space;\textsl{H}_{vap,&space;i})

## Running the code 
To install to code, make sure you are in the top directory of the code folder and execute the following command 
```bash
python setup.py install
```
The run the code. Create a new directory and make sure you create a folder called data/. Then run the following command and an example for input.json file will be provided in the scripts folder. 
```bash
mkdir -p NewDirectory
cd NewDirectory
mkdir -p data
python -m CrudeOilBlending input.json
```
A portion of the input.json file is provided below, the user needs to change the oil blend, volume as well as the folder at which they want to store the data 


### Example output
An example of the output would look something like the following 
![mixture_3](/scripts/mixture_3.png)