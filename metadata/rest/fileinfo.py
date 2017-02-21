"""Core interface for the fileinfo metadataobjects."""
from metadata.rest.fileinfo_queries.file_details import FileDetailsLookup
from metadata.rest.fileinfo_queries.earliest_latest import EarliestLatestFiles


# pylint: disable=too-few-public-methods
class FileInfoAPI(object):
    """FileInfoAPI."""

    exposed = True

    def __init__(self):
        """Create local objects for subtree items."""
        self.file_details = FileDetailsLookup()
        self.earliest_latest = EarliestLatestFiles()
