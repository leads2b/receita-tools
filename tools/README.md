Tools work with Receita's data
==============================

This set of tools will allow you to easily retrieve data from multiple
companies. Those tool will also allow you to create a few CSV files to easily
export the retrieved data and adapt it the way you want.

Usage / How it works
--------------------

All tools work based on the existence one CSV file. This file should be a CSV
file containing one line for each company you want information from. Each line
should contain in the first column some company identifier, and the second
column should contain the company CNPJ. Here's an example of one line of this
CSV.

    "Company Identifier";"00.000.000/0000-00"

Now you're ready to run the command that will allow you to retrieve information
about those companies (supposing the CSV file is `cnpj.csv`).

    $ php retrieve.php cnpj.csv

This script will create a directory named `data` and will create one file to
each CNPJ informed in the CSV file. The files created there are the barebone
HTML file retrieved from the Receita's website.

Now you're ready to parse thos HTML files and generate the data you want. The
following scripts will parse all HTML files they find in the `data` directory
and print to **stdout** the resulting CSV file.

To create a CSV with information from each company, except their activity, run
the program `company.php` like:

    $ php company.php

To craete a CSV with information about the activities of each company, run the
the program `activities.php` to each activity type you need, like:

    $ php activities.php -m     # main activities
    $ php activities.php -s     # secondary activities

To finish the set of available tools, you may want to retrieve captchas from the
Receita's website. To do this in an easy way, use the program `getcaptchas.php`.
This program will write captchas to the `captchas/` directory.
