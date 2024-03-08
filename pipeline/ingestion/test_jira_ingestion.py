"""Test JiraIngestion"""
from jira_ingestion import JiraIngestion

class JiraTestNameItemCol:
    """Jira mock named item collection"""
    def __init__(self, v, k = "name"):        
        setattr(self, k, v)

class JiraTestFields:
    """Jira mock fields"""
    def __init__(self, jira):
        self.fields = jira
        self.key = jira.key


class JiraTestItem:
    """Jira mock item"""
    def __init__(self, key, components, versions, assignee, summary, description, customfield_16432, customfield_16433, customfield_16434):                        
        self.key = key
        self.components = components
        self.versions = versions
        self.assignee = assignee
        self.summary = summary
        self.description = description
        self.customfield_16432 = customfield_16432
        self.customfield_16433 = customfield_16433
        self.customfield_16434 = customfield_16434

class JiraTestCollection:
    """JIRA mock collection"""
    rows = []
    total = 0
    _index = 0

    def add(self, row):
        """adds row to collection"""
        self.rows.append(row)
        self.total = len(self.rows)

    def __iter__(self):
        """iterator method"""
        self._index = 0
        return self

    def __next__(self):
        """iterator method"""
        if self._index < len(self.rows):
            result = self.rows[self._index]
            self._index += 1
            return result
        else:
            raise StopIteration

class JiraTestClient:
    """Mocks the Jira Client for testing porpuses"""

    def search_issues(self, query, start_at, fields, max_results=99999):
        """Mocks the search_issues"""
        jiras = []
        j = JiraTestItem("TEST-1",
                [JiraTestNameItemCol("Spark")],
                [JiraTestNameItemCol("7.1.8")],
                JiraTestNameItemCol("falbani@cloudera.com", "emailAddress"),
                "Jira summary field",
                "Jira description field",
                "field_16432",
                "field_16433",
                "field_16434")

        jiras.append(JiraTestFields(j))
        jira_collection = JiraTestCollection()

        for jira in jiras:
            jira_collection.add(jira)
        return jira_collection


def test_fetch_documents():
    """Tests the fetch_documents"""
    jira_ingestion = JiraIngestion(client=JiraTestClient())
    docs = jira_ingestion.fetch_documents()
    assert len(docs)==1
    assert docs[0]["key"] == "TEST-1"
