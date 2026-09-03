import glob
import json
import os
import sys
import csv


class BaseCSV(object):
    ERROR = "ERROR"

    def __init__(self, output):
        path = os.path.join(output, self._filename + ".csv")
        self._f = open(path, "w")

        self.writer = csv.DictWriter(
            self._f, fieldnames=self._fields, extrasaction="ignore"
        )
        self.writer.writeheader()


class _CompaniesCSV(BaseCSV):
    _filename = "companies"
    _fields = [
        "cnpj",
        "tipo",
        "abertura",
        "nome",
        "fantasia",
        "natureza_juridica",
        "porte",
        "logradouro",
        "numero",
        "complemento",
        "cep",
        "bairro",
        "municipio",
        "uf",
        "email",
        "telefone",
        "efr",
        "situacao",
        "data_situacao",
        "motivo_situacao",
        "situacao_especial",
        "data_situacao_especial",
        "capital_social",
        "simples_optante",
        "simples_data_opcao",
        "simples_data_exclusao",
        "simples_ultima_atualizacao",
        "simei_optante",
        "simei_data_opcao",
        "simei_data_exclusao",
        "simei_ultima_atualizacao",
    ]

    def visit(self, data):
        # Flatten simples and simei data
        row = data.copy()

        if "simples" in data and data["simples"]:
            row["simples_optante"] = data["simples"].get("optante")
            row["simples_data_opcao"] = data["simples"].get("data_opcao")
            row["simples_data_exclusao"] = data["simples"].get("data_exclusao")
            row["simples_ultima_atualizacao"] = data["simples"].get(
                "ultima_atualizacao"
            )

        if "simei" in data and data["simei"]:
            row["simei_optante"] = data["simei"].get("optante")
            row["simei_data_opcao"] = data["simei"].get("data_opcao")
            row["simei_data_exclusao"] = data["simei"].get("data_exclusao")
            row["simei_ultima_atualizacao"] = data["simei"].get("ultima_atualizacao")

        self.writer.writerow(row)


class _ActivitiesCSV(BaseCSV):
    _filename = "activities"
    _fields = [
        "cnpj",
        "tipo",
        "codigo",
        "descricao",
    ]

    def visit(self, data):
        if data["status"] == self.ERROR:
            return

        for activity in data["atividade_principal"]:
            self.writer.writerow(
                {
                    "cnpj": data["cnpj"],
                    "tipo": "principal",
                    "codigo": activity["code"],
                    "descricao": activity["text"],
                }
            )

        for activity in data["atividades_secundarias"]:
            self.writer.writerow(
                {
                    "cnpj": data["cnpj"],
                    "tipo": "secundaria",
                    "codigo": activity["code"],
                    "descricao": activity["text"],
                }
            )


class _ActivitiesSeenCSV(BaseCSV):
    _filename = "activities_seen"
    _fields = [
        "codigo",
        "descricao",
    ]

    def __init__(self, output):
        super(_ActivitiesSeenCSV, self).__init__(output)
        self._activities = {}

    def _process(self, activities):
        for activity in activities:
            if activity["code"] == "00.00-0-00":
                continue
            key = (
                activity["code"],
                activity["text"],
            )
            if key in self._activities:
                continue
            self._activities[key] = activity["text"]
            self.writer.writerow(
                {"codigo": activity["code"], "descricao": activity["text"]}
            )

    def visit(self, data):
        if data["status"] == self.ERROR:
            return
        self._process(data["atividade_principal"])
        self._process(data["atividades_secundarias"])


class _QSACSV(BaseCSV):
    _filename = "qsa"
    _fields = [
        "cnpj",
        "nome",
        "qual",
        "pais_origem",
        "nome_rep_legal",
        "qual_rep_legal",
    ]

    def visit(self, data):
        if data["status"] == self.ERROR:
            return

        for qsa in data["qsa"]:
            qsa.update({"cnpj": data["cnpj"]})
            self.writer.writerow(qsa)


class _SimplesCSV(BaseCSV):
    _filename = "simples"
    _fields = [
        "cnpj",
        "simples_optante",
        "simples_data_opcao",
        "simei_optante",
        "simei_data_opcao",
    ]

    def visit(self, data):
        row = {"cnpj": data.get("cnpj")}

        simples = data.get("simples")
        if simples:
            row["simples_optante"] = simples.get("optante")
            row["simples_data_opcao"] = simples.get("data_opcao")

        simei = data.get("simei")
        if simei:
            row["simei_optante"] = simei.get("optante")
            row["simei_data_opcao"] = simei.get("data_opcao")

        self.writer.writerow(row)


class _SimplesHistoricoCSV(BaseCSV):
    _filename = "simples_historico"
    _fields = [
        "cnpj",
        "tipo",
        "inicio",
        "fim",
        "detalhamento",
    ]

    def _process_historico(self, data, tipo, historico):
        if not historico:
            return
        periodos = historico.get("periodos_anteriores", [])
        if not periodos:
            return
        for periodo in periodos:
            self.writer.writerow(
                {
                    "cnpj": data.get("cnpj"),
                    "tipo": tipo,
                    "inicio": periodo.get("inicio"),
                    "fim": periodo.get("fim"),
                    "detalhamento": periodo.get("detalhamento"),
                }
            )

    def visit(self, data):
        simples = data.get("simples")
        if simples:
            self._process_historico(data, "simples", simples.get("historico"))

        simei = data.get("simei")
        if simei:
            self._process_historico(data, "simei", simei.get("historico"))


class _CCCCSV(BaseCSV):
    _filename = "ccc"
    _fields = [
        "cnpj",
        "uf",
        "ie",
        "tipo_ie",
        "situacao_ie",
        "data_situacao",
        "regime_icms",
        "situacao_cnpj",
        "data_atualizacao",
    ]

    def visit(self, data):
        if data.get("status") == self.ERROR:
            return

        cnpj = data.get("cnpj")
        for registro in data.get("registros", []):
            row = registro.copy()
            row["cnpj"] = cnpj
            self.writer.writerow(row)


VISITORS = {
    "cnpj": [
        _CompaniesCSV,
        _ActivitiesCSV,
        _ActivitiesSeenCSV,
        _QSACSV,
    ],
    "simples": [
        _SimplesCSV,
        _SimplesHistoricoCSV,
    ],
    "ccc": [
        _CCCCSV,
    ],
}


class Build(object):
    def __init__(self, input_, output, api_type="cnpj"):
        self.input = os.path.abspath(input_)
        self.output = os.path.abspath(output)
        self.api_type = api_type

    def run(self):
        """Reads data from disk and generates CSV files."""
        # Try to create the directory
        if not os.path.exists(self.output):
            try:
                os.mkdir(self.output)
            except:
                print("failed to create output directory %s" % self.output)

        # Be sure it is a directory
        if not os.path.isdir(self.output):
            print("invalid output directory %s" % self.output)
            sys.exit(1)

        # Create the CSV handlers
        visitor_classes = VISITORS.get(self.api_type)
        if visitor_classes is None:
            print(
                "invalid api_type %s; supported types are: %s"
                % (self.api_type, ", ".join(sorted(VISITORS.keys())))
            )
            sys.exit(1)
        visitors = [cls(self.output) for cls in visitor_classes]

        # Run by each company populating the CSV files
        for path in glob.glob(os.path.join(self.input, "%s_*.json" % self.api_type)):
            with open(path, "r") as f:
                try:
                    data = json.load(f)
                except ValueError:
                    continue

                for visitor in visitors:
                    visitor.visit(data)
