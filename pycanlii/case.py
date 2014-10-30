import pycanlii.pycanliibase as base
import pycanlii.enumerations as enums
import requests
from bs4 import BeautifulSoup

class CaseDatabase(base.PyCanliiBase):

    def __init__(self, data, apikey, language=enums.Language.en):
        base.PyCanliiBase.__init__(self, apikey, language)
        self.name = data['name']

        self.id = data["databaseId"]
        # still need to add jurisdiction although for basic functionality, strictly speaking, not required
        self.jurisdiction = enums.LegislationJurisdiction[data['jurisdiction']]
        self._cases = []
        self.index = 0
        self._full = False

    def _getCases(self, extension=10000):
        cases = self._request("http://api.canlii.org/v1/caseBrowse", True, self.id,
                              offset=self.index, resultCount=extension).json()['cases']

        self.index += extension
        if (len(cases) < extension):
            self._full = False

        for case in cases:
            self._cases.append(Case(case, self._key, self._lang))


    def __iter__(self):
        while(not self._full):
            self._getCases()
        return self._cases.__iter__()

    def __getitem__(self, item):
        while(self.index <= item):
            self._getCases()
        return self._cases[item]

class Case(base.PyCanliiBase):
    """
    An object representing a CanLII Case
    """

    def __init__(self, data, apikey, language=enums.Language.en):
        base.PyCanliiBase.__init__(self, apikey, language)
        self.databaseId = data['databaseId']
        self.caseId = data['caseId'][self._lang.name]
        self.title = data['title']
        self.citation = data['citation']

        self._populated = False
        self._url = None
        self._title = None
        self._citation = None
        self._docketNumber = None
        self._decisionDate = None

        # Used to store the content of the case
        self._content = None


    def _populate(self):
        case = self._request("http://api.canlii.org/v1/caseBrowse", True, self.databaseId, self.caseId)
        case = case.json()
        self._url = case['url']
        self._title = case['title']
        self._citation = case['citation']
        self._docketNumber = case['docketNumber']
        self._decisionDate = case['decisionDate']

        self._populated = True

    def getContent(self):
        """
        Returns the HTML content of the case

        :return: Returns a BeautifulSoup object representing the HTML content of the case
        """
        if not self._populated:
            self._populate()

        if not self._content:
            req = requests.get(self._url)
            self._content = BeautifulSoup(req.content)

        return self._content

    def citedCases(self):
        """
        Returns a list of up to a maximum of 5 cases that are cited by this one. Not yet implemented.

        :return: A list of up to a maximum of 5 cases that are cited by this one
        """
        return

    def citingCases(self):
        """
        Returns a list of up to a maximum of 5 cases that are citing this one. Not yet implemented.

        :return: A list of up to a maximum of 5 cases that are citing this one
        """
        return
    def citedLegislation(self):
        """
        Returns a list of up to a maximum of 5 pieces of legislation that are cited by this one. Not yet implemented.
        
        :return: A list of up to a maximum of 5 pieces of legislation that are cited by this one
        """
        return