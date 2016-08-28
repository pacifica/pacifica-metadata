#!/usr/bin/python
"""
Metadata Client Module
"""

from json import loads, dumps
import requests

class PMClientError(Exception):
    """
    Base Exception Error Class
    """
    pass

class PMClient(object):
    """
    Pacifica Metadata Client

    This class provides client API to connect to the metadata service
    """

    def __init__(self, url):
        """
        constructor takes the url to the endpoint
        """
        self.url = url

    def create(self, cls_type, set_hash):
        """
        Create the object of type based on hash
        """
        ret = requests.put('%s/%s'%(self.url, cls_type), data=dumps(set_hash))
        if ret.status_code / 100 == 2:
            return True
        elif ret.status_code / 100 == 5:
            raise PMClientError("Internal Server Error (%s) %s"%(ret.status_code, ret.content))
        else:
            raise PMClientError("Unknown Error (%s) %s"%(ret.status_code, ret.content))

    def update(self, cls_type, query_hash, set_hash):
        """
        Update the object of type returned from query_hash and
        set the values in set_hash
        """
        ret = requests.post('%s/%s'%(self.url, cls_type), params=query_hash, data=dumps(set_hash))
        if ret.status_code / 100 == 2:
            return True
        if ret.status_code / 100 == 4:
            return False
        elif ret.status_code / 100 == 5:
            raise PMClientError("Internal Server Error (%s) %s"%(ret.status_code, ret.content))
        else:
            raise PMClientError("Unknown Error (%s) %s"%(ret.status_code, ret.content))

    def get(self, cls_type, query_hash):
        """
        Get the object of type from query_hash
        """
        ret = requests.get("%s/%s"%(self.url, cls_type), params=query_hash, allow_redirects=True)
        if ret.status_code / 100 == 2:
            return loads(ret.content)
        elif ret.status_code / 100 == 4:
            return {}
        elif ret.status_code / 100 == 5:
            raise PMClientError("Internal Server Error (%s) %s"%(ret.status_code, ret.content))
        else:
            raise PMClientError("Unknown Error (%s) %s"%(ret.status_code, ret.content))

    def delete(self, cls_type, query_hash):
        """
        Delete the object of type from query_hash
        """
        ret = requests.delete("%s/%s"%(self.url, cls_type), params=query_hash, allow_redirects=True)
        if ret.status_code / 100 == 2 or ret.status_code / 100 == 4:
            return True
        elif ret.status_code / 100 == 5:
            raise PMClientError("Internal Server Error (%s) %s"%(ret.status_code, ret.content))
        else:
            raise PMClientError("Unknown Error (%s) %s"%(ret.status_code, ret.content))
