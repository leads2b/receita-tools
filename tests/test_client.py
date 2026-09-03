import requests
from requests.exceptions import Timeout

from receita.tools.client import DEFAULT_BASE_URL, Client


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

    def test_client_cnpj_url(self, mocker, response, cnpj):
        mocker.patch("requests.get", side_effect=response)
        Client(cnpj, api_type="cnpj").get()
        url = requests.get.call_args[0][0]
        assert "/v1/cnpj/" in url

    def test_client_simples_url(self, mocker, response, cnpj):
        mocker.patch("requests.get", side_effect=response)
        Client(cnpj, days=30, token="tok", api_type="simples").get()
        url = requests.get.call_args[0][0]
        assert "/v1/simples/" in url
        assert "/days/30" in url

    def test_client_ccc_url(self, mocker, response, cnpj):
        mocker.patch("requests.get", side_effect=response)
        Client(cnpj, days=30, token="tok", api_type="ccc").get()
        url = requests.get.call_args[0][0]
        assert "/v1/ccc/" in url
        assert "/days/30" in url

    def test_client_auth_header_when_token(self, mocker, response, cnpj):
        mocker.patch("requests.get", side_effect=response)
        Client(cnpj, days=30, token="mytoken", api_type="simples").get()
        headers = requests.get.call_args[1].get("headers", {})
        assert headers.get("Authorization") == "Bearer mytoken"

    def test_client_uses_default_base_url(self, mocker, response, cnpj):
        mocker.patch("requests.get", side_effect=response)
        Client(cnpj).get()
        url = requests.get.call_args[0][0]
        assert url.startswith("%s/cnpj/" % DEFAULT_BASE_URL)

    def test_client_uses_custom_base_url(self, mocker, response, cnpj):
        mocker.patch("requests.get", side_effect=response)
        Client(cnpj, base_url="https://example.com/v1").get()
        url = requests.get.call_args[0][0]
        assert url == "https://example.com/v1/cnpj/%s" % cnpj

    def test_client_strips_trailing_slash_from_base_url(self, mocker, response, cnpj):
        mocker.patch("requests.get", side_effect=response)
        Client(cnpj, base_url="https://example.com/v1/").get()
        url = requests.get.call_args[0][0]
        assert url == "https://example.com/v1/cnpj/%s" % cnpj

    def test_client_custom_base_url_with_type_and_days(self, mocker, response, cnpj):
        mocker.patch("requests.get", side_effect=response)
        Client(
            cnpj,
            days=1,
            token="tok",
            api_type="simples",
            base_url="https://example.com/v1",
        ).get()
        url = requests.get.call_args[0][0]
        assert url.startswith("https://example.com/v1/simples/%s" % cnpj)
        assert "/days/1" in url
