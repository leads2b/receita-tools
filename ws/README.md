receita-tools webservice
========================

This is a simple implementation of a webservice that provides automatic
information recovery from Receita's website. By default it will listen to port
8080. It will also write data to the `cache` directory and will serve requests
from there when possible since the information about a company is not likely to
change in a short period of time.

Be sure to read the README file inside the root directory of this repository for
more information about the tool and how it works.

Webservice URLs
===============

Assuming you are running this webservice in your local machine, the webservice
provide the following links (where the fisrt will answer with JSON data):

    http://localhost:8080/receita/v1/cnpj/{cnpj}
    http://localhost:8080/receita/v1/cnpj/{cnpj}.json
    http://localhost:8080/receita/v1/cnpj/{cnpj}.html

Example
-------

    http://localhost:8080/receita/v1/cnpj/60580263000149
