"""CherryPy Status Metadata proposalinfo base class."""


class QueryBase(object):
    """Retrieves a set of instruments for a given keyword set."""

    @staticmethod
    def format_instrument_block(instrument_entry):
        """Construct a dictionary from a given proposal instance in the metadata stack."""
        _ie = instrument_entry
        return {
            'id': _ie.id,
            'display_name': _ie.display_name,
            'name': _ie.name,
            'name_short': _ie.name_short,
            'active': _ie.active
        }

    @staticmethod
    def instrument_help_block_message():
        """Assemble a block of relevant help text to be returned with an invalid request."""
        message = 'You must supply either a instrument id (like "/instrumentinfo/<instrument_id>")'
        message += ' or search for one using the form "/instrumentinfo/search/<search_term_1>+<search_term_2>"'
        return message
