
import json

from receita.tools.runner import Runner


class TestRunner(object):

    def test_runner_with_correct_responses(self, mocker, response, cnpj_batch):
        """Tests runner execution.

        This only tests the success case, where the response is returned.
        """
        mocker.patch('requests.get', new=response)

        # Execute
        runner = Runner(cnpj_batch)
        data = {}
        for result in runner:
            data[result[0]] = result[1]

        # Check results
        for cnpj in cnpj_batch:
            assert cnpj in data
            assert data[cnpj] == json.loads(response(cnpj).content)
