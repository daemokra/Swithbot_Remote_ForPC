from .requestsutil import RequestsUtil
from .device import *

class SwitchbotRemote:
    def __init__(self, token, secret, nonce ,version, host='https://api.switch-bot.com') -> None:
        self._r = RequestsUtil(token=token,secret=secret,nonce=nonce,version=version, host=host)

    def get_devices_list(self):
        return self._r.get_request('devices')['body']

    def get_physical_devices(self):
        return self.get_devices_list()['deviceList']

    def get_virtual_devices(self):
        return self.get_devices_list()['infraredRemoteList']

    def set_api_settings(self):
        pass

    def get_airconditioners(self) -> AirConditioner:
        acs = []
        for device in self.get_virtual_devices():
            if  device['remoteType'] == 'Air Conditioner':
                acs.append(AirConditioner(device['deviceId'], device['deviceName'], device['remoteType'], device['hubDeviceId'],self._r))
        return acs

    def get_hubminis(self) -> HubMini:
        d = []
        for device in self.get_physical_devices():
            if  device['deviceType'] == 'Hub Mini':
                d.append(HubMini(device['deviceId'], device['deviceName'], device['deviceType'], device['hubDeviceId'],self._r))
        return d
