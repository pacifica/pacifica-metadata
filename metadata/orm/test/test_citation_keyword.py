#!/usr/bin/python
"""Test the citation contributor ORM object."""
from json import dumps
from metadata.orm.test.base import TestBase
from metadata.orm.citation_keyword import CitationKeyword
from metadata.orm.test.test_keywords import SAMPLE_KEYWORD_HASH, TestKeywords
from metadata.orm.keywords import Keywords
from metadata.orm.test.test_citations import SAMPLE_CITATION_HASH, TestCitations
from metadata.orm.citations import Citations

SAMPLE_CITATION_KEYWORD_HASH = {
    'citation_id': SAMPLE_CITATION_HASH['_id'],
    'keyword_id': SAMPLE_KEYWORD_HASH['_id']
}


class TestCitationKeyword(TestBase):
    """Test the Keyword ORM object."""

    obj_cls = CitationKeyword
    obj_id = CitationKeyword.keyword

    @classmethod
    def dependent_cls(cls):
        """Return dependent classes for the CitationContributor object."""
        ret = [CitationKeyword]
        ret += TestKeywords.dependent_cls()
        ret += TestCitations.dependent_cls()
        return ret

    @classmethod
    def base_create_dep_objs(cls):
        """Create all objects that Files depend on."""
        keyword = Keywords()
        TestKeywords.base_create_dep_objs()
        keyword.from_hash(SAMPLE_KEYWORD_HASH)
        keyword.save(force_insert=True)
        cite1 = Citations()
        TestCitations.base_create_dep_objs()
        cite1.from_hash(SAMPLE_CITATION_HASH)
        cite1.save(force_insert=True)

    def test_citation_keyword_hash(self):
        """Test the hash portion using base object method."""
        self.base_test_hash(SAMPLE_CITATION_KEYWORD_HASH)

    def test_citation_keyword_json(self):
        """Test the hash portion using base object method."""
        self.base_test_json(dumps(SAMPLE_CITATION_KEYWORD_HASH))

    def test_citation_keyword_where(self):
        """Test the hash portion using base object method."""
        self.base_where_clause(SAMPLE_CITATION_KEYWORD_HASH)
