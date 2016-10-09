receita-tools
=============

|pypi| |travis| |license|

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

Installation
------------

To install the tool the easiest way is to use pip::

    pip install receita-tools


Tools to work with Receita's data
---------------------------------

This set of tools will allow you to easily retrieve data from Receita's
website. You can get information about multiple companies at once. Those
tools also allow you to create a few CSV files to easily import the
retrieved data to your system.

How it works
++++++++++++

The data retriever program works based on a CSV file containing information
about the CNPJs it should look for. This file must have at least on column,
and the first one should contain the CNPJ of the companies you want to get
information.

You can run ``receita get cnpj.csv`` to get information from that CSV file.
The retrieved data will be saved by default at the ``data`` directory in the
directory you ran the command. You can change the directory by using the
``--output`` option.

With the data saved locally, you can run the ``receita build`` command to
build the CSV files you need. By default, it will create two CSV files:
the ``companies.csv`` file that contains general information about
each company, and the ``activities.csv`` that contains information about the
activities of each company.

Examples
++++++++

To get data and save to ``cnpj_data`` folder::

    receita get list.csv --output cnpj_data

Keep in mind that you can use absolute or relative paths too. You can
now run the build command. If you did not used the default directory
to save the data, you need to inform it. You can also say the directory
where the generated files will be stored.

.. code::

    receita build --input cnpj_data --output results

Getting Help
++++++++++++

You can always use the ``--help`` option to get help about a command.
You can also use it with the subcommands, like ``receita build --help``.


Changelog
---------

2.1.0 (not released)
++++++++++++++++++++

* `#10`_: Add suport for ReceitaWS's `Comercial API`_
* `#9`_ / `#12`_: Reduced memory usage when dealing with a big number of companies
* `#5`_ / `#11`_: Add JSONP support on the API
* `#3`_: Add new output file: all activities seen

.. _Comercial API: https://www.receitaws.com.br/pricing

2.0.3
+++++

* `#2`_: Fixed error when handling invalid company data

.. _#2: https://github.com/vkruoso/receita-tools/issues/2
.. _#3: https://github.com/vkruoso/receita-tools/issues/3
.. _#5: https://github.com/vkruoso/receita-tools/issues/5
.. _#9: https://github.com/vkruoso/receita-tools/issues/9
.. _#10: https://github.com/vkruoso/receita-tools/issues/10
.. _#11: https://github.com/vkruoso/receita-tools/issues/11
.. _#12: https://github.com/vkruoso/receita-tools/issues/12


Webservice performance
----------------------

The performance of the webservice is very limited. This is
because Receita's website is very actively blocking access
when there is an elevated number of requests from a single
IP. We try to run workers on multiple IPs to allow a faster
response, but in any case, your code must be prepared to wait
for a long time for a response (5mins+). Results are cached,
so if you prefer, you can trigger lots of requests, and check
their results after some time.
