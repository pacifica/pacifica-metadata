"""CherryPy Metadata Instrument Categories Class."""
import re
from collections import defaultdict
from cherrypy import tools
from metadata.orm import Instruments
from metadata.rest.instrument_queries.query_base import QueryBase


class InstrumentCategories(QueryBase):
    """Calculates a set of instrument categories from the display names of EUS instruments."""

    exposed = True

    @staticmethod
    def _derived_instrument_categories():
        """Extract category names from the display name strings for EUS Instruments."""
        inst_collection = Instruments.select(
            Instruments.id, Instruments.name, Instruments.display_name
        )
        category_list = []
        categorized_instruments = defaultdict(list)
        uncategorized_instruments = {}
        for inst in inst_collection:
            # print "ID => {0} / inst_name => {1} / disp_name => {2}".format(inst.id, inst.name, inst.display_name)
            match = re.match(r'^(.+?):\s+(.+)', inst.name)
            if match:
                category = match.group(1)
                category_list.append(category)
                categorized_instruments[category].append(inst.id)
            else:
                uncategorized_instruments[inst.id] = inst.display_name

        for inst_id in uncategorized_instruments:
            categorized_instruments['Miscellaneous'].append(inst_id)
        return categorized_instruments

    # CherryPy requires these named methods
    # pylint: disable=invalid-name
    @staticmethod
    @tools.json_out()
    def GET():
        """CherryPy GET method."""
        return InstrumentCategories._derived_instrument_categories()
