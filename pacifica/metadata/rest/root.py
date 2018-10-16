#!/usr/bin/python
# -*- coding: utf-8 -*-
"""CherryPy root object class."""
from json import dumps
import cherrypy
from pacifica.metadata.orm import ORM_OBJECTS
from pacifica.metadata.elastic.elasticupdate import ElasticSearchUpdateAPI
from pacifica.metadata.rest.objectinfo import ObjectInfoAPI
from pacifica.metadata.rest.userinfo import UserInfoAPI
from pacifica.metadata.rest.proposalinfo import ProposalInfoAPI
from pacifica.metadata.rest.transactioninfo import TransactionInfoAPI
from pacifica.metadata.rest.fileinfo import FileInfoAPI
from pacifica.metadata.rest.ingest import IngestAPI
from pacifica.metadata.rest.instrumentinfo import InstrumentInfoAPI
from pacifica.metadata.rest.summaryinfo import SummaryInfoAPI
from pacifica.metadata.rest.migrationinfo import MigrationInfoAPI
from pacifica.metadata.rest.tkvinfo import TkvInfoAPI
from pacifica.metadata.rest.tkvupload import TkvUploadAPI


def error_page_default(**kwargs):
    """The default error page should always enforce json."""
    cherrypy.response.headers['Content-Type'] = 'application/json'
    return dumps({
        'status': kwargs['status'],
        'message': kwargs['message'],
        'traceback': kwargs['traceback'],
        'version': kwargs['version']
    })


# pylint: disable=too-few-public-methods
class Root(object):
    """
    CherryPy root object class.

    not exposed by default the base objects are exposed
    """

    exposed = True

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
    # this is based on the module name being something like pacifica.metadata.orm.BLAH
    obj_loc = cls.__module__.split('.')[3]
    setattr(Root, obj_loc, cls())
