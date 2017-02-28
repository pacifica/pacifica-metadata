"""CherryPy Status Metadata proposalinfo base class."""
import re


class QueryBase(object):
    """Retrieves a set of instruments for a given keyword set."""

    @staticmethod
    def format_instrument_block(instrument_entry):
        """Construct a dictionary from a given proposal instance in the metadata stack."""
        _ie = instrument_entry
        name_components = re.search(r'(.+):\s*(.+)', str(_ie.name))
        category = name_components.group(1) if name_components is not None else 'Miscellaneous'
        name = name_components.group(2) if name_components is not None else _ie.name
        display_name = '[{0} / ID:{1}] {2}'.format(
            category, _ie.id, name
        )
        return {
            'id': _ie.id,
            'category': category,
            'display_name': display_name,
            'name': name,
            'name_short': _ie.name_short,
            'active': _ie.active
        }

    @staticmethod
    def instrument_help_block_message():
        """Assemble a block of relevant help text to be returned with an invalid request."""
        message = 'You must supply either a instrument id (like "/instrumentinfo/<instrument_id>")'
        message += ' or search for one using the form "/instrumentinfo/search/<search_term_1>+<search_term_2>"'
        return message
