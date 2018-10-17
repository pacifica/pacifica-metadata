#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Core modules.

This loads all model objects and contains global operations
on those objects.
"""
from time import sleep
from peewee import OperationalError
from ..elastic import create_elastic_index, try_es_connect
from .base import DB
from .citations import Citations
from .contributors import Contributors
from .institution_person import InstitutionPerson
from .institutions import Institutions
from .instruments import Instruments
from .instrument_custodian import InstrumentCustodian
from .journals import Journals
from .keywords import Keywords
from .citation_keyword import CitationKeyword
from .citation_contributor import CitationContributor
from .proposal_group import ProposalGroup
from .proposal_instrument import ProposalInstrument
from .users import Users
from .proposal_participant import ProposalParticipant
from .proposals import Proposals
from .citation_proposal import CitationProposal
from .files import Files
from .keys import Keys
from .values import Values
from .transactions import Transactions
from .file_key_value import FileKeyValue
from .trans_key_value import TransactionKeyValue
from .groups import Groups
from .user_group import UserGroup
from .instrument_group import InstrumentGroup
from .analytical_tools import AnalyticalTools
from .atool_proposal import AToolProposal
from .atool_transaction import AToolTransaction
from .transaction_release import TransactionRelease
from .doi_transaction import DOITransaction
from .citation_transaction import CitationTransaction
from .citation_doi import CitationDOI
from .doi_entries import DOIEntries
from .doi_authors import DOIAuthors
from .doi_author_mapping import DOIAuthorMapping
from .doi_info import DOIInfo

DATABASE_CONNECT_ATTEMPTS = 40
DATABASE_WAIT = 3

ORM_OBJECTS = [
    Journals,
    Users,
    Institutions,
    Proposals,
    Instruments,
    InstrumentCustodian,
    Citations,
    Contributors,
    InstitutionPerson,
    Keywords,
    Groups,
    CitationContributor,
    CitationKeyword,
    ProposalInstrument,
    ProposalParticipant,
    ProposalGroup,
    CitationProposal,
    Transactions,
    Files,
    Keys,
    Values,
    FileKeyValue,
    TransactionKeyValue,
    UserGroup,
    InstrumentGroup,
    AnalyticalTools,
    AToolProposal,
    AToolTransaction,
    TransactionRelease,
    DOIEntries,
    DOIAuthors,
    DOITransaction,
    CitationTransaction,
    CitationDOI,
    DOIAuthorMapping,
    DOIInfo
]


def try_db_connect(attempts=0):
    """Recursively try to connect to the database."""
    try:
        DB.connect()
    except OperationalError:
        if attempts < DATABASE_CONNECT_ATTEMPTS:
            sleep(DATABASE_WAIT)
            attempts += 1
            try_db_connect(attempts)
        else:
            raise OperationalError


def create_tables():
    """Create the tables for the objects if they exist."""
    try_db_connect()
    try_es_connect()
    create_elastic_index()
    for obj in ORM_OBJECTS:
        if not obj.table_exists():
            obj.create_table()
            obj.create_elastic_mapping()
    DB.close()
