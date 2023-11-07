# NISR_Hackathon
this is a dashboard built with streamlit and plotly-express to visualize the amount of land used by crop
for the 2022 agricultural season in Rwanda
The dashboard uses the data in SAS 2022_Tables.xlsx excel file renamed to 2022_Tables.xlsx
###### file location  
data/2022_Tables.xlsx

<div>
<img src="data/Screenshot 2023-11-07 at 10.46.58 AM (1).png" width=250px height=180px>

## installation
```sh
git clone https://github.com/danjor667/NISR_Hackathon.git 
```
or download the zip and extract it
then 
```sh
cd NISR_Hackathon
```
create a virtual enviroment and install the requirements
```sh
python3 -m venv venv
source venv/bin/activate
pip install -r requirements
```
then run the app
```sh
streamlit run main.py
```
