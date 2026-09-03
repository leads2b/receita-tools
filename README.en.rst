receita-tools
=============

|pypi| |license|

**README Languages:** |ptbr| `Português`_ · |en| `English`_

Set of tools to allow automated information recovery from the
Secretary of the Federal Revenue of Brazil website. This set of
tools will use the `receitaws.com.br <http://receitaws.com.br>`_
web service to retrieve information about all Brazilian
companies you like.

.. |pypi| image:: https://img.shields.io/pypi/v/receita-tools.svg?style=flat-square
    :target: https://pypi.python.org/pypi/receita-tools

.. |license| image:: https://img.shields.io/dub/l/vibe-d.svg?style=flat-square

.. _Português: https://github.com/leads2b/receita-tools/blob/master/README.rst
.. _English: https://github.com/leads2b/receita-tools/blob/master/README.en.rst

.. |ptbr| image:: https://flagicons.lipis.dev/flags/4x3/br.svg
    :height: 20px

.. |en| image:: https://flagicons.lipis.dev/flags/4x3/us.svg
    :height: 20px

Installation
------------

Using Docker
++++++++++++

You can use the Docker image to run commands without installing anything
locally. The official image is published on Docker Hub:

.. code-block:: bash

    docker pull leads2b/receita-tools

Alternatively, you can build the image locally:

.. code-block:: bash

    docker build -t leads2b/receita-tools .

Then run commands by mounting a local directory for data:

.. code-block:: bash

    docker run --rm -v $(pwd):/data -e RWS_TOKEN="<my-token>" leads2b/receita-tools get list.csv --output data -d 20
    docker run --rm -v $(pwd):/data leads2b/receita-tools build --input data --output results
    docker run --rm -v $(pwd):/data -e RWS_TOKEN="<my-token>" leads2b/receita-tools get list.csv --type simples -d 20

Using pip
+++++++++

To install the tool the easiest way is to use ``pip``:

.. code-block:: bash

    pip install receita-tools


Tools to work with Receita's data
---------------------------------

This set of tools will allow you to easily retrieve data from Receita's
website. You can get information about multiple companies at once. Those
tools also allow you to create a few CSV files to easily import the
retrieved data to your system.

The Webservice
++++++++++++++

The tools provided here use the **ReceitaWS** webservice. Here are a few
important links to read about how the system works before using this tool:

* `API Documentation`_
* `FAQ`_
* `Pricing`_

.. _API Documentation: https://www.receitaws.com.br/api
.. _FAQ: https://www.receitaws.com.br/faq
.. _Pricing: https://www.receitaws.com.br/pricing

The ``get`` command
+++++++++++++++++++

The data retriever program works based on a CSV file containing information
about the CNPJs it should look for. This file must have at least on column,
and the first one should contain the CNPJ of the companies you want to get
information.

You can run ``receita get cnpj.csv`` to get information from that CSV file.
The retrieved data will be saved by default at the ``data`` directory in the
directory you ran the command. You can change the directory by using the
``--output`` option. Keep in mind that you can use absolute or relative
paths too.

The ``--type`` option lets you choose which API to query:

* ``cnpj`` (default): company registration data from Receita Federal;
* ``simples``: Simples Nacional and SIMEI data;
* ``ccc``: Cadastro Centralizado de Contribuinte (State Tax Registration) data.

You can use the webservice Public API or the Commercial API. Below we describe
how to use each of them.

Public API
**********

By default the ``get`` command will use the Public API to get information about
companies. There is no extra configuration or command to perform, so you
are ready to go. For example, to get data from the companies listed in the
``list.csv`` file and save to ``cnpj_data`` folder using the Public API:

.. code-block:: bash

    receita get list.csv --output cnpj_data

Commercial API
**************

To use the Commercial API you need to provide two extra informations: the
maximum data deprecation value (in days) and the API access token. You can
generate an access token by accessing your control panel at the ReceitaWS
website.

Once you have that information, you need to provide your token as the
``RWS_TOKEN`` environment variable. The deprecation value must be provided
using the ``-d`` option.

To set the environment variable you can use the ``export`` command or simply
define it when getting information. Here is a sample using the ``export``
command and setting the data tolerance to 20 days:

.. code-block:: bash

    export RWS_TOKEN="<my-token>"
    receita get list.csv --output cnpj_data -d 20

The ``simples`` and ``ccc`` APIs are commercial-only and always require
the ``-d`` and ``RWS_TOKEN`` parameters:

.. code-block:: bash

    export RWS_TOKEN="<my-token>"
    receita get list.csv --type simples -d 20 --output simples_data
    receita get list.csv --type ccc -d 20 --output ccc_data

Alternative base URL
********************

The ``--base-url`` option queries a base URL other than the default
(``https://www.receitaws.com.br/v1``), for when the service provides a
dedicated address:

.. code-block:: bash

    receita get list.csv --base-url https://dedicated-address/v1 -d 1 --output cnpj_data

The ``build`` command
+++++++++++++++++++++

After you run the ``get`` command all data is already downloaded to your
local filesystem. The ``build`` command is used to read all this data and
generate consolidated CSV files with its information.

If you did not used the default directory to save the data, you need to
inform it. You can also say the directory where the generated files will
be stored.

.. code-block:: bash

    receita build --input cnpj_data --output results

The API type must match the type used in the ``get`` command:

.. code-block:: bash

    receita build --type simples --input simples_data --output results
    receita build --type ccc --input ccc_data --output results

The generated files depend on the API type:

**CNPJ** (default):

* **companies.csv**: data for every company retrieved;
* **activities.csv**: list of companies activities (primary/secondary);
* **activities_seen.csv**: the full set of activities from those companies;
* **qsa.csv**: board members and partners of the companies.

**Simples Nacional** (``--type simples``):

* **simples.csv**: current Simples Nacional and SIMEI status;
* **simples_historico.csv**: historical Simples and SIMEI option periods.

**CCC** (``--type ccc``):

* **ccc.csv**: state tax registrations (Inscrição Estadual) for each company.

Getting Help
++++++++++++

You can always use the ``--help`` option to get help about a command.
You can also use it with the subcommands, like ``receita build --help``.
