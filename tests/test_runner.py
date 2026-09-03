import json

import pytest

from receita.tools.runner import Runner


class TestRunner(object):
    def test_runner_with_correct_responses(self, mocker, response, cnpj_batch):
        """Tests runner execution.

        This only tests the success case, where the response is returned.
        """
        mocker.patch("requests.get", new=response)

        # Execute
        runner = Runner(cnpj_batch)
        data = {}
        for result in runner:
            data[result[0]] = result[1]

        # Check results
        for cnpj in cnpj_batch:
            assert cnpj in data
            assert data[cnpj] == json.loads(response(cnpj).content)

    def test_runner_rejects_invalid_api_type_before_starting(self, cnpj_batch):
        """An invalid api_type must fail up front.

        Validating inside a worker would kill every thread with the CNPJ
        already pulled off the queue, leaving the iterator blocked forever.
        """
        with pytest.raises(ValueError) as excinfo:
            Runner(cnpj_batch, api_type="bogus")

        assert "bogus" in str(excinfo.value)

    def test_runner_passes_base_url_to_client(self, mocker, response, cnpj_batch):
        mocker.patch("requests.get", new=response)

        runner = Runner(cnpj_batch, base_url="https://example.com/v1")
        for _ in runner:
            pass

        assert runner._base_url == "https://example.com/v1"
