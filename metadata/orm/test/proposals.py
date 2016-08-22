#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Test the proposals ORM object
"""
from datetime import datetime
from unittest import main
from json import dumps
from metadata.orm.test.base import TestBase
from metadata.orm.proposals import Proposals

SAMPLE_PROPOSAL_HASH = {
    "_id": "17a",
    "title": "My Proposal Title",
    "abstract": """
This is my proposal that's really cool and you should accept it. ;)
""",
    "science_theme": "Nobel Prize Winners",
    "proposal_type": "Blarg!",
    "encoding": "UTF8",
    "submitted_date": datetime.now().replace(microsecond=0).isoformat(),
    "accepted_date": datetime.now().date().isoformat(),
    "actual_start_date": datetime.now().date().isoformat(),
    "actual_end_date": datetime.now().date().isoformat(),
    "closed_date": datetime.now().date().isoformat()
}

SAMPLE_UNICODE_PROPOSAL_HASH = {
    "_id": u"17é",
    "title": u"My Proposal Titlé",
    "abstract": u"""
This is my proposal that's réally cool and you should accept it. ;)
""",
    "science_theme": u"Nobél Prize Winners",
    "proposal_type": u"Blarg!é",
    "encoding": "UTF8",
    "submitted_date": datetime.now().replace(microsecond=0).isoformat(),
    "accepted_date": datetime.now().date().isoformat(),
    "actual_start_date": datetime.now().date().isoformat(),
    "actual_end_date": datetime.now().date().isoformat(),
    "closed_date": datetime.now().date().isoformat()
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

    def test_unicode_proposals_hash(self):
        """
        Test the hash portion using base object method.
        """
        self.base_test_hash(SAMPLE_UNICODE_PROPOSAL_HASH)

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

    def test_unicode_proposals_where(self):
        """
        Test the hash portion using base object method.
        """
        self.base_where_clause(SAMPLE_UNICODE_PROPOSAL_HASH)

if __name__ == '__main__':
    main()
