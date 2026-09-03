import os
import re
import sys

import pytest

# Add module to the path
base = os.path.abspath(os.path.dirname(__file__))
sys.path.insert(0, (os.path.join(base, "..")))

# Create resources path
resources = os.path.join(base, "resources")


@pytest.fixture
def response():
    class Response(object):
        def __init__(self, cnpj):
            self.status_code = 200
            self.content = None

            path = os.path.join(resources, cnpj)
            with open("%s.json" % path, "rb") as f:
                self.content = f.read()

    def get(*args, **kwargs):
        # The URL may include extra path segments and a query string
        # (e.g. .../simples/<cnpj>/days/30?fallback=noCache), so pick the
        # 14-digit CNPJ token rather than the last path segment.
        match = re.search(r"\d{14}", args[0])
        cnpj = match.group(0) if match else args[0].split("/")[-1]
        return Response(cnpj)

    return get


_CNPJ_BATCH = [
    "03420926004979",
    "03420926004980",
    "21030611000152",
    "23713354000189",
    "60580263000149",
]


@pytest.fixture
def cnpj_batch():
    return _CNPJ_BATCH


@pytest.fixture(params=_CNPJ_BATCH)
def cnpj(request):
    return request.param
