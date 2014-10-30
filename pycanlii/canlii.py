import pycanlii.pycanliibase as base
import pycanlii.legislation
import pycanlii.case
import os
import pycanlii.enumerations as enums

class CanLII(base.PyCanliiBase):
    """
    This is base the object used to interface with the CanLII API.
    """


    def __init__(self, apikey, language=enums.Language.en):
        """
        Initializes a CanLII object. It takes in a string representing your api key for the CanLII API. Optionally you
        can also put in a pycanlii.enumerations.Language enum, if you don't it defaults to english.
        :param apikey: A string representing your CanLII api key
        :param language: A pycanlii.enuemerations.Language enum, defaults to english
        :return: None
        """
        base.PyCanliiBase.__init__(self, apikey, language)
        self._db = None

    def legislation_databases(self):
        """
        Returns a list of LegislationDatabase objects, each representing a legislation database on CanLII
        :return: A list of LegislationDatabase objects
        """
        l = self._request("http://api.canlii.org/v1/legislationBrowse", True)
        self._db = []
        dbs = l.json()['legislationDatabases']
        for db in dbs:
            self._db.append(pycanlii.legislation.LegislationDatabase(db, self._key, self._lang))

        return self._db


    def case_databases(self):
        """
        Returns a list of CaseDatabase objects, each representing the case database on CanLII
        :return: A list of CaseDatabase objects
        """
        l = self._request("http://api.canlii.org/v1/caseBrowse", True)
        casedb = []
        dbs = l.json()['caseDatabases']
        for db in dbs:
            casedb.append(pycanlii.case.CaseDatabase(db, self._key, self._lang))

        return casedb

    def search(self, fullText, resultCount=100, offset=0):
        """
        Returns upto the first 100 results of a search in CanLII. If you can potentially return more than 100 results
        you're bad and you should feel bad. Put in a more precise search.
        :param fullText: Your search query
        :param resultCount: Some number less than 100. Okay?
        :param offset: This can technically be anything, any positive integer anyways. I'd be wary of going
        _too_ hard on this one
        :return: A list of results
        """
        results = self._request("http://api.canlii.org/v1/search", True, fullText=fullText,
                                 resultCount=resultCount, offset=offset).json()
        results = results['results']
        l = []
        for result in results:
            if 'legislation' in result:
                l.append(pycanlii.legislation.Legislation(result['legislation'], self._key, self._lang))
            else:
                l.append(pycanlii.case.Case(result['case'], self._key, self._lang))
        return l
