import json
import requests


class Client(object):

    def __init__(self, cnpj):
        self.cnpj = cnpj

    def get(self):
        try:
            response = requests.get(
                'http://www.receitaws.com.br/v1/cnpj/%s' % self.cnpj,
                timeout=70
            )
        except:
            return None
        if response.status_code != 200:
            return None
        return json.loads(response.content, encoding='utf-8')
