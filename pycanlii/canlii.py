__author__ = 'jonathanwebb'

import pycanlii.pycanliibase as base
from pycanlii.legislation import LegislationDatabase
import os
import pycanlii.enumerations as enums

class CanLII(base.PyCanliiBase):

    def __init__(self, apikey, language=enums.Language.en):
        base.PyCanliiBase.__init__(self, apikey, language)

    def legislation_databases(self):
        '''
        Returns a list of LegislationDatabase objects, each representing a legislation database on CanLII
        :return: A list of LegislationDatabase objects
        '''
        l = self._request("http://api.canlii.org/v1/legislationBrowse", True)
        ret = []
        dbs = l.json()['legislationDatabases']
        for db in dbs:
            ret.append(LegislationDatabase(db, self.key, self.lang))

        return ret


if __name__ == '__main__':
    x = CanLII(os.environ["CANLII_KEY"])
    #y = x.request("http://api.canlii.org/v1/legislationBrowse", True)
    #print(y.json())
    y = x.legislation_databases()
    print(y)