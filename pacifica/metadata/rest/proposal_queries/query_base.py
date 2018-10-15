#!/usr/bin/python
# -*- coding: utf-8 -*-
"""CherryPy Status Metadata proposalinfo base class."""
import datetime


class QueryBase(object):
    """Retrieves a set of proposals for a given keyword set."""

    @staticmethod
    def format_proposal_block(proposal_entry, instruments=None):
        """Construct a dictionary from a given proposal instance in the metadata stack."""
        _pe = proposal_entry
        if _pe.closed_date is not None and _pe.actual_end_date is not None:
            _pe.actual_end_date = _pe.actual_end_date if _pe.actual_end_date < _pe.closed_date else _pe.closed_date
        else:
            if _pe.closed_date is not None and _pe.actual_end_date is None:
                _pe.actual_end_date = _pe.closed_date

        now = datetime.datetime.now().date()

        proposal_state = 'inactive'
        currently_active = True if _pe.actual_start_date is not None and _pe.actual_start_date < now else False
        currently_closed = True if currently_active and _pe.actual_end_date is not None and \
            _pe.actual_end_date < now else False

        if not currently_active:
            proposal_state = 'pre_active'
        else:
            if not currently_closed:
                proposal_state = 'active'
            else:
                proposal_state = 'closed'

        currently_active = True if proposal_state == 'active' and (
            _pe.actual_end_date is None or _pe.actual_end_date >= now) else False
        proposal_state = 'invalid' if _pe.actual_start_date is None and _pe.actual_end_date is None else proposal_state
        title = _pe.title if _pe.title is not None else '<Title Unspecified>'
        year = _pe.actual_end_date.year if _pe.actual_end_date is not None else 'Unknown'
        return_block = {
            'id': _pe.id,
            'title': title,
            'category': year,
            'display_name': u'[Proposal {0}]: {1}'.format(_pe.id, _pe.title),
            'currently_active': currently_active,
            'state': proposal_state,
            'start_date': _pe.actual_start_date.strftime('%Y-%m-%d') if _pe.actual_start_date is not None else '---',
            'end_date': _pe.actual_end_date.strftime('%Y-%m-%d') if _pe.actual_end_date is not None else '---',
            'closed_date': _pe.closed_date.strftime('%Y-%m-%d') if _pe.closed_date is not None else '---',
            'science_theme': _pe.science_theme,
            'proposal_type': _pe.proposal_type.lower().title()
        }
        if instruments is not None:
            return_block['instruments'] = instruments

        return return_block

    @staticmethod
    def proposal_help_block_message():
        """Assemble a block of relevant help text to be returned with an invalid request."""
        message = 'You must supply either a proposal id (like "/proposalinfo/<proposal_id>")'
        message += ' or search for one using the form "/proposalinfo/search/<search_term_1>+<search_term_2>"'
        return message
