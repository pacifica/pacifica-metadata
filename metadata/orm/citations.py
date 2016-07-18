#!/usr/bin/python
"""
Citations model for tracking journal articles.
"""
from peewee import IntegerField, TextField, CharField, ForeignKeyField, Expression, OP
from metadata.orm.journals import Journals
from metadata.rest.orm import CherryPyAPI

# Citations has too many attributes...
# pylint: disable=too-many-instance-attributes
class Citations(CherryPyAPI):
    """
    Citations model tracks metadata for a journal article.
    """
    article_title = TextField(default="")
    journal = ForeignKeyField(Journals, related_name='citations')
    journal_volume = IntegerField(default=-1)
    journal_issue = IntegerField(default=-1)
    page_range = CharField(default="")
    abstract_text = TextField(default="")
    xml_text = TextField(default="")
    release_authorization_id = CharField(default="")
    doi_reference = CharField(default="")

    @staticmethod
    def elastic_mapping_builder(obj):
        """
        Build the elasticsearch mapping bits
        """
        super(Citations, Citations).elastic_mapping_builder(obj)
        obj['journal_id'] = obj['journal_volume'] = \
        obj['journal_issue'] = {'type': 'integer'}
        obj['article_title'] = obj['abstract_text'] = obj['xml_text'] = \
        obj['page_range'] = obj['doi_reference'] = obj['release_authorization_id'] = \
        {'type': 'string'}

    def to_hash(self):
        """
        Convert the citation fields to a serializable hash.
        """
        obj = super(Citations, self).to_hash()
        obj['_id'] = int(self.id)
        obj['article_title'] = str(self.article_title)
        obj['abstract_text'] = str(self.abstract_text)
        obj['xml_text'] = str(self.xml_text)
        obj['journal_id'] = int(self.journal.id)
        obj['journal_volume'] = int(self.journal_volume)
        obj['journal_issue'] = int(self.journal_issue)
        obj['page_range'] = str(self.page_range)
        obj['doi_reference'] = str(self.doi_reference)
        obj['release_authorization_id'] = str(self.release_authorization_id)
        return obj

    def from_hash(self, obj):
        """
        Converts the object into the citation object fields.
        """
        super(Citations, self).from_hash(obj)
        if '_id' in obj:
            # pylint: disable=invalid-name
            self.id = int(obj['_id'])
            # pylint: enable=invalid-name
        if 'article_title' in obj:
            self.article_title = str(obj['article_title'])
        if 'journal_id' in obj:
            self.journal = Journals.get(Journals.id == int(obj['journal_id']))
        if 'journal_volume' in obj:
            self.journal_volume = int(obj['journal_volume'])
        if 'journal_issue' in obj:
            self.journal_issue = int(obj['journal_issue'])
        if 'page_range' in obj:
            self.page_range = str(obj['page_range'])
        if 'doi_reference' in obj:
            self.doi_reference = str(obj['doi_reference'])
        if 'xml_text' in obj:
            self.xml_text = str(obj['xml_text'])
        if 'release_authorization_id' in obj:
            self.release_authorization_id = str(obj['release_authorization_id'])
        if 'abstract_text' in obj:
            self.abstract_text = str(obj['abstract_text'])

    def where_clause(self, kwargs):
        """
        Generate the PeeWee where clause used in searching.
        """
        where_clause = super(Citations, self).where_clause(kwargs)
        if 'journal_id' in kwargs:
            journal = Journals.get(Journals.id == int(kwargs['journal_id']))
            where_clause &= Expression(Citations.journal, OP.EQ, journal)
        if '_id' in kwargs:
            where_clause &= Expression(Citations.id, OP.EQ, int(kwargs['_id']))
        for key in ['article_title', 'journal_volume', 'journal_issue', 'page_range',
                    'doi_reference']:
            if key in kwargs:
                where_clause &= Expression(getattr(Citations, key), OP.EQ, kwargs[key])
        return where_clause
