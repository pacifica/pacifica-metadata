#!/usr/bin/python
"""
Test all the objects
"""
from unittest import main
#pylint: disable=unused-import
from metadata.orm.test.users import TestUsers
from metadata.orm.test.transactions import TestTransactions
from metadata.orm.test.files import TestFiles
from metadata.orm.test.keys import TestKeys
from metadata.orm.test.values import TestValues
from metadata.orm.test.dbdates import TestDBDates
from metadata.orm.test.file_key_value import TestFileKeyValue
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
#pylint: enable=unused-import

if __name__ == '__main__':
    main()
