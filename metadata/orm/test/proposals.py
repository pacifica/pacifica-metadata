#!/usr/bin/python
"""
Test the proposals ORM object
"""
from datetime import datetime
from time import mktime
from unittest import main
from json import dumps
from metadata.orm.test.base import TestBase
from metadata.orm.proposals import Proposals

SAMPLE_PROPOSAL_HASH = {
    "_id": 17,
    "title": "My Proposal Title",
    "abstract": """
This is my proposal that's really cool and you should accept it. ;)
""",
    "science_theme": "Nobel Prize Winners",
    "proposal_type": "Blarg!",
    "submitted_date": int(mktime(datetime.now().timetuple())),
    "accepted_date": int(mktime(datetime.now().timetuple())),
    "actual_start_date": int(mktime(datetime.now().timetuple())),
    "actual_end_date": int(mktime(datetime.now().timetuple()))
}

class TestProposals(TestBase):
    """
    Test the Proposals ORM object
    """
    obj_cls = Proposals
    obj_id = Proposals.id

    @classmethod
    def dependent_cls(cls):
        """
        Return dependent classes for the Proposals object
        """
        return [Proposals]

    def test_proposals_hash(self):
        """
        Test the hash portion using base object method.
        """
        self.base_test_hash(SAMPLE_PROPOSAL_HASH)

    def test_proposals_json(self):
        """
        Test the hash portion using base object method.
        """
        self.base_test_json(dumps(SAMPLE_PROPOSAL_HASH))

    def test_proposals_where(self):
        """
        Test the hash portion using base object method.
        """
        self.base_where_clause(SAMPLE_PROPOSAL_HASH)

if __name__ == '__main__':
    main()
