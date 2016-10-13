#!/usr/bin/python
"""
Test all the objects
"""
from os import getenv
import logging
from unittest import main
#pylint: disable=unused-import
from metadata.orm.test.users import TestUsers
from metadata.orm.test.transactions import TestTransactions
from metadata.orm.test.files import TestFiles
from metadata.orm.test.keys import TestKeys
from metadata.orm.test.values import TestValues
from metadata.orm.test.dbdates import TestDBDates
from metadata.orm.test.file_key_value import TestFileKeyValue
from metadata.orm.test.trans_key_value import TestTransactionKeyValue
from metadata.orm.test.institutions import TestInstitutions
from metadata.orm.test.institution_person import TestInstitutionPerson
from metadata.orm.test.journals import TestJournals
from metadata.orm.test.citations import TestCitations
from metadata.orm.test.contributors import TestContributors
from metadata.orm.test.citation_contributor import TestCitationContributor
from metadata.orm.test.proposals import TestProposals
from metadata.orm.test.instruments import TestInstruments
from metadata.orm.test.proposal_instrument import TestProposalInstrument
from metadata.orm.test.proposal_participant import TestProposalParticipant
from metadata.orm.test.instrument_custodian import TestInstrumentCustodian
from metadata.orm.test.citation_proposal import TestCitationProposal
from metadata.orm.test.keywords import TestKeywords
from metadata.orm.test.groups import TestGroups
from metadata.orm.test.user_group import TestUserGroup
from metadata.orm.test.instrument_group import TestInstrumentGroup
from metadata.orm.test.analytical_tools import TestAnalyticalTools
from metadata.orm.test.atool_proposal import TestAToolProposal
from metadata.orm.test.atool_transaction import TestAToolTransaction
from metadata.orm.test.utils import TestUtils
from metadata.orm.test.connect import TestConnections
from metadata.orm.test.available_hash_list import TestKeysHashList
from metadata.elastic.test.elastic import TestElastic
from metadata.elastic.test.base import TestElasticUtils
from metadata.elastic.test.api import TestElasticAPI
from metadata.test_client import TestClient
from metadata.rest.test.orm import TestCherryPyAPI
#pylint: enable=unused-import

if __name__ == '__main__':
    if getenv('PEEWEE_SQL_DEBUG', False):
        LOGGER = logging.getLogger('peewee')
        LOGGER.setLevel(logging.DEBUG)
        LOGGER.addHandler(logging.StreamHandler())
    main()
