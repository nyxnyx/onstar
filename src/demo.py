import aiohttp
import asyncio
import json
from collections import namedtuple
import getpass

print("This demo will connect to: https://gsp.eur.onstar.com/\n")
print("Before trying - ensure you have access by login in above site\n")
print("\nProvide credentials\n")
username = input("Username/email: ")
password = getpass.getpass("Password: ")
gm_pin = getpass.getpass("PIN for localization: ")


def _json_object_hook(d): return namedtuple('X', d.keys())(*d.values())

def dumpJson(parsed):
    print(json.dumps(parsed, sort_keys=True, indent=4))

@asyncio.coroutine
def fetch(loop):
    payload = {'username': username, 'password': password, 'roleCode': 'driver', 'place': ''}

    session = aiohttp.ClientSession(loop=loop) 
    response = yield from session.post('https://gsp.eur.onstar.com/gspserver/services/admin/login.json', data=payload) 
    ret = yield from response.text()
        
    return json.loads(ret, object_hook=lambda d: namedtuple('X', d.keys())(*d.values())), session

@asyncio.coroutine
def getLoginInfo(token, session):
    header = {'X-GM-token': token}

    ret = yield from session.get('https://gsp.eur.onstar.com/gspserver/services/admin/getLoginInfo.json', headers=header)
    return ret

@asyncio.coroutine
def getDiagnostics(token, session, vehicleId):
    header = {'X-GM-token': token}
    payload = {'vehicleId': vehicleId}
    ret = yield from session.get('https://gsp.eur.onstar.com/gspserver/services/vehicle/getDiagnosticsReport.json', params=payload, headers = header)
    return ret

@asyncio.coroutine
def locateCar(token, pin, session, vehicleId):
    header = {'X-GM-token': token, 'X-GM-pincode': pin}
    payload = {'vehicleId': vehicleId}
    ret = yield from session.post('https://gsp.eur.onstar.com/gspserver/services/vehicle/performLocationHistoryQuery.json', data=payload, headers = header)
    return ret




@asyncio.coroutine
def main(loop):
    data,session = ((yield from fetch(loop)))
    print("Data from fetch - looking for token\n")
    print(data)
    token = data.results[0].token
    print("Found token: ")
    print(token)
    print("\n\n")
    data  = (yield from getLoginInfo(token,session))
    object = yield from data.text()
    print("Getting login info data, looking for first vehicleId:\n")
    dumpJson(json.loads(object) )
    object = json.loads(object, object_hook=lambda d: namedtuple('X', d.keys())(*d.values()))
    vehicleId = object.results[0].vehicles[0].vehicle.vehicleId
    print("Found vehicleId: ")
    print(vehicleId)
    print ("\n")
    diag = (yield from getDiagnostics(token, session, vehicleId))
    vehDiag = yield from diag.text()
    print("Getting diagnostics information:\n")
    dumpJson(json.loads(vehDiag))
    print("Getting localization:\n")
    locate = (yield from locateCar(token, gm_pin, session, vehicleId) )
    locate = yield from locate.text()
    dumpJson(json.loads(locate))
    print("Done for now")
    session.close()

loop = asyncio.get_event_loop()
loop.run_until_complete(main(loop))
