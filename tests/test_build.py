import csv
import json

from receita.tools.build import Build


class TestBuildSimples(object):
    def test_build_simples_csv(self, tmp_path):
        # Write a sample simples JSON file
        data = {
            "cnpj": "03420926004979",
            "simples": {
                "optante": True,
                "data_opcao": "2019-08-24T14:15:22Z",
                "historico": {
                    "periodos_anteriores": [
                        {
                            "inicio": "2014-01-01",
                            "fim": "2018-12-31",
                            "detalhamento": "Optante pelo Simples Nacional",
                        }
                    ]
                },
            },
            "simei": {
                "optante": False,
                "data_opcao": None,
                "historico": {"periodos_anteriores": []},
            },
        }
        input_dir = tmp_path / "input"
        input_dir.mkdir()
        with open(input_dir / "simples_03420926004979.json", "w") as f:
            json.dump(data, f)

        output_dir = tmp_path / "output"
        output_dir.mkdir()

        Build(str(input_dir), str(output_dir), api_type="simples").run()

        # Check simples.csv
        with open(output_dir / "simples.csv") as f:
            reader = list(csv.DictReader(f))
            assert len(reader) == 1
            row = reader[0]
            assert row["cnpj"] == "03420926004979"
            assert row["simples_optante"] == "True"
            assert row["simples_data_opcao"] == "2019-08-24T14:15:22Z"
            assert row["simei_optante"] == "False"

        # Check simples_historico.csv
        with open(output_dir / "simples_historico.csv") as f:
            reader = list(csv.DictReader(f))
            assert len(reader) == 1
            row = reader[0]
            assert row["cnpj"] == "03420926004979"
            assert row["tipo"] == "simples"
            assert row["inicio"] == "2014-01-01"
            assert row["fim"] == "2018-12-31"


class TestBuildCCC(object):
    def test_build_ccc_csv(self, tmp_path):
        data = {
            "status": "OK",
            "ultima_atualizacao": "2019-08-24T14:15:22Z",
            "cnpj": "03420926004979",
            "registros": [
                {
                    "uf": "SP",
                    "ie": "123456789",
                    "tipo_ie": "Principal",
                    "situacao_ie": "Ativa",
                    "data_situacao": "2019-01-01",
                    "regime_icms": "Normal",
                    "situacao_cnpj": "Ativa",
                    "data_atualizacao": "2019-08-24",
                },
                {
                    "uf": "RJ",
                    "ie": "987654321",
                    "tipo_ie": "Secundaria",
                    "situacao_ie": "Ativa",
                    "data_situacao": "2020-06-15",
                    "regime_icms": "Simples Nacional",
                    "situacao_cnpj": "Ativa",
                    "data_atualizacao": "2020-06-15",
                },
            ],
        }
        input_dir = tmp_path / "input"
        input_dir.mkdir()
        with open(input_dir / "ccc_03420926004979.json", "w") as f:
            json.dump(data, f)

        output_dir = tmp_path / "output"
        output_dir.mkdir()

        Build(str(input_dir), str(output_dir), api_type="ccc").run()

        # Check ccc.csv
        with open(output_dir / "ccc.csv") as f:
            reader = list(csv.DictReader(f))
            assert len(reader) == 2
            assert reader[0]["cnpj"] == "03420926004979"
            assert reader[0]["uf"] == "SP"
            assert reader[0]["ie"] == "123456789"
            assert reader[1]["uf"] == "RJ"
            assert reader[1]["ie"] == "987654321"


class TestBuildCNPJBackwardCompat(object):
    def test_build_default_type_is_cnpj(self, tmp_path):
        """Ensure Build without api_type still works (backward compat)."""
        build = Build(str(tmp_path), str(tmp_path))
        assert build.api_type == "cnpj"
