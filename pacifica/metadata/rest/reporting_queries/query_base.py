#!/usr/bin/python
# -*- coding: utf-8 -*-
"""CherryPy Status Metadata proposalinfo base class."""
import pytz


# pylint: disable=too-few-public-methods
class QueryBase(object):
    """Formats summary data for other classes down the tree."""

    time_basis_mappings = {
        'modified': 'mtime',
        'created': 'ctime',
        'submitted': 'updated'
    }

    object_type_mappings = {
        'instrument': 'instrument',
        'proposal': 'proposal',
        'user': 'submitter'
    }

    local_timezone = pytz.timezone('America/Los_Angeles')
