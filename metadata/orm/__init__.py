#!/usr/bin/python
"""
Core modules.

This loads all model objects and contains global operations
on those objects.
"""
from time import sleep
from peewee import OperationalError
from metadata.elastic import create_elastic_index, try_es_connect
from metadata.orm.base import DB
from metadata.orm.citations import Citations
from metadata.orm.contributors import Contributors
from metadata.orm.institution_person import InstitutionPerson
from metadata.orm.institutions import Institutions
from metadata.orm.instruments import Instruments
from metadata.orm.instrument_custodian import InstrumentCustodian
from metadata.orm.journals import Journals
from metadata.orm.keywords import Keywords
from metadata.orm.citation_keyword import CitationKeyword
from metadata.orm.citation_contributor import CitationContributor
from metadata.orm.proposal_instrument import ProposalInstrument
from metadata.orm.users import Users
from metadata.orm.proposal_participant import ProposalParticipant
from metadata.orm.proposals import Proposals
from metadata.orm.citation_proposal import CitationProposal
from metadata.orm.files import Files
from metadata.orm.keys import Keys
from metadata.orm.values import Values
from metadata.orm.transactions import Transactions
from metadata.orm.file_key_value import FileKeyValue
from metadata.orm.trans_key_value import TransactionKeyValue
from metadata.orm.groups import Groups
from metadata.orm.user_group import UserGroup
from metadata.orm.instrument_group import InstrumentGroup
from metadata.orm.analytical_tools import AnalyticalTools
from metadata.orm.atool_proposal import AToolProposal
from metadata.orm.atool_transaction import AToolTransaction

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
    CitationContributor,
    CitationKeyword,
    ProposalInstrument,
    ProposalParticipant,
    CitationProposal,
    Transactions,
    Files,
    Keys,
    Values,
    FileKeyValue,
    TransactionKeyValue,
    Groups,
    UserGroup,
    InstrumentGroup,
    AnalyticalTools,
    AToolProposal,
    AToolTransaction
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
