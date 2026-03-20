import json
import requests

API_PATHS = {
    "cnpj": "cnpj",
    "simples": "simples",
    "ccc": "ccc",
}


class Client(object):
    def __init__(self, cnpj, days=None, token=None, api_type="cnpj"):
        self.cnpj = cnpj
        self.days = days
        self.token = token
        self.api_type = api_type

    def get(self):
        path = API_PATHS[self.api_type]
        url = "https://www.receitaws.com.br/v1/%s/%s" % (path, self.cnpj)
        headers = {}

        if self.days and self.token:
            url = "%s/days/%s?fallback=noCache" % (url, self.days)
            headers.update({"Authorization": "Bearer %s" % self.token})

        try:
            response = requests.get(url, headers=headers, timeout=70)
        except:
            return None
        if response.status_code != 200:
            return None
        return json.loads(response.content)
