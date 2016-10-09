import json
import requests


class Client(object):

    def __init__(self, cnpj, days=None, token=None):
        self.cnpj = cnpj
        self.days = days
        self.token = token

    def get(self):
        url = 'https://www.receitaws.com.br/v1/cnpj/%s' % self.cnpj
        headers = {}

        if self.days and self.token:
            url = '%s/days/%s' % (url, self.days)
            headers.update({'Authorization': 'Bearer %s' % self.token})

        try:
            response = requests.get(url, headers=headers, timeout=70)
        except:
            return None
        if response.status_code != 200:
            return None
        return json.loads(response.content, encoding='utf-8')
