# crudeoilblending

## Description


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