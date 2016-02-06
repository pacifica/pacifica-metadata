#!/usr/bin/python

from metadata.orm.base import DB
from metadata.orm.citations import Citations
from metadata.orm.contributors import Contributors
from metadata.orm.institution_person import InstitutionPerson
from metadata.orm.institutions import Institutions
from metadata.orm.instruments import Instruments
from metadata.orm.journals import Journals
from metadata.orm.keywords import Keywords
from metadata.orm.product_contributor import ProductContributor
from metadata.orm.proposal_instrument import ProposalInstrument
from metadata.orm.users import Users
from metadata.orm.proposal_participants import ProposalParticipants
from metadata.orm.proposals import Proposals
from metadata.orm.publication_proposal import PublicationProposal

def create_tables():
    objects = [
        Citations,
        Contributors,
        InstitutionPerson,
        Institutions,
        Instruments,
        Journals,
        Keywords,
        ProductContributor,
        ProposalInstrument,
        ProposalParticipants,
        Proposals,
        PublicationProposal,
        Users
    ]
    DB.connect()
    DB.create_tables(objects)
    DB.close()

