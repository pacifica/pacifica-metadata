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

    Attributes:
        +--------------------------+-----------------------------------------+
        | Name                     | Description                             |
        +==========================+=========================================+
        | article_title            | The title of the article                |
        +--------------------------+-----------------------------------------+
        | journal                  | Link to the journal it was published in |
        +--------------------------+-----------------------------------------+
        | journal_volume           | Journal volume for the publication      |
        +--------------------------+-----------------------------------------+
        | journal_issue            | Journal issue for the publication       |
        +--------------------------+-----------------------------------------+
        | page_range               | Pages in issue/volume was the article   |
        +--------------------------+-----------------------------------------+
        | abstract_text            | Abstract from the article in the        |
        |                          | journal                                 |
        +--------------------------+-----------------------------------------+
        | xml_text                 | xml blob for the citation               |
        +--------------------------+-----------------------------------------+
        | release_authorization_id | External link to authorization metadata |
        |                          | about the released article              |
        +--------------------------+-----------------------------------------+
        | doi_reference            | Digital Object Identifier for the       |
        |                          | citation                                |
        +--------------------------+-----------------------------------------+
        | encoding                 | Language this metadata is in not the    |
        |                          | article itself                          |
        +-------------------+------------------------------------------------+
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
    encoding = CharField(default="UTF8")

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
        obj['encoding'] = {'type': 'string'}

    def to_hash(self):
        """
        Convert the citation fields to a serializable hash.
        """
        obj = super(Citations, self).to_hash()
        obj['_id'] = int(self.id)
        obj['article_title'] = unicode(self.article_title)
        obj['abstract_text'] = unicode(self.abstract_text)
        obj['xml_text'] = unicode(self.xml_text)
        obj['journal_id'] = int(self.journal.id)
        obj['journal_volume'] = int(self.journal_volume)
        obj['journal_issue'] = int(self.journal_issue)
        obj['page_range'] = str(self.page_range)
        obj['doi_reference'] = str(self.doi_reference)
        obj['release_authorization_id'] = str(self.release_authorization_id)
        obj['encoding'] = str(self.encoding)
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
        if 'journal_id' in obj:
            self.journal = Journals.get(Journals.id == int(obj['journal_id']))
        for key in ['journal_volume', 'journal_issue']:
            if key in obj:
                setattr(self, key, int(obj[key]))
        for key in ['page_range', 'release_authorization_id', 'encoding',
                    'doi_reference']:
            if key in obj:
                setattr(self, key, str(obj[key]))
        for key in ['article_title', 'xml_text', 'abstract_text']:
            if key in obj:
                setattr(self, key, unicode(obj[key]))

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
                    'doi_reference', 'encoding']:
            if key in kwargs:
                key_oper = OP.EQ
                if "%s_operator"%(key) in kwargs:
                    key_oper = getattr(OP, kwargs["%s_operator"%(key)])
                where_clause &= Expression(getattr(Citations, key), key_oper, kwargs[key])
        return where_clause
