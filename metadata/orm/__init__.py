#!/usr/bin/python
"""
Core module loads all model objects and contains global operations
on those objects.
"""
from time import sleep
from peewee import OperationalError
from metadata.orm.base import DB
from metadata.orm.citations import Citations
from metadata.orm.contributors import Contributors
from metadata.orm.institution_person import InstitutionPerson
from metadata.orm.institutions import Institutions
from metadata.orm.instruments import Instruments
from metadata.orm.journals import Journals
from metadata.orm.keywords import Keywords
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

DATABASE_CONNECT_ATTEMPTS = 10
DATABASE_WAIT = 1

ORM_OBJECTS = [
    Journals,
    Users,
    Institutions,
    Proposals,
    Instruments,
    Citations,
    Contributors,
    InstitutionPerson,
    Keywords,
    CitationContributor,
    ProposalInstrument,
    ProposalParticipant,
    CitationProposal,
    Transactions,
    Files,
    Keys,
    Values,
    FileKeyValue
]

def try_db_connect(attempts=0):
    """
    Recursively try to connect to the database.
    """
    try:
        DB.connect()
    except OperationalError, ex:
        if attempts < DATABASE_CONNECT_ATTEMPTS:
            sleep(DATABASE_WAIT)
            attempts += 1
            try_db_connect(attempts)
        raise ex

def create_tables():
    """
    Create the tables for the objects if they exist.
    """
    try_db_connect()
    for obj in ORM_OBJECTS:
        if not obj.table_exists():
            obj.create_table()
    DB.close()
