import glob
import json
import os
import sys
import unicodecsv


class BaseCSV(object):

    ERROR = 'ERROR'

    def __init__(self, output):
        path = os.path.join(output, self._filename + '.csv')
        self._f = open(path, 'w')

        self.writer = unicodecsv.DictWriter(
            self._f, fieldnames=self._fields,
            extrasaction='ignore')
        self.writer.writeheader()


class _CompaniesCSV(BaseCSV):

    _filename = 'companies'
    _fields = [
        'cnpj',
        'tipo',
        'abertura',
        'nome',
        'fantasia',
        'natureza_juridica',
        'logradouro',
        'numero',
        'complemento',
        'cep',
        'bairro',
        'municipio',
        'uf',
        'email',
        'telefone',
        'efr',
        'situacao',
        'data_situacao',
        'motivo_situacao',
        'situacao_especial',
        'data_situacao_especial',
    ]

    def visit(self, data):
        self.writer.writerow(data)


class _ActivitiesCSV(BaseCSV):

    _filename = 'activities'
    _fields = [
        'cnpj',
        'tipo',
        'codigo',
        'descricao',
    ]

    def visit(self, data):
        if data['status'] == self.ERROR:
            return

        for activity in data['atividade_principal']:
            self.writer.writerow({
                'cnpj': data['cnpj'],
                'tipo': 'principal',
                'codigo': activity['code'],
                'descricao': activity['text']
            })

        for activity in data['atividades_secundarias']:
            self.writer.writerow({
                'cnpj': data['cnpj'],
                'tipo': 'secundaria',
                'codigo': activity['code'],
                'descricao': activity['text']
            })


class _ActivitiesSeenCSV(BaseCSV):

    _filename = 'activities_seen'
    _fields = [
        'codigo',
        'descricao',
    ]

    def __init__(self, output):
        super(_ActivitiesSeenCSV, self).__init__(output)
        self._activities = {}

    def _process(self, activities):
        for activity in activities:
            if activity['code'] in self._activities:
                continue
            self._activities[activity['code']] = activity['text']
            self.writer.writerow({
                'codigo': activity['code'],
                'descricao': activity['text']
            })

    def visit(self, data):
        if data['status'] == self.ERROR:
            return
        self._process(data['atividade_principal'])
        self._process(data['atividades_secundarias'])


class Build(object):

    def __init__(self, input_, output):
        self.input = os.path.abspath(input_)
        self.output = os.path.abspath(output)

    def run(self):
        """Reads data from disk and generates CSV files."""
        # Try to create the directory
        if not os.path.exists(self.output):
            try:
                os.mkdir(self.output)
            except:
                print 'failed to create output directory %s' % self.output

        # Be sure it is a directory
        if not os.path.isdir(self.output):
            print 'invalid output directory %s' % self.output
            sys.exit(1)

        # Create the CSV handlers
        visitors = [
            _CompaniesCSV(self.output),
            _ActivitiesCSV(self.output),
            _ActivitiesSeenCSV(self.output)
        ]

        # Run by each company populating the CSV files
        for path in glob.glob(os.path.join(self.input, '*.json')):
            with open(path, 'r') as f:
                try:
                    data = json.load(f, encoding='utf-8')
                except ValueError:
                    continue

                for visitor in visitors:
                    visitor.visit(data)
