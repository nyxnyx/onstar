# About
Purpose of this project is to create atleast home-assitant component for getting information about your opel or
other OnStar enabled car into home-assistant. 

URL investigated: https://gspweb.eur.onstar.com

Login with email and password for OnStar account / also you need PIN for localization.

# Status
Currently we can get information for OnStar about car like Diagnostics and localization.
This is prove of concept - idea is to add as custom_component to home-assistant providing sensor.py for sensor and switch.py for switches (like key fob, syrene).

# How to get it working?
Install python >=3.5 (instructions on the internet)

Check if your python has proper version:
```
python3 --version
```
```
python --version
```
If in both cases you get version >=3.5 - you can use python or python3.
If python gives you version 2.7 and python3 version 3.X - use python3 and pip3 instead.

Install pip (on debian systems ``apt install python3 pip3``)

With pip3 install aiohttp library by:
```
pip3 install aiohttp
```


