# About
Purpose of this project is to create atleast home-assitant component for getting information about your opel or
other OnStar enabled car into home-assistant. I'm not related to any of Onstar.com companies. If you are from Onstar.com company or represening it or other entities related to Onstar.com and reading this and want to access code - you have to pay me 1 000 000 EUR. So stop right now or pay to proceed. For further actions - please contanct me over github.

URL investigated: https://gspweb.eur.onstar.com (it was not reverse engineering work or decompilation just looking at my own web browser traffic which belong to me when I was logging into onstar.com website using my own account data which is paid service).

Login with email and password for OnStar account / also you need PIN for localization.

# Status
Currently we can get information for OnStar about car like Diagnostics and localization.
This is prove of concept - idea is to add as custom_component to home-assistant providing sensor.py for sensor and switch.py for switches (like key fob, syrene). 

# Noverber 2019 - maintarner needed
In November 2019 Onstar.com has closed my account. I'm unable to work on it. They don't like my work to give you opportunity to build useful scenarios with interactions with your car. My idea was to add ability to unlock car when you are outsite and your CCTV has detected that it is YOU and you want to open your car. But now - I've switched to another device which will allow me to do that without paying to companies like Onstar.com which are not going to give you flexibility in retrieving information where your car is. 
So if you want to maintain that code - please contact me directly.

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


