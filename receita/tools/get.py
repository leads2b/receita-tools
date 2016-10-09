import unicodecsv
import json
import re
import os
import sys

from progressbar import Bar, Counter, Percentage, ProgressBar, Timer

from receita.tools.runner import Runner


class Get(object):

    def __init__(self, file_, output, days):
        self.file = file_
        self.output = os.path.abspath(output)
        self.days = days
        self.token = os.environ.get('RWS_TOKEN')

        if self.days and not self.token:
            print('error: no token provided. Provide an access token using '
                  'the environment variable RWS_TOKEN.')
            sys.exit(1)

    def run(self):
        """Reads data from CNPJ list and write results to output directory."""
        self._assure_output_dir(self.output)
        companies = self.read()
        print '%s CNPJs found' % len(companies)

        pbar = ProgressBar(
            widgets=[Counter(), ' ', Percentage(), ' ', Bar(), ' ', Timer()],
            maxval=len(companies)).start()

        resolved = 0
        runner = Runner(companies, self.days, self.token)

        try:
            for data in runner:
                self.write(data)
                resolved = resolved + 1
                pbar.update(resolved)
        except KeyboardInterrupt:
            print '\naborted: waiting current requests to finish.'
            runner.stop()
            return

        pbar.finish()

    def read(self):
        """Reads data from the CSV file."""
        companies = []
        with open(self.file) as f:
            reader = unicodecsv.reader(f)
            for line in reader:
                if len(line) >= 1:
                    cnpj = self.format(line[0])
                    if self.valid(cnpj):
                        companies.append(cnpj)
        return companies

    def write(self, data):
        """Writes json data to the output directory."""
        cnpj, data = data

        path = os.path.join(self.output, '%s.json' % cnpj)
        with open(path, 'w') as f:
            json.dump(data, f, encoding='utf-8')

    def _assure_output_dir(self, dir):
        # Try to create the directory
        if not os.path.exists(dir):
            try:
                os.mkdir(dir)
            except:
                print 'failed to create output directory %s' % dir
                sys.exit(1)

        # Be sure it is a directory
        if not os.path.isdir(dir):
            print 'invalid output directory %s' % dir
            sys.exit(1)

    def format(self, cnpj):
        """Removes all symbols except digits."""
        return re.sub('\D', '', cnpj)

    def valid(self, cnpj):
        """Check if a CNPJ is valid.

        We should avoid sending invalid CNPJ to the web service as we know
        it is going to be a waste of bandwidth. Assumes CNPJ is a string.
        """
        if len(cnpj) != 14:
            return False

        tam = 12
        nums = cnpj[:tam]
        digs = cnpj[tam:]

        tot = 0
        pos = tam-7
        for i in range(tam, 0, -1):
            tot = tot + int(nums[tam-i])*pos
            pos = pos - 1
            if pos < 2:
                pos = 9
        res = 0 if tot % 11 < 2 else 11 - (tot % 11)
        if res != int(digs[0]):
            return False

        tam = tam + 1
        nums = cnpj[:tam]
        tot = 0
        pos = tam-7
        for i in range(tam, 0, -1):
            tot = tot + int(nums[tam-i])*pos
            pos = pos - 1
            if pos < 2:
                pos = 9
        res = 0 if tot % 11 < 2 else 11 - (tot % 11)
        if res != int(digs[1]):
            return False

        return True
