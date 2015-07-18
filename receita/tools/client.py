import json
import requests

from requests.exceptions import Timeout


class Client(object):

    def __init__(self, cnpj):
        self.cnpj = cnpj
        self._timeout = 5*60

    def get(self):
        try:
            response = requests.get(
                'http://receitaws.com.br/v1/cnpj/%s' % self.cnpj,
                timeout=self._timeout
            )
        except Timeout:
            return None
        return json.loads(response.content, encoding='utf-8')
