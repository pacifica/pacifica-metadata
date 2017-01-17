"""Core interface for the fileinfo metadataobjects."""
from metadata.rest.fileinfo_queries.file_details import FileDetailsLookup


# pylint: disable=too-few-public-methods
class FileInfoAPI(object):
    """FileInfoAPI."""

    exposed = True

    def __init__(self):
        """Create local objects for subtree items."""
        self.file_details = FileDetailsLookup()
