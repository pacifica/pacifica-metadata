#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Core modules.

This loads all model objects and contains global operations
on those objects.
"""
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
from .transsip import TransSIP
from .transsap import TransSAP
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
    AnalyticalTools,
    CitationContributor,
    CitationKeyword,
    ProposalInstrument,
    ProposalParticipant,
    ProposalGroup,
    CitationProposal,
    Transactions,
    TransSIP,
    TransSAP,
    Files,
    Keys,
    Values,
    FileKeyValue,
    TransactionKeyValue,
    UserGroup,
    InstrumentGroup,
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
