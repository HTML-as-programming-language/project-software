import requests
from requests.exceptions import ConnectionError

instance = None

class Backend:
    def __init__(self, url, error_callback):
        self.url = url
        self.error_callback = error_callback

    def init(self):
        return self.send_request("/init", '"http://127.0.0.1:8081"')
        pass
        
    def send_request(self, endpoint, data=None):
        try:
            r = requests.post(self.url + endpoint, data)
            if r.status_code is not 200:
                self.error_callback(r.statuscode)
                return None
            return r
        except ConnectionError as e:
            print(e)

            self.error_callback(type(e))
            return None

    def set_module_setting(self, module_id, setting_key, data=None):
        return self.send_request(
                "/module/" + str(module_id) + "/setting/" + str(setting_key),
                data)
