receita-tools
=============

|pypi| |travis| |license|

Set of tools to allow automated information recovery from the
Secretary of the Federal Revenue of Brazil website. This set of
tools will use the `receitaws.com.br <http://receitaws.com.br>`_
web service to retrieve information about all Brazilian
companies you like.

You can find a number of tools in the `tools` folder. Those
tools are designed so you can easily run them on a regular
basis to generate CSV files with all retrieved data. You can
then use those files to import the relevant data to the
system you want (or even directly to a database).

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


About captcha decoding
----------------------

There will be no information about how captcha decoding is
made by the web service. The last time this information was
available there was changes that broken the service.
Basic company information should be available in an easy
way so we can have a more transparent business in the
country.

Decoding percentages will be available in the future, but
they are not really good. If you know a way to achieve +70%
of success decoding it, please let me know. There's a tool
to download some sample captchas to help any development on
that area.
