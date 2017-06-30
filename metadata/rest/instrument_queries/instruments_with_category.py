"""CherryPy Status Metadata object class."""
from cherrypy import tools
from metadata.orm import Instruments
from metadata.rest.instrument_queries.query_base import QueryBase


class InstrumentsWithCategory(QueryBase):
    """InstrumentsByCategory API."""

    exposed = True

    @staticmethod
    def get_instruments_with_category():
        """Return a dictionary containing information about a given instrument."""
        objs = Instruments.select(
            Instruments.id, Instruments.display_name,
            Instruments.name, Instruments.name_short,
            Instruments.active
        )

        inst_list = {obj.id: QueryBase.format_instrument_block(obj) for obj in objs}

        return inst_list

    # pylint: disable=invalid-name
    # pylint: disable=duplicate-code
    @staticmethod
    @tools.json_out()
    def GET():
        """Return a set of instruments arranged by category."""
        return InstrumentsWithCategory.get_instruments_with_category()
