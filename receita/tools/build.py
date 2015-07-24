import unicodecsv
import glob
import json
import os
import sys


class Build(object):

    ERROR = 'ERROR'

    def __init__(self, input_, output):
        self.input = os.path.abspath(input_)
        self.output = os.path.abspath(output)

    def run(self):
        """Reads data from disk and generates CSV files."""
        self.write(self.read())

    def read(self):
        """Reads data from the json files."""
        content = []
        for path in glob.glob(os.path.join(self.input, '*.json')):
            with open(path, 'r') as f:
                try:
                    content.append(json.load(f, encoding='utf-8'))
                except ValueError:
                    pass
        return content

    def write(self, data):
        """Builds the CSV file from data."""
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

        # Save companies information first
        fields = [
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

        path = os.path.join(self.output, 'companies.csv')
        with open(path, 'w') as f:
            writer = unicodecsv.DictWriter(
                f, fieldnames=fields,
                extrasaction='ignore')

            writer.writeheader()
            for company in data:
                writer.writerow(company)

        # Save all activities for each company
        fields = [
            'cnpj',
            'tipo',
            'codigo',
            'descricao',
        ]

        path = os.path.join(self.output, 'activities.csv')
        with open(path, 'w') as f:
            writer = unicodecsv.DictWriter(
                f, fieldnames=fields,
                extrasaction='ignore')

            writer.writeheader()
            for company in data:
                if company['status'] == self.ERROR:
                    continue
                for activity in company['atividade_principal']:
                    writer.writerow({
                        'cnpj': company['cnpj'],
                        'tipo': 'principal',
                        'codigo': activity['code'],
                        'descricao': activity['text']
                    })

                for activity in company['atividades_secundarias']:
                    writer.writerow({
                        'cnpj': company['cnpj'],
                        'tipo': 'secundaria',
                        'codigo': activity['code'],
                        'descricao': activity['text']
                    })
