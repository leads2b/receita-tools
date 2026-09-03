import json
import requests

DEFAULT_BASE_URL = "https://www.receitaws.com.br/v1"

API_PATHS = {
    "cnpj": "cnpj",
    "simples": "simples",
    "ccc": "ccc",
}


class Client(object):
    def __init__(self, cnpj, days=None, token=None, api_type="cnpj", base_url=None):
        self.cnpj = cnpj
        self.days = days
        self.token = token
        self.api_type = api_type
        self.base_url = (base_url or DEFAULT_BASE_URL).rstrip("/")

    def get(self):
        path = API_PATHS.get(self.api_type)
        if path is None:
            raise ValueError(
                "invalid api_type %r; valid options are: %s"
                % (self.api_type, ", ".join(sorted(API_PATHS.keys())))
            )
        url = "%s/%s/%s" % (self.base_url, path, self.cnpj)
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
