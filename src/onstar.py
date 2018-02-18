"""
Class for connecting to OnStar service for getting status of your car

"""
import aiohttp
import asyncio
import json
from collections import namedtuple


class OnStar:
    """Base class for connection to OnStar service"""

    def __init__(self,username, password, pin, loop, dump_json = False):
        """Initiate connection and fetch login data"""
        self._username = username
        self._password = password
        self._pin = pin
        self._loop = loop
        self._dump_json = dump_json
        self._session = None
        self._token = None
        self._vehicle_id = None
        self._LOGIN_URL = 'https://gsp.eur.onstar.com/gspserver/services/admin/login.json'
        self._LOGINIFO_URL = 'https://gsp.eur.onstar.com/gspserver/services/admin/getLoginInfo.json'
        self._DIAGNOSTICS_URL = 'https://gsp.eur.onstar.com/gspserver/services/vehicle/getDiagnosticsReport.json'
        self._POSITION_URL = 'https://gsp.eur.onstar.com/gspserver/services/vehicle/performLocationHistoryQuery.json'
        
    
    def refresh(self):
        yield from self._login()
        yield from self._login_info()
        yield from self._diagnostics()
        yield from self._location()
        self._session.close()


    def dump_json(self, raw_string):
        if self._dump_json:
            print(json.dumps(json.loads(raw_string), sort_keys=True, indent=4, separators=(',', ': ')))


    @asyncio.coroutine
    def _login(self):
        payload = {'username': self._username, 'password': self._password, 'roleCode': 'driver', 'place': ''}

        self._session = aiohttp.ClientSession(loop=self._loop)

        response = yield from self._session.post(self._LOGIN_URL, data=payload)
        response_data = yield from response.text()
        self.dump_json(response_data)

        data = json.loads(response_data, object_hook=lambda d: namedtuple('X', d.keys())(*d.values()))
        self._login_object = data
        self._token = data.results[0].token
        self._header = {'X-GM-token': self._token}


    @asyncio.coroutine
    def _login_info(self):
        response = yield from self._session.get(self._LOGINIFO_URL, headers=self._header)
        login_info_data = yield from response.text()
        self.dump_json(login_info_data)
        self._login_info_object = json.loads(login_info_data, object_hook=lambda d: namedtuple('X', d.keys())(*d.values()))

        self._vehicle_id = self._login_info_object.results[0].vehicles[0].vehicle.vehicleId
        return self._login_info_object

    
    @asyncio.coroutine
    def _diagnostics(self):
        payload = {'vehicleId': self._vehicle_id}

        response = yield from self._session.get(self._DIAGNOSTICS_URL, params = payload, headers = self._header)
        diagnostics = yield from response.text()
        self.dump_json(diagnostics)
        diagnostics = diagnostics.replace('def','def_') #there is def field which must be renamed
        self._diagnostics_object = json.loads(diagnostics, object_hook=lambda d: namedtuple('X', d.keys())(*d.values()))
        return self._diagnostics_object


    @asyncio.coroutine
    def _location(self):
        payload = {'vehicleId': self._vehicle_id}
        header = {'X-GM-token': self._token, 'X-GM-pincode': self._pin}
        
        response = yield from self._session.post(self._POSITION_URL, params = payload, headers = header)
        location = yield from response.text()
        self.dump_json(location)
        self._location_object = json.loads(location, object_hook=lambda d: namedtuple('X', d.keys())(*d.values()))
        return self._location_object


    def get_login_info(self):
        return self._login_info_object


    def get_diagnostics(self):
        return self._diagnostics_object


    def get_location(self):
        return self._location_object



if  __name__ == "__main__":
    import getpass

    print("This demo will connect to: https://gsp.eur.onstar.com/\n")
    print("Before trying - ensure you have access by login in above site\n")
    print("\nProvide credentials\n")
    username = input("Username/email: ")
    password = getpass.getpass("Password: ")
    gm_pin = getpass.getpass("PIN for localization: ")

    loop = asyncio.get_event_loop()
    o = OnStar(username, password, gm_pin, loop, True)

    loop.run_until_complete(o.refresh())
