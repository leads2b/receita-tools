receita-tools
=============

|pypi| |travis| |license|

**README Laguages:** |ptbr| |en|

Set of tools to allow automated information recovery from the
Secretary of the Federal Revenue of Brazil website. This set of
tools will use the `receitaws.com.br <http://receitaws.com.br>`_
web service to retrieve information about all Brazilian
companies you like.

.. contents::
   :local:

.. |pypi| image:: https://img.shields.io/pypi/v/receita-tools.svg?style=flat-square
    :target: https://pypi.python.org/pypi/receita-tools

.. |travis| image:: https://img.shields.io/travis/vkruoso/receita-tools.svg?style=flat-square
    :target: https://travis-ci.org/vkruoso/receita-tools
    :alt: Build Status

.. |license| image:: https://img.shields.io/dub/l/vibe-d.svg?style=flat-square

.. |ptbr| image:: https://lipis.github.io/flag-icon-css/flags/4x3/br.svg
    :target: https://github.com/vkruoso/receita-tools/blob/master/README.rst
    :height: 20px

.. |en| image:: https://lipis.github.io/flag-icon-css/flags/4x3/us.svg
    :target: https://github.com/vkruoso/receita-tools/blob/master/README.en.rst
    :height: 20px

Installation
------------

To install the tool the easiest way is to use ``pip``::

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

You can use the webservice Public API or the Comercial API. Below we describe
how to use each of them.

Public API
**********

By default the ``get`` command will use the Public API to get information about
companies. There is no extra configuration or command to perform, so you
are ready to go. For example, to get data from the companies listed in the
``list.csv`` file and save to ``cnpj_data`` folder using the Public API::

    receita get list.csv --output cnpj_data

Comercial API
*************

To use the Comercial API you need to provide two extra informations: the
maximum data deprecation value (in days) and the API access token. You can
generate an access token by accessing your control panel at the ReceitaWS
website.

Once you have that information, you need to provide your token as the
``RWS_TOKEN`` environment variable. The deprecation value must be provided
using the ``-d`` option.

To set the environment variable you can use the ``export`` command or simply
define it when getting information. Here is a sample using the ``export``
command and setting the data tolerance to 20 days::

    export RWS_TOKEN="<my-token>"
    receita get list.csv --output cnpj_data -d 20

The ``build`` command
+++++++++++++++++++++

After you run the ``get`` command all data is already downloaded to your
local filesystem. The ``build`` command is used to read all this data and
generate consolidated CSV files with its information.

If you did not used the default directory to save the data, you need to
inform it. You can also say the directory where the generated files will
be stored.

.. code::

    receita build --input cnpj_data --output results

This command will generate three files at the output directory:

* **companies.csv**: data for every company retrieved;
* **activities.csv**: list of companies activities (primary/secondary);
* **activities_seen.csv**: the full set of activities from those companies.

Getting Help
++++++++++++

You can always use the ``--help`` option to get help about a command.
You can also use it with the subcommands, like ``receita build --help``.


Changelog
---------

2.2.0
+++++

* `#17`_: Fix activities with the same code bug
* `#15`_: Add QSA support

2.1.1
+++++

* `#13`_: Documentation improvements
* `#10`_: Add suport for ReceitaWS's `Comercial API <https://www.receitaws.com.br/pricing>`_
* `#9`_ / `#12`_: Reduced memory usage when dealing with a big number of companies
* `#5`_ / `#11`_: Add JSONP support on the API
* `#3`_: Add new output file: all activities seen

2.0.3
+++++

* `#2`_: Fixed error when handling invalid company data

2.0.2
+++++

* First official release of Python package *receita-tools*

1.0.0
+++++

* A PHP release the do the webservice work. Deprecated.

.. _#2: https://github.com/vkruoso/receita-tools/issues/2
.. _#3: https://github.com/vkruoso/receita-tools/issues/3
.. _#5: https://github.com/vkruoso/receita-tools/issues/5
.. _#9: https://github.com/vkruoso/receita-tools/issues/9
.. _#10: https://github.com/vkruoso/receita-tools/issues/10
.. _#11: https://github.com/vkruoso/receita-tools/issues/11
.. _#12: https://github.com/vkruoso/receita-tools/issues/12
.. _#13: https://github.com/vkruoso/receita-tools/issues/13
