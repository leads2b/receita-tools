import os
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
        cnpj = args[0].split("/")[-1]
        return Response(cnpj)

    return get


@pytest.fixture
def cnpj_batch():
    return [
        "03420926004979",
        "03420926004980",
        "21030611000152",
        "23713354000189",
        "60580263000149",
    ]


@pytest.fixture(params=cnpj_batch())
def cnpj(request):
    return request.param
