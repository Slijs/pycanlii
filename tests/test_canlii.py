from pycanlii.canlii import CanLII
from pycanlii.enumerations import Language
from pycanlii.legislation import LegislationDatabase
from pycanlii.case import CaseDatabase

class TestCanLII:

    def test__init__(self, config):
        canlii_en = CanLII(config['key'], Language.en)
        assert canlii_en._key == config['key']
        assert canlii_en._lang == Language.en

        canlii_fr = CanLII(config['key'], Language.fr)
        assert canlii_fr._key == config['key']
        assert canlii_fr._lang == Language.en

    def test_legis_db(self, canlii):
        legislation = canlii.legislation_databases()
        assert type(legislation) == LegislationDatabase

    def test_case_db(self, canlii):
        cases = canlii.case_databases()
        assert type(cases) == CaseDatabase