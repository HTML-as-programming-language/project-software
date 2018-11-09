import requests
from requests.exceptions import ConnectionError

instance = None


class Backend:
    def __init__(self, url, error_callback):
        self.url = url
        self.error_callback = error_callback

    def init(self, host):
        return self.send_request("/init", host)
        pass

    def send_request(self, endpoint, data=None):
        try:
            r = requests.post(self.url + endpoint, json=data)
            if r.status_code is not 200:
                print(r.text)
                self.error_callback(r.status_code)
                return None
            return r
        except ConnectionError as e:
            print(e)

            self.error_callback(type(e))
            return None

    def set_module_setting(self, module_id,
                           setting_key, data=None):
        return self.send_request(
                "/module/" + str(module_id) + "/setting/" + str(setting_key),
                data)

    def set_module_sensor_setting(self, module_id,
                                  sensor_id, setting_key, data=None):
        return self.send_request(
                "/module/" + str(module_id) + "/sensor/" +
                str(sensor_id) + "/" + str(setting_key),
                data)
