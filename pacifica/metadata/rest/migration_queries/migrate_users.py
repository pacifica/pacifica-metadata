#!/usr/bin/python
# -*- coding: utf-8 -*-
"""CherryPy Metadata Migration Class for User Entities."""
from cherrypy import tools
from peewee import prefetch
from pacifica.metadata.orm import Users
from pacifica.metadata.orm import ProposalParticipant, InstrumentCustodian, InstitutionPerson
from pacifica.metadata.rest.user_queries.query_base import QueryBase as UserQueryBase


class MigrateUsers(object):
    """Generate a streamlined query for importing instrument entities and linkages."""

    exposed = True

    @staticmethod
    def generate_user_list():
        """Generate user objects with linkages."""
        user_list = {}
        user_collection = (Users
                           .select()
                           .where(Users.deleted.is_null()))

        proposal_collection = ProposalParticipant.select()
        custodian_collection = InstrumentCustodian.select()
        institution_collection = InstitutionPerson.select()

        users_expanded = prefetch(
            user_collection, proposal_collection,
            custodian_collection, institution_collection)

        for user in users_expanded:
            user_entry = UserQueryBase.format_user_block(user, 'simple')
            user_entry['proposals'] = [
                prop.proposal.id for prop in user.proposals]
            user_entry['custodian_list'] = [
                inst.instrument.id for inst in user.instruments]
            user_entry['institutions'] = [
                place.institution.id for place in user.institutions]
            user_list[user.id] = user_entry

        return user_list

    # CherryPy requires these named methods
    # pylint: disable=invalid-name
    @staticmethod
    @tools.json_out()
    def GET():
        """CherryPy GET Method."""
        return MigrateUsers.generate_user_list()
