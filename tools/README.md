Tools to work with Receita's data
=================================

This set of tools will allow you to easily retrieve data from Receita's website
about multiple companies at once. Those tools also allow you to create a few CSV
files to easily import the retrieved data where you want.

Usage / How it works
--------------------

The data retriever program works based on a CSV file containing information
about the CNPJs it should look for. This file should have two columns: the first
should contain a company identifier, and the second column should contain the
company's CNPJ. Here's an example of one line of this CSV file (suppose this is
the `cnpj.csv` file).

    "Company Identifier";"00.000.000/0000-00"

Now you're ready to run the command that will allow you to retrieve information
about those companies.

    $ php retrieve.php cnpj.csv

This script will create a directory named `data` and will create one file to
each CNPJ informed in that CSV file. The files created there are the barebone
HTML files retrieved from Receita's website.

Now you're ready to parse those HTML files and generate the data you want. The
following scripts will parse all HTML files they find in the `data` directory
and print their resulting CSV file to **stdout**.

To create a CSV file with information from each company, except their activity, run
the program `company.php` like:

    $ php company.php > companies.csv

To create a CSV with information about the activities of each company, run
the program `activities.php` to each activity type you need, like:

    $ php activities.php -m > main_activities.csv
    $ php activities.php -s > secondary_activities.csv

To finish the set of available tools, if you want to retrieve captchas from the
Receita's website there's the program `getcaptchas.php`. You can run it until
you have enough captchas to work with. This program will write captchas to the
`captchas/` directory.
