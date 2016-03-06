#!/usr/bin/python
"""
Core module loads all model objects and contains global operations
on those objects.
"""
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
from metadata.orm.proposal_participants import ProposalParticipants
from metadata.orm.proposals import Proposals
from metadata.orm.citation_proposal import CitationProposal
from metadata.orm.files import Files
from metadata.orm.keys import Keys
from metadata.orm.values import Values
from metadata.orm.transactions import Transactions
from metadata.orm.file_key_value import FileKeyValue

ORM_OBJECTS = [
    Citations,
    Contributors,
    InstitutionPerson,
    Institutions,
    Instruments,
    Journals,
    Keywords,
    CitationContributor,
    ProposalInstrument,
    ProposalParticipants,
    Proposals,
    CitationProposal,
    Users,
    Transactions,
    Files,
    Keys,
    Values,
    FileKeyValue
]

def create_tables():
    """
    Create the tables for the objects if they exist.
    """
    DB.connect()
    for obj in ORM_OBJECTS:
        if not obj.table_exists():
            obj.create_table()
    DB.close()
