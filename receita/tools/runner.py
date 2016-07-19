
import Queue
import threading

from receita.tools.client import Client


class Runner(object):
    """Client runner.

    We are keeping multiple requests running at the same time, but
    in a limited fashion. This will allow a better performance while
    getting data from the web service.

    This class assumes that the CNPJ list consists only of valid data
    and that the web service will always return valid json.
    """
    _CLIENT_LIMIT = 5

    def __init__(self, list_):
        self._list = list_
        self._todo = Queue.Queue()
        self._results = Queue.Queue()

    def run(self):
        for cnpj in self._list:
            self._todo.put(cnpj)

        threads = []
        for index in range(0, self._CLIENT_LIMIT):
            threads.append(threading.Thread(
                target=self.work,
                name='worker-%s' % index
            ))
            threads[-1].start()

        while not self._todo.empty():
            yield self._results.get()

        for thread in threads:
            thread.join()

    def work(self):
        while not self._todo.empty():
            cnpj = self._todo.get()

            try:
                data = Client(cnpj).get()
                self._results.put((cnpj, data))
            except:
                # retry later
                self._todo.put(cnpj)
                continue
