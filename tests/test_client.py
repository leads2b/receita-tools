import requests
from requests.exceptions import Timeout

from receita.tools.client import Client


class TestClient(object):
    def test_client_returns_json_object(self, mocker, response, cnpj):
        mocker.patch("requests.get", side_effect=response)
        client = Client(cnpj)
        data = client.get()

        # Checks
        assert isinstance(data, dict)
        assert "status" in data
        assert requests.get.call_count == 1

    def test_client_returns_none_on_timeout(self, mocker, cnpj):
        mocker.patch("requests.get", side_effect=Timeout)
        client = Client(cnpj)
        data = client.get()

        # Checks
        assert data is None
        assert requests.get.call_count == 1
