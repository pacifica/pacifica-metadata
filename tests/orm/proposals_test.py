#!/usr/bin/python
# -*- coding: utf-8 -*-
"""Test the proposals ORM object."""
from datetime import datetime
from json import dumps
from pacifica.metadata.orm.utils import datetime_now_nomicrosecond
from pacifica.metadata.orm.proposals import Proposals
from .base_test import TestBase

SAMPLE_PROPOSAL_HASH = {
    '_id': '17a',
    'title': 'My Proposal Title',
    'short_name': 'Short Name for Display',
    'abstract': """
This is my proposal that's really cool and you should accept it. ;)
""",
    'science_theme': 'Nobel Prize Winners',
    'proposal_type': 'Blarg!',
    'encoding': 'UTF8',
    'submitted_date': datetime_now_nomicrosecond().isoformat(),
    'accepted_date': datetime.utcnow().date().isoformat(),
    'actual_start_date': datetime.utcnow().date().isoformat(),
    'actual_end_date': datetime.utcnow().date().isoformat(),
    'closed_date': datetime.utcnow().date().isoformat(),
    'suspense_date': datetime.utcnow().date().isoformat()
}

SAMPLE_UNICODE_PROPOSAL_HASH = {
    '_id': u'17é',
    'title': u'My Proposal Titlé',
    'short_name': u'Short Namé for Display',
    'abstract': u"""
This is my proposal that's réally cool and you should accept it. ;)
""",
    'science_theme': u'Nobél Prize Winners',
    'proposal_type': u'Blarg!é',
    'encoding': 'UTF8',
    'submitted_date': datetime_now_nomicrosecond().isoformat(),
    'accepted_date': datetime.utcnow().date().isoformat(),
    'actual_start_date': datetime.utcnow().date().isoformat(),
    'actual_end_date': datetime.utcnow().date().isoformat(),
    'closed_date': datetime.utcnow().date().isoformat(),
    'suspense_date': datetime.utcnow().date().isoformat()
}


class TestProposals(TestBase):
    """Test the Proposals ORM object."""

    obj_cls = Proposals
    obj_id = Proposals.id

    def test_proposals_hash(self):
        """Test the hash portion using base object method."""
        self.base_test_hash(SAMPLE_PROPOSAL_HASH)

    def test_unicode_proposals_hash(self):
        """Test the hash portion using base object method."""
        self.base_test_hash(SAMPLE_UNICODE_PROPOSAL_HASH)

    def test_proposals_json(self):
        """Test the hash portion using base object method."""
        self.base_test_json(dumps(SAMPLE_PROPOSAL_HASH))

    def test_proposals_sexpr_uni(self):
        """Test the hash portion using base object method."""
        self.base_where_clause_search_expr(
            SAMPLE_UNICODE_PROPOSAL_HASH,
            title_operator='ILIKE',
            title=u'%é%'
        )

    def test_proposals_sexpr_txt(self):
        """Test the hash portion using base object method."""
        self.base_where_clause_search_expr(
            SAMPLE_PROPOSAL_HASH,
            abstract_operator='ILIKE',
            abstract='%This%'
        )

    def test_proposals_where(self):
        """Test the hash portion using base object method."""
        self.base_where_clause(SAMPLE_PROPOSAL_HASH)

    def test_unicode_proposals_where(self):
        """Test the hash portion using base object method."""
        self.base_where_clause(SAMPLE_UNICODE_PROPOSAL_HASH)
