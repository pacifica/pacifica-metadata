#!/usr/bin/python
# -*- coding: utf-8 -*-
"""CherryPy Metadata Migration Class for Instrument Entities."""
from cherrypy import tools
from peewee import prefetch
from pacifica.metadata.orm import Proposals
from pacifica.metadata.orm import ProposalInstrument, ProposalParticipant
from pacifica.metadata.rest.proposal_queries.query_base import QueryBase as PropQueryBase


class MigrateProposals(object):
    """Generate a streamlined query for importing proposal entities and linkages."""

    exposed = True

    @staticmethod
    def generate_proposal_list():
        """Generate proposal objects with linkages."""
        proposal_list = {}
        prop_collection = (Proposals
                           .select()
                           .order_by(Proposals.id)
                           .where(Proposals.deleted.is_null()))
        instrument_collection = (ProposalInstrument.select(
        ).order_by(ProposalInstrument.instrument))
        person_collection = (ProposalParticipant.select(
        ).order_by(ProposalParticipant.person))

        proposals_with_links = prefetch(
            prop_collection, instrument_collection, person_collection)

        for prop in proposals_with_links:
            prop_entry = PropQueryBase.format_proposal_block(prop)
            prop_entry['abstract'] = prop.abstract
            prop_entry['instruments'] = [
                inst.instrument.id for inst in prop.instruments]
            prop_entry['users'] = [
                user_entry.person.id for user_entry in prop.users]
            proposal_list[prop.id] = prop_entry

        return proposal_list

    # CherryPy requires these named methods
    # pylint: disable=invalid-name
    @staticmethod
    @tools.json_out()
    def GET():
        """CherryPy GET Method."""
        return MigrateProposals.generate_proposal_list()
