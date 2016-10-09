"""Module to execute all command line options to users.

This will be called to run various operations on companies data.
"""

import argparse
import sys

from receita.tools.get import Get
from receita.tools.build import Build


BASE_USAGE = """receita <command> [<args>]

the available commands are:
  get         download information about a list of companies
  build       create CSV files from the retrieved information"""


class Cli(object):

    def __init__(self):
        parser = argparse.ArgumentParser(
            usage=BASE_USAGE,
            epilog=(
                'You can get help for each command using the --help option '
                'for each of them.'
            )
        )
        parser.add_argument('command', help='command to run')
        args = parser.parse_args(sys.argv[1:2])
        if not hasattr(self, args.command):
            print 'unrecognized command\n'
            parser.print_help()
            exit(1)
        getattr(self, args.command)()

    def get(self):
        parser = argparse.ArgumentParser(
            prog='receita get',
            description='Download information about a list of companies.',
            epilog=(
                'The data is retrieved from ReceitaWS webservice on company '
                'information. Please, make sure you read its terms of usage '
                'and its documentation at https://www.receitaws.com.br on '
                'how the webservice works. You MAY be charged when using '
                'some features of this service.'
            )
        )
        parser.add_argument('list', help='CSV file with companies CNPJ')
        parser.add_argument(
            '-d',
            metavar="DAYS",
            dest='days',
            help='maximum data deprecation allowed in days')
        parser.add_argument(
            '--output',
            help='directory to save the output',
            default='data'
        )
        args = parser.parse_args(sys.argv[2:])

        # Execute
        Get(args.list, args.output, args.days).run()

    def build(self):
        parser = argparse.ArgumentParser(
            prog='receita build',
            description='Create CSV files from the retrieved information.')
        parser.add_argument(
            '--output',
            help='directory to save the generated CSV files',
            default='.'
        )
        parser.add_argument(
            '--input',
            help='directory to get input from',
            default='data'
        )
        args = parser.parse_args(sys.argv[2:])

        # Execute
        Build(args.input, args.output).run()


def main():
    Cli()


if __name__ == '__main__':
    main()
