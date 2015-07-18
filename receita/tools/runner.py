
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
        self._queue = Queue.Queue()
        self._semaphore = threading.Semaphore(self._CLIENT_LIMIT)
        self._res = {}

    def run(self):
        for cnpj in self._list:
            self._semaphore.acquire()
            thread = threading.Thread(
                target=self.run_client,
                args=(Client(cnpj), )
            )
            thread.start()

        failed = []
        for cnpj in self._list:
            data = self._queue.get()
            if data is None:
                failed.append(cnpj)
            else:
                self._res[cnpj] = data

        if failed:
            self._list = failed
            return self.run()
        return self._res

    def run_client(self, client):
        try:
            data = client.get()
        except:
            data = None
        self._queue.put(data)
        self._semaphore.release()
