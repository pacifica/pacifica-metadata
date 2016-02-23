#!/usr/bin/python

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
from metadata.orm.files import Files
from metadata.orm.keys import Keys
from metadata.orm.values import Values
from metadata.orm.transactions import Transactions
from metadata.orm.file_key_value import FileKeyValue

class Root(object):
    exposed = False
    citations = Citations()
    contributors = Contributors()
    institution_person = InstitutionPerson()
    institutions = Institutions()
    instruments = Instruments()
    journals = Journals()
    keywords = Keywords()
    product_contributor = ProductContributor()
    proposal_instrument = ProposalInstrument()
    users = Users()
    proposal_participants = ProposalParticipants()
    proposals = Proposals()
    publication_proposal = PublicationProposal()
    files = Files()
    keys = Keys()
    values = Values()
    transactions = Transactions()
    file_key_value = FileKeyValue()

