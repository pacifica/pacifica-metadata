#!/usr/bin/python
"""CherryPy root object class."""
from metadata.orm import ORM_OBJECTS
from metadata.elastic.elasticupdate import ElasticSearchUpdateAPI
from metadata.rest.objectinfo import ObjectInfoAPI
from metadata.rest.userinfo import UserInfoAPI
from metadata.rest.proposalinfo import ProposalInfoAPI
from metadata.rest.transactioninfo import TransactionInfoAPI
from metadata.rest.fileinfo import FileInfoAPI
from metadata.rest.ingest import IngestAPI
from metadata.rest.instrumentinfo import InstrumentInfoAPI
from metadata.rest.summaryinfo import SummaryInfoAPI
from metadata.rest.migrationinfo import MigrationInfoAPI
from metadata.rest.tkvinfo import TkvInfoAPI
from metadata.rest.tkvupload import TkvUploadAPI


# pylint: disable=too-few-public-methods
class Root(object):
    """
    CherryPy root object class.

    not exposed by default the base objects are exposed
    """

    exposed = False

    objectinfo = ObjectInfoAPI()
    elasticupdate = ElasticSearchUpdateAPI()
    userinfo = UserInfoAPI()
    proposalinfo = ProposalInfoAPI()
    fileinfo = FileInfoAPI()
    transactioninfo = TransactionInfoAPI()
    instrumentinfo = InstrumentInfoAPI()
    summaryinfo = SummaryInfoAPI()
    ingest = IngestAPI()
    migrate = MigrationInfoAPI()
    tkvinfo = TkvInfoAPI()
    tkvupload = TkvUploadAPI()
# pylint: enable=too-few-public-methods


for cls in ORM_OBJECTS:
    # this is based on the module name being something like metadata.orm.BLAH
    obj_loc = cls.__module__.split('.')[2]
    setattr(Root, obj_loc, cls())
