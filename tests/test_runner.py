
import json
from requests.exceptions import Timeout

from receita.tools.runner import Runner


class TestRunner(object):

    def test_runner_execution(self, mocker, response, cnpj_batch):
        """Tests runner execution.

        The runner keeps trying to get the data when a timeout or any other
        exceptions occurs. We will issue a list of CNPJs to handle and make
        it return an error, a timeout and success for each of them.
        """

        # The first batch: all Timeout errors.
        # The second batch: all generic errors.
        # The third batch: one error, all other success.
        # The fourth batch: the last success.
        returns = []

        # First and second
        returns.extend([Timeout() for cnpj in cnpj_batch])
        returns.extend([Exception() for cnpj in cnpj_batch])

        # Third and fourth
        returns.extend([Timeout()])
        returns.extend([response(cnpj) for cnpj in cnpj_batch[1:]])
        returns.extend([response(cnpj_batch[0])])

        mocker.patch('requests.get', side_effect=returns)

        # Execute
        runner = Runner(cnpj_batch)
        data = runner.run()

        # Check results
        for cnpj in cnpj_batch:
            assert cnpj in data
            assert data[cnpj] == json.loads(response(cnpj).content,
                                            encoding='utf-8')
