from receita.tools.get import Get


def _cnpj(base):
    """Builds a CNPJ by appending the correct check digits to a base."""
    getter = Get("sample.csv", "/tmp", None)
    first = getter._check_digit(base)
    second = getter._check_digit(base + str(first))
    return "%s%d%d" % (base, first, second)


class TestGetFormat(object):
    def test_format_strips_punctuation_from_numeric_cnpj(self):
        getter = Get("sample.csv", "/tmp", None)

        assert getter.format("03.420.926/0049-79") == "03420926004979"

    def test_format_keeps_letters_and_normalizes_case(self):
        getter = Get("sample.csv", "/tmp", None)

        assert getter.format("AB.CD/1234.5678-80") == "ABCD1234567880"
        assert getter.format("ab.cd/1234.5678-80") == "ABCD1234567880"


class TestGetValid(object):
    def test_valid_accepts_numeric_cnpj(self):
        getter = Get("sample.csv", "/tmp", None)

        assert getter.valid("03420926004979") is True
        assert getter.valid(getter.format("03.420.926/0049-79")) is True

    def test_valid_accepts_alphanumeric_cnpj(self):
        getter = Get("sample.csv", "/tmp", None)

        assert getter.valid(_cnpj("ABCD12345678")) is True
        assert getter.valid(_cnpj("12ABC34567DE")) is True
        assert getter.valid(_cnpj("ABCD12345678").lower()) is True

    def test_valid_accepts_published_alphanumeric_sample(self):
        """Sample value published for the alphanumeric format."""
        getter = Get("sample.csv", "/tmp", None)

        assert getter.valid("00000000E08G12") is True
        assert getter.valid(getter.format("00.000.000/E08G-12")) is True
        assert getter.valid("00000000E08G13") is False

    def test_valid_rejects_wrong_check_digits(self):
        """The checksum must be enforced for both formats.

        Sending an invalid CNPJ to the web service is a waste of a request,
        so an alphanumeric value is only accepted when its check digits
        match, exactly like the numeric one.
        """
        getter = Get("sample.csv", "/tmp", None)

        assert getter.valid("03420926004978") is False
        assert getter.valid("ABCD1234567899") is False
        assert getter.valid("ABCD1234567890") is False

    def test_valid_rejects_non_numeric_check_digits(self):
        getter = Get("sample.csv", "/tmp", None)

        assert getter.valid("ABCDEFGHIJKLMN") is False
        assert getter.valid("AAAAAAAAAAAAAA") is False

    def test_valid_rejects_wrong_length_and_punctuation(self):
        getter = Get("sample.csv", "/tmp", None)

        assert getter.valid("ABCD123456788") is False
        assert getter.valid("ABCD123456788000") is False
        assert getter.valid("03.420.926/0049-79") is False
        assert getter.valid("") is False
        assert getter.valid(None) is False

    def test_valid_rejects_company_names_that_fit_the_length(self):
        """Text columns must not be mistaken for alphanumeric CNPJs."""
        getter = Get("sample.csv", "/tmp", None)

        assert getter.valid(getter.format("Empresa ABC Ltda")) is False
        assert getter.valid(getter.format("Cliente numero 1")) is False


class TestGetRead(object):
    def test_read_keeps_only_valid_cnpjs(self, tmp_path):
        alphanumeric = _cnpj("ABCD12345678")
        listing = tmp_path / "list.csv"
        listing.write_text(
            "03.420.926/0049-79\n"
            "03420926004978\n"
            "%s\n"
            "Empresa ABC Ltda\n" % alphanumeric
        )

        getter = Get(str(listing), str(tmp_path), None)

        assert getter.read() == ["03420926004979", alphanumeric]
