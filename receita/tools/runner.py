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
        self._returned = 0
        self._list = list_
        self._todo = Queue.Queue()
        self._results = Queue.Queue()

        for cnpj in self._list:
            self._todo.put(cnpj)

        self._threads = []
        for index in range(0, self._CLIENT_LIMIT):
            self._threads.append(threading.Thread(
                target=self.work,
                name='worker-%s' % index
            ))
            self._threads[-1].start()

    def __iter__(self):
        return self

    # Python 3 compatibility
    def __next__(self):
        return self.next()

    def next(self):
        if self._returned == len(self._list):
            for thread in self._threads:
                thread.join()
            raise StopIteration()
        self._returned = self._returned + 1
        return self._results.get(block=True)

    def work(self):
        while self._returned < len(self._list):
            try:
                cnpj = self._todo.get(block=True, timeout=1)
            except Queue.Empty:
                continue

            data = Client(cnpj).get()
            if data:
                self._results.put((cnpj, data))
            else:
                self._todo.put(cnpj)
